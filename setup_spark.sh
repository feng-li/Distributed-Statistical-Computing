#
# USAGE:
#       source setup_spark.sh

export JAVA_HOME=/usr/lib/jvm/default-java
export SPARK_HOME=${HOME}/.APP/spark/
export PATH=${SPARK_HOME}/bin:$PATH

export PYARROW_IGNORE_TIMEZONE=1
