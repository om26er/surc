import subprocess

import yaml

from database.db_controller import DBController


def main():
    with open('config.yaml') as file:
        scriptlets = yaml.load(file)
    for scriptlet in scriptlets:
        name, source = tuple(scriptlet.values())
        script_name = name.replace('-', '_')
        result = subprocess.check_output(['scriptlets/{}'.format(script_name)], universal_newlines=True).strip()
        update_available = DBController.compare(name=name, version=result)
        if update_available:
            print("Time to send that email and create the PR...")
        else:
            print("No update available for {}".format(name))


if __name__ == '__main__':
    main()
