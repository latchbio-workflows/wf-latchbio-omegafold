
# Base Image
FROM nvidia/cuda:12.1.0-cudnn8-devel-ubuntu20.04
# FROM nvidia/cuda:12.6.0-cudnn-devel-ubuntu20.04

# Latch environment building
COPY --from=812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base-cuda:fe0b-main /bin/flytectl /bin/flytectl
WORKDIR /root

ENV VENV /opt/venv
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONPATH /root
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y libsm6 libxext6 libxrender-dev build-essential procps rsync openssh-server

RUN apt-get install -y software-properties-common &&\
    add-apt-repository -y ppa:deadsnakes/ppa &&\
    apt-get install -y python3.9 python3-pip python3.9-distutils curl

RUN python3.9 -m pip install --upgrade pip && python3.9 -m pip install awscli

RUN curl -L https://github.com/peak/s5cmd/releases/download/v2.0.0/s5cmd_2.0.0_Linux-64bit.tar.gz -o s5cmd_2.0.0_Linux-64bit.tar.gz &&\
    tar -xzvf s5cmd_2.0.0_Linux-64bit.tar.gz &&\
    mv s5cmd /bin/ &&\
    rm CHANGELOG.md LICENSE README.md

COPY --from=812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base-cuda:fe0b-main /root/Makefile /root/Makefile
COPY --from=812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base-cuda:fe0b-main /root/flytekit.config /root/flytekit.config

WORKDIR /tmp/docker-build/work/

SHELL [ \
    "/usr/bin/env", "bash", \
    "-o", "errexit", \
    "-o", "pipefail", \
    "-o", "nounset", \
    "-o", "verbose", \
    "-o", "errtrace", \
    "-O", "inherit_errexit", \
    "-O", "shift_verbose", \
    "-c" \
]

ENV TZ='Etc/UTC'

ENV LANG='en_US.UTF-8'
ARG DEBIAN_FRONTEND=noninteractive

# Install system requirements
RUN apt-get update --yes && \
    xargs apt-get install --yes aria2 git wget unzip

# Install Miniconda
# RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh && \
#     bash miniconda.sh -b -p /root/miniconda && \
#     rm miniconda.sh

RUN pip3 install torch torchvision torchaudio biopython

RUN git clone https://github.com/HeliXonProtein/OmegaFold

# Latch SDK
# DO NOT REMOVE
RUN pip install latch==2.52.2
RUN mkdir /opt/latch

# Copy workflow data (use .dockerignore to skip files)
COPY . /root/

# Latch workflow registration metadata
# DO NOT CHANGE
ARG tag
# DO NOT CHANGE
ENV FLYTE_INTERNAL_IMAGE $tag

WORKDIR /root
