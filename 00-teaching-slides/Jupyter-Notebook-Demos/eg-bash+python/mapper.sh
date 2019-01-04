#! /bin/bash

awk -F '\t' '{printf ("%s\t%s\t%s\t%s\n", $1, $2, $4,$5)}'

