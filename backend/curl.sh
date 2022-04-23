#!/bin/sh -x 
curl -s localhost:8080/debug/mytemp | jq
curl -s localhost:8080/debug/geoip | jq
curl -s localhost:8080/debug/users?limit=4 | jq
curl -s -d '{"age":12,"isPublic":false,"status":"working"}' -H 'Content-Type: application/json' localhost:8080/debug/users | jq
