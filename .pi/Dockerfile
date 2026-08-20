FROM node:24-bookworm-slim

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    bash build-essential ca-certificates capnproto curl git \
    python3 ripgrep vim \
  && rm -rf /var/lib/apt/lists/*
ENV EDITOR=vim
COPY --from=ghcr.io/casey/just:latest /just /usr/local/bin/
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/
RUN npm install -g --ignore-scripts @earendil-works/pi-coding-agent
RUN pi install npm:pi-read-map

WORKDIR /workspace
ENTRYPOINT ["pi"]
