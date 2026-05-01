#!/usr/bin/env bash
set -euo pipefail


if command -v docker >/dev/null 2>&1; then
  echo "[devcontainer] Docker CLI found: $(docker --version)"
else
  echo "[devcontainer] WARNING: Docker CLI is not installed 
in the container."
  echo "[devcontainer] The devcontainer image installs Docker
CLI, but the environment may not have been rebuilt."
fi


if [ -S /var/run/docker.sock ]; then
  echo "[devcontainer] Docker socket is available at 
/var/run/docker.sock"
  if docker info >/dev/null 2>&1; then
    echo "[devcontainer] Docker daemon is reachable."
  else
    echo "[devcontainer] WARNING: Docker daemon socket 
exists, but 'docker info' failed."
    echo "[devcontainer] Check host Docker runtime and 
permissions on /var/run/docker.sock."
  fi
else
  echo "[devcontainer] WARNING: Docker socket 
/var/run/docker.sock is missing."
  echo "[devcontainer] Ensure the container is rebuilt with 
the socket mount enabled."
fi


