Snap Upstream Release Checker is an automation tool to check if there is new update for a software that
is published as a snap but is not integrated into the upstream's automated release process.

This will notify people maintaining snaps to push a new update, so users always enjoy the latest and greatest.

## Installation
```bash
snap install surc
```

You also need to download and place the config file in your $HOME directory
https://raw.githubusercontent.com/om26er/surc/master/surc-conf.yaml

The config file requires a working MailGun account (for now), SMTP support is coming.

To run, just use the command line entry point

```bash
om26er@Intel-NUC-PC:~/code/ubuntu$ surc
No update available for android-studio
No update available for sublime-text
No update available for pyside2
No update available for crossbar
```

You probably want to setup a cron job that checks everyday if new updates are available.
