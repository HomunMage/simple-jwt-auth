#!/bin/bash
echo $(date +%H:%M:%S)
supervisorctl restart fastapi
