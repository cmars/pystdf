# Default: sync the environment, run the test suite, then build the package.
default: sync test build

# Create/sync the local .venv and install the project + dev deps from uv.lock.
sync:
    uv sync

# Run the test suite inside the managed environment.
test:
    uv run pytest tests/ -v

# Build the sdist and wheel into ./dist.
build:
    uv build

# Re-resolve and refresh the lock file.
lock:
    uv lock

### The following may be somewhat specific to my development environment

# Build an image with pi-dev for menial tasks
pi-sandbox:
    podman build -t pi-sandbox -f ./.pi/Dockerfile .

# Drop into a development environment shell using same setup
dev: pi-sandbox
    podman run --rm -it \
        -e LMSTUDIO_API_KEY=$(gopass show auth/lm-studio/dev) \
        -v ${PWD}:/workspace:z \
        -v ${PWD}/.pi:/root/.pi:z \
        --entrypoint /bin/bash \
        pi-sandbox

# Launch pi in a podman container isolated from the host
pi: pi-image
    podman run --rm -it \
        -e LMSTUDIO_API_KEY=$(gopass show auth/lm-studio/dev) \
        -v ${PWD}:/workspace:z \
        -v ${PWD}/.pi:/root/.pi:z \
        pi-sandbox

