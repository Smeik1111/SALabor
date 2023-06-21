import argparse
import os

from django.core.management import BaseCommand

from projectApp.download_sentinel5p_data import download_sentinel5p_data


class Command(BaseCommand):
    help = 'Download last 30 days of Sentinel5P data as .nc for a given timeframe'
    timespan_start = 'NOW-30DAYS'
    timespan_end = 'NOW'

    def add_arguments(self, parser):
        parser.add_argument('-f', '--force', action=argparse.BooleanOptionalAction, help='Dont check for existing data', )
        parser.add_argument('-p', '--path', type=str, help='Path to download folder', )


    def handle(self, *args, **kwargs):
        download_sentinel5p_data(kwargs['path'], kwargs['force'], self.timespan_start, self.timespan_end)