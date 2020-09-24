# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.134.1/containers/python-3/.devcontainer/base.Dockerfile
ARG VARIANT="3"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

ENV CVFI_LOGLEVELCONSOLE=20
ENV FILE_HOSP=https://www.data.gouv.fr/fr/datasets/r/63352e38-d353-4b54-bfd1-f1b3ee1cabd7
ENV SCHEDULE=19:15
ENV SCHEDULE_DELTA_M=30
ENV WAIT_NEW_M=10
ENV INFLUX_PORT=8086
ENV INFLUX_DB=covidfr

# [Optional] If your pip requirements rarely change, uncomment this section to add them to the image.
COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
   && rm -rf /tmp/pip-tmp

VOLUME [ "/data" ]