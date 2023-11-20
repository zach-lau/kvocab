# Problem on mac with jpype so we build it from source
FROM --platform=$BUILDPLATFORM ubuntu:jammy as build
WORKDIR /root
RUN apt-get update
RUN apt-get install -y musl-dev git python3 pip default-jdk
RUN git clone https://github.com/jpype-project/jpype.git
WORKDIR jpype
RUN python3 setup.py build

FROM --platform=$BUILDPLATFORM ubuntu:jammy as kvocab
RUN apt-get update
# We need jdk for install (might be a better way)
RUN apt-get install -y musl-dev default-jdk python3 pip
WORKDIR /code
COPY requirements.txt /code
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt
RUN pip3 uninstall -y JPype1
WORKDIR /root
COPY --from=build /root/jpype /root/jpype
WORKDIR /root/jpype
RUN python3 setup.py install
ENV PYTHONPATH=${PYTHONPATH}:.
COPY . /code
