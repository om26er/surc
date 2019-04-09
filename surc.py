#!/usr/bin/env python3

import os
import subprocess
import shlex

import requests
import yaml

from database.db_controller import DBController


def sanitize_name(name):
    if '-' in name:
        return ' '.join([name.capitalize() for name in name.split('-')]).strip()
    return name.capitalize()


def send_email_and_create_pull_request(config, name, version, snap_source):
    name = sanitize_name(name)
    email_text = "Version {} of {} is available, please update.\n\nsource: {}".format(version, name, snap_source)
    response = requests.post(
        'https://api.mailgun.net/v3/{}/messages'.format(config['MAILGUN_DOMAIN']),
        auth=('api', config['MAILGUN_API_KEY']),
        data={'from': 'Update Checker <surc@{}>'.format(config['MAILGUN_DOMAIN']),
              "to": config['recipients'],
              "subject": "{} {} Available".format(name, version),
              "text": email_text}
    )
    print(response, response.status_code, response.json())


def check_if_update_available(name, scriptlet, *scriptlet_args):
    command = 'scriptlets/{}'.format(scriptlet)
    command = command + " " + ' '.join(scriptlet_args)
    result = subprocess.check_output(shlex.split(command), universal_newlines=True).strip()
    return DBController.compare(name=name, version=result), result


def main():
    with open('config.yaml') as file:
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
            print("Unsupported type={} provided, skipping....".format(type_))
            continue

        if not update_available:
            send_email_and_create_pull_request(config['mailing'], name, version, snap)


if __name__ == '__main__':
    main()
