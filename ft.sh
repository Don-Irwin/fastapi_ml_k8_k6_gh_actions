#!/bin/bash

good_return_codes=0
bad_return_codes=0


eval_return () {
  my_code="$1"
  

if [ "$my_code" == "200" ]; then

    echo "$my_code"
    let "good_return_codes = good_return_codes+1"

else

    let "bad_return_codes = bad_return_codes+1"

fi

}

eval_return "202"
echo "good_return_codes=${good_return_codes}"
echo "bad_return_codes=${bad_return_codes}"

FILE=./src/model_pipeline.pkl
if test -f "$FILE"; then
    echo "$FILE exists."
fi