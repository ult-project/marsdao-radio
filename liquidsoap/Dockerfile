FROM debian:stable-slim

ENV DEBIAN_FRONTEND noninteractive

# install liquidsoap dependencies
RUN set -x; \
    apt update && apt upgrade -y && \
    apt install -y \
    gcc \
    make \
    m4 \
    opam \
    ffmpeg \
    debianutils \
    pkg-config \
    zlib1g-dev \
    libavcodec-dev \
    libavdevice-dev \
    libavfilter-dev \
    libavformat-dev \
    libavutil-dev \
    libcurl4-gnutls-dev \
    libmad0-dev \
    libmp3lame-dev \
    libogg-dev \
    libpcre3-dev \
    libsamplerate0-dev \
    libswresample-dev \
    libswscale-dev \
    libtag1-dev \
    libtheora-dev \
    libvorbis-dev \
    logrotate

COPY logrotate.conf /etc/logrotate.d

# add user for liquidsoap and create necessary directories
RUN set -x; \
    groupadd -g 999 radio && \
    useradd -m -r -u 999 -s /bin/bash -g radio radio && \
    mkdir -p /etc/liquidsoap /radio/music /radio/logs && \
    chown -R radio /etc/liquidsoap /radio

ARG LIQUIDSOAP_VERSION
ARG OPAM_PACKAGES="liquidsoap${LIQUIDSOAP_VERSION:+.$LIQUIDSOAP_VERSION} ffmpeg taglib mad lame ogg vorbis theora cry samplerate"

USER radio

# setup opam
RUN set -x; \
    opam init -a -y --disable-sandboxing && \
    eval $(opam env)

# install liquidsoap
RUN set -x; \
    opam install -y ${OPAM_PACKAGES} && \
    eval $(opam env) && \
    opam clean -acryv --logs --unused-repositories

CMD eval $(opam env) && liquidsoap /etc/liquidsoap/radio.liq
