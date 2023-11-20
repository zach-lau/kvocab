#!/usr/bin/env bash
THISDIR=$(realpath $(dirname $0))
export PATH=${PATH}:${THISDIR}
export PYTHONPATH=${PYTHONPATH}:${THISDIR}/..
