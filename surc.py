#!/usr/bin/env python3

import os
import subprocess
import shlex
import sys

import requests
import yaml

from database.db_controller import DBController


def is_snap():
    return os.environ.get('SNAP_NAME') == 'surc'


def sanitize_name(name):
    if '-' in name:
        return ' '.join([name.capitalize() for name in name.split('-')]).strip()
    return name.capitalize()


def send_email_and_create_pull_request(config, name, version, snap_source):
    name = sanitize_name(name)
    email_text = "Version {} of {} is available, please update.\n\nsource: {}".format(version, name, snap_source)
    requests.post(
        'https://api.mailgun.net/v3/{}/messages'.format(config['MAILGUN_DOMAIN']),
        auth=('api', config['MAILGUN_API_KEY']),
        data={'from': 'Update Checker <surc@{}>'.format(config['MAILGUN_DOMAIN']),
              "to": config['recipients'],
              "subject": "{} {} Available".format(name, version),
              "text": email_text}
    )


def check_if_update_available(name, scriptlet, *scriptlet_args):
    command = 'scriptlets/{}'.format(scriptlet)
    if is_snap():
        command = os.path.join(os.path.expandvars('$SNAP'), command)
    command = command + " " + ' '.join(scriptlet_args)
    result = subprocess.check_output(shlex.split(command), universal_newlines=True).strip()
    return DBController.compare(name=name, version=result), result


def main():
    filename = 'surc-conf.yaml'
    # If we are running from within a snap, find real $HOME
    if is_snap():
        home_dir = subprocess.check_output(shlex.split('perl -we "print((getpwuid $>)[7])"'), universal_newlines=True)
        file_in_home = os.path.join(home_dir, filename)
    else:
        file_in_home = os.path.expandvars('$HOME/{}'.format(filename))

    if os.path.exists(file_in_home):
        config_file = file_in_home
    elif os.path.exists(filename):
        config_file = filename
    else:
        print("Config file not found, exiting")
        sys.exit(1)

    with open(config_file) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    # FIXME: validate config data
    for project in config['projects']:
        name, snap, type_ = tuple(project.values())
        if type_ == 'scriptlet':
            scriptlet = name.replace('-', '_')
            update_available, version = check_if_update_available(name, scriptlet)
        elif type_ == 'pypi':
            update_available, version = check_if_update_available(name, type_, name)
        else:
            print("Unsupported type={} provided, skipping".format(type_))
            continue

        if update_available:
            send_email_and_create_pull_request(config['mailing'], name, version, snap)
        else:
            print("No update available for {}".format(name))


if __name__ == '__main__':
    main()
