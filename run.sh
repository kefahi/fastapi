#!/bin/bash
uvicorn --env-file sample.env --port 8080 --app-dir backend --reload main:app
