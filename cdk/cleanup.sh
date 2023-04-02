#!/bin/bash

dir="lambda"

for file in "$dir"/*
do
  if [ "$file" != "$dir/lambda.py" ] && [ "$file" != "$dir/$(basename $0)" ]
  then
    rm -r "$file"
  fi
done
