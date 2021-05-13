from pyspark.sql.functions import col, when
from pyspark.sql import functions as F
import pyspark.sql.types as T
from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler
from pyspark.ml import Pipeline
from pyspark.sql.window import Window


def get_sdummies(sdf,
                 dummy_columns,
                 keep_top,
                 replace_with='000_OTHERS',
                 dummy_info=[],
                 dropLast=False,
                 sparse=False):
    """Index string columns and group all observations that occur in less then a keep_top% of the rows in sdf per column.

    :param sdf: A pyspark.sql.dataframe.DataFrame
    :param dummy_columns: String columns that need to be indexed
    :param keep_top: List [1, 0.8, 0.8]
    :param replace_with: String to use as replacement for the observations that need to be
    grouped.
    :param dropLast: bool. Whether to get k-1 dummies out of k categorical levels by
    removing the last level. Note that it behaves differently with pandas.get_dummies()
    where it drops the first level.

    return sdf, dummy_info
    """
    total = sdf.count()
    column_i = 0

    factor_set = {}  # The full dummy sets
    factor_selected = {}  # Used dummy sets
    factor_dropped = {}  # Dropped dummy sets
    factor_selected_names = {}  # Final revised factors with ordered by ONEHOT encoding

    for string_col in dummy_columns:

        if len(dummy_info) == 0:
            # Descending sorting with counts
            sdf_column_count = sdf.groupBy(string_col).count().orderBy(
                'count', ascending=False)
            sdf_column_count = sdf_column_count.withColumn(
                "cumsum",
                F.sum("count").over(Window.orderBy(F.monotonically_increasing_id())))

            # Obtain top dummy factors: the cumulative percentage of kept dummy factors
            # should reach e.g. top %90 and group the remaining dummy factors 10% as
            # `others`. Also always keep dummy factors that has 10% ratio of the total.
            sdf_column_top_dummies = sdf_column_count.withColumn(
                "cumperc", sdf_column_count['cumsum'] /
                total).filter((col('cumperc') <= keep_top[column_i]) |
                              (col('count') >= 0.1 * total))

            keep_list = sdf_column_top_dummies.select(string_col).rdd.flatMap(
                lambda x: x).collect()

            # Save factor sets
            factor_set[string_col] = sdf_column_count.select(
                string_col).rdd.flatMap(lambda x: x).collect()
            factor_selected[string_col] = keep_list
            factor_dropped[string_col] = list(
                set(factor_set[string_col]) - set(keep_list))

            # Get correct encoding order of dummies. NOTE that in Spark, ONEHOT encoding
            # sort dummies according to the weights, the factor with highest wight will be
            # labeled 0, then 1, 2, ... TODO: better solution with IndexEncoder
            factor_old_len = len(factor_selected[string_col])
            factor_count = sdf_column_count.limit(factor_old_len).select([string_col, 'count']).toPandas()
            factor_count['perc'] = factor_count['count'] / total

            if len(factor_dropped[string_col]) != 0:
                factor_count = factor_count.append(
                    {string_col: replace_with, 'count': None,
                     'perc': 1 - factor_count['perc'].sum()},
                    ignore_index = True)
            # Descending sorting by percentage
            factor_count = factor_count.sort_values(by='perc', ascending=False)
            factor_selected_names[string_col] = factor_count[string_col].tolist()
            if dropLast:
                factor_selected_names[string_col] = factor_selected_names[string_col][:-1]

        else:
            keep_list = dummy_info["factor_selected"][string_col]

        # Replace dropped dummy factors with grouped factors.
        sdf = sdf.withColumn(
            string_col,
            when((col(string_col).isin(keep_list)),
                 col(string_col)).otherwise(replace_with))

        column_i += 1

    # The index of string vlaues multiple columns
    indexers = [
        StringIndexer(inputCol=c, outputCol="{0}_IDX".format(c))
        for c in dummy_columns
    ]

    # The encode of indexed vlaues multiple columns
    encoders = [
        OneHotEncoder(dropLast=dropLast,
                      inputCol=indexer.getOutputCol(),
                      outputCol="{0}_ONEHOT".format(indexer.getOutputCol()))
        for indexer in indexers
    ]

    # Vectorizing encoded values
    assembler = VectorAssembler(
        inputCols=[encoder.getOutputCol() for encoder in encoders],
        outputCol="features_ONEHOT")

    pipeline = Pipeline(stages=indexers + encoders + [assembler])
    # pipeline = Pipeline(stages=[assembler])
    onehot_model = pipeline.fit(sdf)
    sdf = onehot_model.transform(sdf)

    # Convert Spark SparseVector (VectorUDT type not supported by Pandas UDF) to dense list
    if sparse is False:
        to_array = F.udf(lambda v: v.toArray().tolist(), T.ArrayType(T.FloatType()))
        sdf = sdf.withColumn('features_ONEHOT', to_array('features_ONEHOT'))

    # Drop intermediate columns
    drop_columns = [x + "_IDX" for x in dummy_columns]
    drop_columns = [x + "_ONEHOT" for x in drop_columns] + drop_columns

    sdf = sdf.drop(*drop_columns)

    if len(dummy_info) == 0:
        dummy_info = {
            'factor_set': factor_set,
            'factor_selected': factor_selected,
            'factor_dropped': factor_dropped,
            'factor_selected_names': factor_selected_names
        }

    return sdf, dummy_info
