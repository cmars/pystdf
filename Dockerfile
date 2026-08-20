# Build a runnable PySTDF image using uv.
#   docker build -t pystdf .
#   docker run --rm pystdf stdf2text somefile.stdf
FROM python:3.11-slim

# Install uv (the Python toolchain manager) system-wide.
RUN pip install --no-cache-dir uv

WORKDIR /app

# Install third-party dependencies from the lock file (layer-cached).
# --no-install-project: skip building the local package; its source directory
# is not present in this layer yet.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

# Add the project source, then build + install it into the venv (editable).
# This also creates the CLI entry points (stdf2text, stdf_slice, ...).
COPY . .
RUN uv sync --frozen

# Put the venv's bin directory (and thus the PySTDF CLI tools) on PATH.
ENV PATH="/app/.venv/bin:$PATH"
ENTRYPOINT ["uv", "run"]
