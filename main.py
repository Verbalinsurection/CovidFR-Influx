#!/usr/bin/python3

"""Main script."""

import re
from datetime import datetime, timedelta
from os import environ, remove
from os.path import basename
from time import sleep
from urllib.error import HTTPError
from urllib.request import urlopen, urlretrieve

import schedule
from influxdb import InfluxDBClient

import modules.csv_loader as csvl
from modules.logs import CVFILOG

APP_FOLDER = '/data/'
MEASUREMENT = 'Covid_France'
FIXED_HOUR = '20:00:00'


class idbc():
    """Class idbc (InfluxDB Client)."""

    def __init__(self, default_db):
        """Init idbc class."""
        self.__db = environ.get('INFLUX_DB', default_db)
        self.__client = InfluxDBClient(
            environ.get('INFLUX_HOST'),
            int(environ.get('INFLUX_PORT', 8086)),
            environ.get('INFLUX_USER'),
            environ.get('INFLUX_PASS'),
            self.__db)

    def last_record(self):
        """Return datetime of last record, None if no result."""
        query = 'select last("dc") from "' + MEASUREMENT + '";'
        result = self.__client.query(query)

        if len(result) == 0:
            return None

        for val in result.get_points(measurement=MEASUREMENT):
            return val['time'][:10]

    def write_data(self, data_points):
        """Clean database and write datapoints."""
        CVFILOG.debug('Deleting db ' + self.__db)
        self.__client.drop_database(self.__db)
        CVFILOG.debug('Creating db ' + self.__db)
        self.__client.create_database(self.__db)
        CVFILOG.debug('Write points on db')
        return self.__client.write_points(data_points)


def get_remote_filename(url):
    """Return the remote filename, None if error."""
    try:
        response = urlopen(url)
        redir_url = response.url
        return basename(redir_url)
    except HTTPError as e:
        error = ' (' + str(e.code) + ': ' + e.reason + ')'
        CVFILOG.warning('Error ' + url + error)
        return None
    except TimeoutError as e:
        CVFILOG.warning('Timeout ' + url + '(' + e + ')')
        return None


def have_new_data(remote_filename, last_record):
    """Return True if new data on remote."""
    regex = r'(?s)(?<=covid-hospit-).*?(?=-..h)'
    result = re.search(regex, remote_filename)
    if result is None:
        return False

    dt_file = datetime.strptime(result.group(0), '%Y-%m-%d')
    dt_lrecord = datetime.strptime(last_record, '%Y-%m-%d')

    if (dt_file - dt_lrecord).total_seconds() > 0:
        return True
    return False


def download_file(url, dest_filepath, retry=3, wait=60):
    """Download file from url at the given path, False on error."""
    retry_count = 0
    have_error = False
    while retry_count < retry:
        try:
            retry_count += 1
            CVFILOG.debug('Get %s to %s|Try %s' %
                          (url, dest_filepath, str(retry_count)))
            urlretrieve(url, dest_filepath)
        except HTTPError as e:
            error = ' (' + str(e.code) + ': ' + e.reason + ')'
            CVFILOG.warning(url + error)
            have_error = True
        except TimeoutError as e:
            CVFILOG.warning('Timeout ' + url + '(' + e + ')')
            have_error = True
        else:
            CVFILOG.debug('File downloaded')
            return True

        if have_error and retry_count < retry:
            CVFILOG.warning('Waiting %s seconds', wait)
            sleep(wait)

    CVFILOG.error('Can\'t download file from ' + url)
    return False


def process_data():
    """Scheduled process data."""
    start_time = datetime.now()
    stop_time = start_time + timedelta(
        minutes=int(environ.get('SCHEDULE_DELTA_M')))

    waiting = True
    while waiting:
        min_left = int((stop_time - datetime.now()).total_seconds() / 60)
        CVFILOG.info('Check if new data. ' + str(min_left) + ' minutes left.')

        cov_idbc = idbc('covidfr')
        last_record = cov_idbc.last_record()
        remote_filename = get_remote_filename(environ.get('FILE_HOSP'))

        process = False
        if last_record is None:
            process = True
        else:
            if have_new_data(remote_filename, last_record):
                process = True

        if process:
            waiting = False
        else:
            if datetime.now() > stop_time:
                CVFILOG.error('Timeout, no new data')
                return
            else:
                CVFILOG.info('No new data, waiting')
                sleep(int(environ.get('WAIT_NEW_M', '10')) * 60)

    CVFILOG.info('New data to process')
    dest_filepath = APP_FOLDER + remote_filename
    if not download_file(environ.get('FILE_HOSP'), dest_filepath):
        return

    data_points = csvl.load_csv(dest_filepath, FIXED_HOUR, MEASUREMENT)
    if len(data_points) == 0 or data_points is None:
        CVFILOG.error('Downloaded file untreated')
        return
    CVFILOG.info('Measures count: ' + str(len(data_points)))

    if not cov_idbc.write_data(data_points):
        CVFILOG.error('Can\'t write points in db')
        return

    remove(dest_filepath)
    CVFILOG.info('Data recorded in db')


def main():
    """Start main function."""
    process_data()

    schedule.every().day.at(environ.get('SCHEDULE', '19:15')).do(process_data)
    CVFILOG.info('Scheduled at ' + environ.get('SCHEDULE', '19:15'))

    while True:
        schedule.run_pending()
        sleep(1)


if __name__ == "__main__":
    main()
