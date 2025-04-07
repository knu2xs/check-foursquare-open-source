#!/usr/bin/env python
# coding: utf-8

from configparser import ConfigParser
from datetime import date
import logging
from pathlib import Path

from boto3 import resource
import pandas as pd

from py_message import send_pushover


# path to where foursquare release data is located
bkt_pth = 's3://fsq-os-places-us-east-1/release/'


if __name__ == '__main__':

    # path to where data resources will be cached
    dir_data = Path(__file__).parent.parent / 'data'

    # path to where logs will be saved
    dir_logs = dir_data / 'logs'

    # get today's date
    dt_today = date.today()

    # set up logging
    logging.basicConfig(
        filename=dir_logs / f'check_available_{dt_today.year}{dt_today.month:02d}{dt_today.day}.log',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
        format='%(asctime)s - %(levelname)s - %(message)s',
    )

    # ensure directory for data and logs exist
    if not dir_logs.exists():
        dir_logs.mkdir(parents=True)

    if not dir_data.exists():
        dir_data.mkdir(parents=True)

    # get the path to the configuration secrets file
    config_secrets_pth = Path(__file__).parent.parent / 'config' / 'secrets.ini'

    # check if the configuration secrets file exists
    if not config_secrets_pth.exists():
        raise FileNotFoundError(f"Configuration secrets file does not exist: {config_secrets_pth}")

    # create a config parser object
    config = ConfigParser()

    # read the configuration secrets file
    config.read(config_secrets_pth)

    # get Pushover credentials
    pushover_user_key = config.get('PUSHOVER', 'USER_KEY')
    pushover_api_token = config.get('PUSHOVER', 'API_TOKEN')

    # ensure credentials retrieved
    if pushover_user_key == '' or pushover_user_key == '':
        raise ValueError("Pushover credentials not found in configuration file")
    
    # path to the existing months file
    exist_mth_pth = Path(__file__).parent.parent / 'data' / 'existing_months.csv'

    # see if the existing months file exists
    if not exist_mth_pth.exists():

        # create a data frame to hydrate
        df_exists = pd.DataFrame(columns=['dt'], dtype='datetime64[ns]')

    else:
        # read the existing months file
        df_exists = pd.read_csv(exist_mth_pth, parse_dates=['dt'])

    # see if the current month is already in the existing months file, indicating a notification has already been sent
    already_notified = len(df_exists[(df_exists['dt'].dt.year == dt_today.year) & (df_exists['dt'].dt.month == dt_today.month)]) > 0

    # if the current month has not alaredy been delivered and a notification sent, check for new data``
    if not already_notified:

        # split apart the buckeet string parts on the forward slash
        bkt_prts = [prt for prt in bkt_pth.split('/') if len(prt) > 0 and prt != 's3:']

        # pull out the bucket name
        bkt_name = bkt_prts[0]

        # get the path suffix
        bkt_suffix = '/'.join(bkt_prts[1:])

        # get a bucket object to interrogate
        bkt = resource('s3').Bucket(bkt_name)

        # get the part of the path with the date
        obj_str_set = set(bkt_obj.key.split('/')[1] for bkt_obj in bkt.objects.filter(Prefix=bkt_suffix))

        # get just the date part of the string
        dt_str_lst = [dt_str.split('=')[1] for dt_str in obj_str_set if dt_str.startswith('dt=')]

        # create date objects from the date strings
        dt_lst = [date(*map(int, (dt_str.split('-')))) for dt_str in dt_str_lst]

        # sort so easier to view and work with
        dt_lst.sort()

        # get a list of released dates with the same month and year as current
        mtch_lst = [dt for dt in dt_lst if dt_today.year == dt.year and dt_today.month == dt.month]

        # boolean if data has been released for current month
        data_released = len(mtch_lst) > 1

        # format the date string for the current month
        dt_str = dt_today.strftime('%b %Y')

        # if data has been released for current month
        if data_released:

            # create a message to send
            msg = f"Foursquare data is available for {dt_str}."

            # send the pushover notification
            send_pushover(msg, api_token=pushover_api_token, user_key=pushover_user_key)

            # udpate the existing months file with the current month
            df_exists = pd.concat([df_exists, pd.DataFrame({'dt': [dt_today]})], ignore_index=True)
            df_exists.to_csv(exist_mth_pth, index=False)

        # log if data not yet released
        else:
            logging.info(f"Data not yet released for {dt_str}.")