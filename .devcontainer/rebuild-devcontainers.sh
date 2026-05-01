#!/usr/bin/env bash
set -euo pipefail


if ! command -v docker >/dev/null 2>&1; then
  echo "[rebuild] Docker CLI is required to rebuild the 
devcontainer image."
  echo "[rebuild] Install Docker on the host or use VS Code 
Dev Container rebuild."
  exit 1
fi


IMAGE_NAME="pejic-lang-core-devcontainer"
DOCKERFILE=".devcontainer/Dockerfile"
CONTEXT="."


echo "[rebuild] Building devcontainer image '$IMAGE_NAME' 
from '$DOCKERFILE'..."
docker build -f "$DOCKERFILE" -t "$IMAGE_NAME" "$CONTEXT"


echo "[rebuild] Build complete."
echo "[rebuild] If you are in VS Code, run 'Rebuild 
Container' to apply the new image."

