from io import StringIO
from typing import List, Tuple, Dict, Union

from configured_mail_sender import create_sender, MailSender
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from breeze_chms_api.profile_helper import ProfileHelper, join_dicts, profile_compare
from breeze_chms_api import breeze

import logging
import sys
import json
import gzip
import argparse
import os
import platformdirs
import datetime

from breeze_email_reports.table_format import ColSpec, _HTMLFormatter, _CSVFormatter, _TextFormatter

DEFAULT_DATA_DIR = platformdirs.user_data_dir('BreezeProfiles')
DEFAULT_COLUMN_WIDTHS = '30,20,20'


class ProfileData:
    def __init__(self):
        self.datetime_str = 'Unknown'
        self.fields_map = {}
        self.profiles = {}

    def get_datetime(self) -> str:
        """
        Get time of this data dump
        :return: Date time in iso format
        """
        return self.datetime_str

    def get_fields_map(self) -> Dict[str, Dict[str, Union[str, List[str]]]]:
        """
        Get mapping from field id to name
        :return: The mapping
        """
        return self.fields_map

    def get_profile_fields(self) -> Dict[str, Dict[str, Union[str, List[str]]]]:
        """
        Return profile field values as list of tuples. First item in each tuple
        is the profile id. Second is a mapping from field id to Value(s) of
        the field.
        :return: List of profiles with their field values
        """
        return self.profiles

    def save_data(self) -> None:
        """
        Save current data to a new file in the given directory,
        if this was freshly loaded from Breeze.
        :return: None
        """
        return


class ProfileFromBreeze(ProfileData):
    """
    Profile data fetched directly from Breeze.
    """
    def __init__(self,
                 args,
                 breeze_api: breeze.BreezeApi = None,
                 do_save: bool = True):
        """
        Get current data from breeze
        :param args: Command line arguments
        :param breeze_api: Pre-existing Breeze API
        :param do_save: Save results on completion
        """
        ProfileData.__init__(self)
        self.do_save = do_save
        self.args = args
        ProfileData.__init__(self)
        breeze_api = breeze_api if breeze_api \
            else breeze.breeze_api(overrides=args.breeze_creds)
        profile_helper = ProfileHelper(breeze_api.get_profile_fields())
        self.fields_map = profile_helper.get_field_id_to_name()
        people = breeze_api.list_people(details=True)
        self.profiles = profile_helper.process_profiles(people)
        curtime = datetime.datetime.now()
        self.save_file_name = (datetime.datetime.isoformat(curtime)
                               + '.json.gz')
        self.datetime_str = curtime.strftime("%b %d %Y %I:%M%p")

    def save_data(self) -> None:
        if self.do_save:
            new_file = os.path.join(self.args.data, self.save_file_name)
            with gzip.open(new_file, 'w') as outfile:
                towrite = json.dumps((self.fields_map, self.profiles), indent=2)
                outfile.write(bytes(towrite, 'utf8'))


class ProfileFromFile(ProfileData):
    """
    Profile data loaded from a file.
    """
    def __init__(self, filepath: str):
        """
        Load profile fields from a file
        :param filepath:
        """
        ProfileData.__init__(self)
        directory, file = os.path.split(filepath)
        if filepath.endswith('.gz'):
            date_part = file[:-8]
            with gzip.open(filepath, 'r') as prfile:
                data = json.loads(prfile.read())
        else:
            date_part = file[:-5]
            with open(filepath, 'r') as prfile:
                data = json.loads(prfile.read())
        if data:
            (self.fields_map, self.profiles) = data
            try:
                dtime = datetime.datetime.fromisoformat(date_part)
                self.datetime_str = dtime.strftime("%b %d %Y %I:%M%p")
            except ValueError:
                self.datetime_str = 'Unknown'


class EmptyProfile(ProfileData):
    """
    Used when there isn't actually any profile data.
    """
    def __init__(self):
        ProfileData.__init__(self)


class Results:
    def __init__(self,
                 reference_data: ProfileData,
                 current_data: ProfileData):
        """
        Save results of compare and method to save data after successful delivery
        :param reference_data: Previous data
        :param current_data: Current data
        """
        self.reference_data: ProfileData = reference_data
        self.current_data: ProfileData = current_data

    def get_diffs(self) -> List[Tuple[str, List[Tuple[str, List[str], List[str]]]]]:
        """
        Return result of compare
        :return: The list of profile differences
        """
        all_fields = dict(self.reference_data.get_fields_map())
        all_fields.update(self.current_data.get_fields_map())
        joined_values = join_dicts(self.reference_data.get_profile_fields(),
                                   self.current_data.get_profile_fields())

        diffs = profile_compare(joined_values, all_fields)
        # If there are multiple values in a bucket they're in random order
        # Sort them. Alpha order is nice for the report, but mostly
        # this makes repeatable unit test possible.
        for person, fields in diffs:
            for field in fields:
                if field[1]:
                    field[1].sort()
                if field[2]:
                    field[2].sort()
        return diffs

    def save_data(self) -> None:
        """
        Save recent data on successful send of email.
        :return: None
        """
        self.current_data.save_data()

    @property
    def header(self) -> str:
        """
        Return date range of differences as string.
        :return:
        """
        return (f'{self.reference_data.get_datetime()} thru '
                f'{self.current_data.get_datetime()}')


def _generate_diffs(args,
                    breeze_api: breeze.BreezeApi = None) -> Results:
    if args.reference_data:
        # Special case. Run current data against an existing reference
        # and don't save the results
        reference_data = ProfileFromFile(args.reference_data)
        current_data = ProfileFromBreeze(args, breeze_api, do_save=False)
    else:
        prev_saved = [f for f in os.listdir(args.data)
                      if f.endswith(('.json', '.json.gz'))]
        prev_saved.sort(reverse=False)
        if args.replay:
            # Generate report from the two previous runs
            if len(prev_saved) < 2:
                # Need two files for replay
                sys.exit(f'Need at two previous runs in {args.data}')
            reference_data = ProfileFromFile(os.path.join(args.data,
                                                          prev_saved[-2]))
            current_data = ProfileFromFile(os.path.join(args.data,
                                                        prev_saved[-1]))
        else:
            if not prev_saved:
                logging.warning('No previous data found. This will be big!')
                reference_data = EmptyProfile()
            else:
                reference_data = ProfileFromFile(os.path.join(args.data,
                                                 prev_saved[-1]))
            current_data = ProfileFromBreeze(args, breeze_api)

    return Results(reference_data, current_data)


def _verify_directory(args):
    if not (os.access(args.data, os.W_OK | os.R_OK) and os.path.isdir(args.data)):
        sys.exit(f"{args.data} is not a writable directory")


def main(breeze_api: breeze.BreezeApi = None,
         email_sender: MailSender = None):
    """
    Email a report of Breeze profile changes
    :param breeze_api: (For testing) pre-made Breeze API
    :param email_sender: (For testing) email sender
    :return: None
    """

    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(message)s",
        level=logging.INFO
    )

    logging.info(f'Running {" ".join(sys.argv)}')
    # First, figure out what we'll be doing
    parser = argparse.ArgumentParser('Generate report of recent Breeze changes')
    parser.add_argument('--from',
                        '-f',
                        dest='sender',
                        metavar='sender',
                        help='sending email address (required in most cases)')
    parser.add_argument('--to',
                        '-t',
                        metavar='recipient(s)',
                        help='public recipients, comma separated')
    parser.add_argument('--bcc',
                        '-b',
                        metavar='<blind recipient(s)>',
                        help='hidden recipients, comma separated')
    parser.add_argument('--data',
                        '-d',
                        metavar='<data directory>',
                        help=f'directory with history, default: {DEFAULT_DATA_DIR}',
                        default=DEFAULT_DATA_DIR)
    parser.add_argument('--reference_data',
                        metavar='<reference data file>',
                        help='explicit previous data file to compare against')
    parser.add_argument('--format',
                        metavar='<report format>',
                        help='form of report (html, text, or csv)',
                        choices=['html', 'text', 'csv'],
                        default='html')
    parser.add_argument('--columns',
                        metavar='<column widths>',
                        help='column widths for format=text, default: ' +
                             DEFAULT_COLUMN_WIDTHS,
                        default=DEFAULT_COLUMN_WIDTHS)
    parser.add_argument('--breeze_creds',
                        metavar='<Breeze credential file>',
                        help='file with Breeze credentials if not standard',
                        default=None)
    parser.add_argument('--email_creds',
                        metavar='<email credential file>',
                        help='file with email passwords if not standard')
    parser.add_argument('--email_servers',
                        metavar='<email domain specification file>',
                        help='file with email domain configuration if not standard')
    parser.add_argument('--replay',
                        help='send differences between last two snapshots',
                        default=False,
                        action='store_true')
    parser.add_argument('--list_directories',
                        default=False,
                        action='store_true',
                        help='list data and configuration directories and exit')
    parser.add_argument('--initialize',
                        default=False,
                        action='store_true',
                        help="initialize from Breeze before first use "
                             "without sending report")

    args = parser.parse_args()

    if args.list_directories:
        # Making it easy to note where users should look for files on this platform.
        print('Default directory where email_profile_report '
              f'stores historical data: {DEFAULT_DATA_DIR}')
        print(f'User configuration directory: {platformdirs.user_config_dir()}')
        print(f'Site configuration directory: {platformdirs.site_config_dir()}')
        sys.exit(0)

    if args.initialize:
        _verify_directory(args)
        # Create first-time reference data to prevent monster first report
        current_data = ProfileFromBreeze(args, breeze_api)
        current_data.save_data()
        print(f'Initial data saved to {current_data.save_file_name}')
        sys.exit(0)

    if not args.sender:
        sys.exit('--from=sender is required')

    if not args.to and not args.bcc:
        sys.exit('Either -t or -b is required')

    _verify_directory(args)

    results = _generate_diffs(args, breeze_api)

    widths = [int(w) for w in args.columns.split(',')]
    names = ['Field', 'Old', 'New']
    column_specs = [ColSpec(names[i], width=widths[i]) for i in range(3)]
    msg = MIMEMultipart()
    msg['Subject'] = 'Breeze profile change report'
    if args.to:
        msg['To'] = args.to
    if args.bcc:
        msg['Bcc'] = args.bcc
    diffs = results.get_diffs()
    if diffs:
        msg.attach(MIMEText(f'Breeze changes for {results.header}'))
        if args.format == 'html':
            formatter = _HTMLFormatter(column_specs)
        elif args.format == 'csv':
            formatter = _CSVFormatter(column_specs)
        else:
            args.format = 'plain'
            formatter = _TextFormatter(column_specs)
        output = StringIO()
        formatter.format_table(diffs, output)
        output.seek(0)
        txt = output.read()
        if args.format == 'csv':
            part = MIMEText(txt, 'csv', 'utf-8')
            # part.set_payload(txt)
            part.add_header('Content-Disposition',
                            "attachment; filename=profile_changes.csv")
            msg.attach(part)
        else:
            msg.attach(MIMEText(txt, args.format))
    else:
        msg.attach(MIMEText(f'No changes found between {results.header}'))

    sender = email_sender if email_sender else \
        create_sender(args.sender,
                      creds_file=args.email_creds,
                      overrides=args.email_servers)
    sender.send_message(msg)

    results.save_data()


if __name__ == "__main__":
    main()
