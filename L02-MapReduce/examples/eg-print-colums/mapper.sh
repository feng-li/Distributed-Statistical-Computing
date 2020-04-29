#! /bin/bash

# print some columns of my data
awk -F '\t' '{printf ("%s\t%s\t%s\t%s\n",  $1, $2, $10, $12)}'

