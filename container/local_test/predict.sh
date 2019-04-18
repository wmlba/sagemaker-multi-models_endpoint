#!/bin/bash

payload=$1
content=${2:-text/csv}

curl --data-binary @${payload} -H "Content-Type: ${content}" -H "CustomAttributes: customer1" -v http://localhost:8080/invocations
