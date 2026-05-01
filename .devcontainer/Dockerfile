# Dev container image for PejicLang Core
FROM mcr.microsoft.com/devcontainers/python:1-3.12


# Install Docker CLI and compose plugin inside the dev 
container
RUN apt-get update \
    && apt-get install -y --no-install-recommends docker.io 
docker-compose-plugin \
    && if [ -f /usr/libexec/docker/cli-plugins/docker-compose 
] && [ ! -e /usr/bin/docker-compose ]; then \
         ln -s /usr/libexec/docker/cli-plugins/docker-compose 
/usr/bin/docker-compose; \
       fi \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /workspace
