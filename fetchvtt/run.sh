#!/usr/bin/env bash
DEBUG=--debug
[[ $1 = "prod" ]] && DEBUG=""
flask run ${DEBUG} --key ../cert/server.key --cert ../cert/server.crt
