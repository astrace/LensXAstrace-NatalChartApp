#!/bin/bash
cd ../..
sam local start-lambda &
  aws lambda invoke \
    --function-name "NatalChartGenFunction" \
    --payload '{"queryStringParameters":{"datetime_string":"04/01/91 17:55:00","location_string":"zenica"}}' \
    out.json \
    --endpoint-url "http://127.0.0.1:3001" \
    --no-verify-ssl \
    --cli-binary-format raw-in-base64-out
OUTPUT=$(jq '.body' out.json | jq -r | jq '.preSignedUrl')
[[ "$OUTPUT" =~ ^\"https.*\"$ ]] && exit 0 || exit 1
rm -f out.json
