FROM jupyter/scipy-notebook
MAINTAINER iwasakishuto <cabernet.rock@gmail.com>

USER root
# Install system packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      vim \
      bzip2 \
      g++ \
      git \
      graphviz \
      libgl1-mesa-glx \
      libhdf5-dev \
      openmpi-bin \
      wget && \
    rm -rf /var/lib/apt/lists/*

# Permission.
ENV NB_USER pyguitar
ENV NB_UID 1001
RUN useradd -m -s /bin/bash -N -u $NB_UID $NB_USER && \
    mkdir -p /src && \
    chown $NB_USER /src
USER $NB_USER

# Install Python packages and PyGuitar
RUN pip install --upgrade pip && \
    pip install \
      matplotlib>=2.2.4 \
      selenium>=3.6.0 && \
      git clone git://github.com/iwasakishuto/PyGuitar.git /src && pip install -e /src[tests] && \
      pip install git+git://github.com/iwasakishuto/PyGuitar.git

# matplotlib Japanese.
RUN wget https://ipafont.ipa.go.jp/IPAfont/IPAfont00303.zip -O font.zip && \
    unzip font.zip && \
    cp IPAfont00303/ipam.ttf /opt/conda/lib/python3.7/site-packages/matplotlib/mpl-data/fonts/ttf/ipam.ttf && \
    echo "font.family : IPAMincho" >>  /opt/conda/lib/python3.7/site-packages/matplotlib/mpl-data/matplotlibrc && \
    rm -r ./.cache

ENV PYTHONPATH='/src/:$PYTHONPATH'

WORKDIR /data

CMD jupyter notebook --port=8888 --ip=0.0.0.0
