#!/bin/bash

echo
echo "+================================"
echo "| START: ForgetToReadLater"
echo "+================================"
echo

source backend/.env

datehash=`date | md5sum | cut -d" " -f1`
abbrvhash=${datehash: -8}
echo "Using conn string ${MDBCONNSTR}"

echo 
echo "Building container using tag ${abbrvhash}"
echo
docker build -t graboskyc/forgettoreadlater:latest -t graboskyc/forgettoreadlater:${abbrvhash} --platform=linux/amd64 .

EXITCODE=$?

if [ $EXITCODE -eq 0 ]
    then

    echo 
    echo "Starting container"
    echo
    docker stop forgettoreadlater
    docker rm forgettoreadlater
    docker run -t -i -d -p 8000:8000 --name forgettoreadlater -e "MDBCONNSTR=${MDBCONNSTR}" --restart unless-stopped graboskyc/forgettoreadlater:${abbrvhash}

    echo
    echo "+================================"
    echo "| END:  ForgetToReadLater"
    echo "+================================"
    echo
else
    echo
    echo "+================================"
    echo "| ERROR: Build failed"
    echo "+================================"
    echo
fi