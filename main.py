import importlib

import yaml

from database.db_controller import DBController


def main():
    with open('config.yaml') as file:
        scriptlets = yaml.load(file)
    for scriptlet in scriptlets:
        name, source = tuple(scriptlet.values())
        module = importlib.import_module('.{}'.format(name.replace('-', '_')), 'scriptlets')
        update_available = DBController.compare(name=name, version=module.main())
        if update_available:
            print("Time to send that email and create the PR...")
        else:
            print("No update available for {}".format(name))


if __name__ == '__main__':
    main()
