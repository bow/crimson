FROM python:3.10.4-alpine AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR /src

RUN apk add --update --no-cache build-base~=0 make~=4 git~=2 libffi-dev~=3 py3-pip~=22 \
    && pip --no-cache-dir install poetry==1.1.13 poetry-dynamic-versioning==0.16.0 twine==4.0.1

COPY .git /src/.git

RUN git checkout -- . \
    && WHEEL_DEPS_DIR=/wheels/deps make build build-deps \
    && mv dist/*.whl /wheels/

# --- #

FROM python:3.10.4-alpine

ARG REVISION
ARG BUILD_TIME

LABEL org.opencontainers.image.title="crimson"
LABEL org.opencontainers.image.revision="${REVISION}"
LABEL org.opencontainers.image.created="${BUILD_TIME}"

ENV PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR /runtime
COPY --from=builder /wheels /wheels

RUN apk add --update --no-cache py3-pip~=22 \
    && pip install --no-cache-dir --no-index --find-links=/wheels/deps /wheels/deps/* \
    && pip install --no-cache-dir --no-index --no-deps --find-links=/wheels crimson \
    && apk --purge del py3-pip \
    && rm -rf /wheels/

ENTRYPOINT ["crimson"]
