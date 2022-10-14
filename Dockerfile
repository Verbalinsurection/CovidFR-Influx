FROM python:3.11.0rc2

WORKDIR /code
VOLUME /data

ENV CVFI_LOGLEVELCONSOLE=20
ENV FILE_HOSP=https://www.data.gouv.fr/fr/datasets/r/63352e38-d353-4b54-bfd1-f1b3ee1cabd7
ENV SCHEDULE=19:15
ENV SCHEDULE_DELTA_M=30
ENV WAIT_NEW_M=10
ENV INFLUX_PORT=8086
ENV INFLUX_DB=covidfr

COPY requirements.txt .
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /code/requirements.txt \
   && rm -rf /code/requirements.txt

COPY main.py .
COPY modules ./modules

CMD [ "python", "-u", "./main.py" ]
