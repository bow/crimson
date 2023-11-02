# Dockerfile for packaging releases.
#
# Copyright (c) 2015-2023 Wibowo Arindrarto <contact@arindrarto.dev>
# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of crimson <https://github.com/bow/crimson>.

FROM python:3.12.0-alpine AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_NO_CACHE_DIR=on

WORKDIR /src

RUN apk add --update --no-cache build-base~=0 make~=4 git~=2 libffi-dev~=3 py3-pip~=23

COPY .git /src/.git

RUN git checkout -- . \
    && WHEEL_DEPS_DIR=/wheels/deps make install-build build \
    && mv dist/*.whl /wheels/

# --- #

FROM python:3.12.0-alpine

ARG REVISION
ARG BUILD_TIME

LABEL org.opencontainers.image.title="crimson"
LABEL org.opencontainers.image.revision="${REVISION}"
LABEL org.opencontainers.image.created="${BUILD_TIME}"

ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_NO_CACHE_DIR=on
ENV PIP_NO_INDEX=on

WORKDIR /app
COPY --from=builder /wheels /wheels

RUN apk add --update --no-cache py3-pip~=23 \
    && pip install --find-links=/wheels/deps /wheels/deps/* \
    && pip install --no-deps --find-links=/wheels crimson \
    && apk --purge del py3-pip \
    && rm -rf /wheels/

ENTRYPOINT ["crimson"]
