from surc.db_controller import DBController
from surc.scriplets import AndroidStudioStable, SublimeTextStable


SCRIPTLETS = [AndroidStudioStable, SublimeTextStable]


def check_updates_and_notify():
    for ScriptletClass in SCRIPTLETS:
        scriptlet = ScriptletClass()
        update_available = DBController.compare(name=scriptlet.name, version=scriptlet.get_latest())
        if update_available:
            print("Time to send that email and create the PR...")
        else:
            print("No update available for {}".format(scriptlet.name))


if __name__ == '__main__':
    check_updates_and_notify()
