FROM --platform=$BUILDPLATFORM python:3.10-alpine as kvocab

WORKDIR /code
COPY requirements.txt /code
RUN apk --no-cache add musl-dev linux-headers g++ openblas-dev
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

COPY . /code
