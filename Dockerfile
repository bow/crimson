FROM python:3.10.4-alpine AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR /src

RUN apk add --update --no-cache build-base~=0 make~=4 git~=2 libffi-dev~=3 py3-pip~=20 \
    && pip install poetry==1.1.13

COPY .git /src/.git

RUN git checkout -- . \
    && mkdir -p /wheels/deps/ \
    && poetry export --without-hashes -f requirements.txt -o /tmp/requirements.txt \
    && poetry build -f wheel \
    && mv dist/*.whl /wheels/ \
    && pip wheel -r /tmp/requirements.txt --wheel-dir=/wheels/deps/

# --- #

FROM python:3.10.4-alpine

ARG GIT_COMMIT
ARG BUILD_TIME

LABEL org.opencontainers.image.name="crimson"
LABEL org.opencontainers.image.revision="${GIT_COMMIT}"
LABEL org.opencontainers.image.created="${BUILD_TIME}"

ENV PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR /runtime
COPY --from=builder /wheels /wheels

RUN apk add --update --no-cache py3-pip~=20 \
    && pip install --no-cache-dir --no-index --find-links=/wheels/deps /wheels/deps/* \
    && pip install --no-cache-dir --no-index --no-deps --find-links=/wheels crimson \
    && apk --purge del py3-pip \
    && rm -rf /wheels/

ENTRYPOINT ["crimson"]
