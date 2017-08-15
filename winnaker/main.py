# -*- coding: utf-8 -*-
import argparse
import logging
import os
import sys
from winnaker.models import *
from winnaker.notify import *
from selenium import webdriver
import pkg_resources  # part of setuptools
import atexit
from datetime import datetime
from winnaker.settings import *


def main():
    print ("""
____    __    ____  __  .__   __. .__   __.      ___       __  ___  _______ .______
\   \  /  \  /   / |  | |  \ |  | |  \ |  |     /   \     |  |/  / |   ____||   _  \\
 \   \/    \/   /  |  | |   \|  | |   \|  |    /  ^  \    |  '  /  |  |__   |  |_)  |
  \            /   |  | |  . `  | |  . `  |   /  /_\  \   |    <   |   __|  |      /
   \    /\    /    |  | |  |\   | |  |\   |  /  _____  \  |  .  \  |  |____ |  |\  \----.
    \__/  \__/     |__| |__| \__| |__| \__| /__/     \__\ |__|\__\ |_______|| _| `._____|

    """)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--start",
        help="starts manual execution of the pipline",
        action="store_true")
    parser.add_argument(
        "-fb",
        "--forcebake",
        help="force bake, to be used wth --start ",
        action="store_true")
    parser.add_argument(
        "-a",
        "--app",
        type=str,
        help="the name of application to look for",
        default=cfg_app_name)
    parser.add_argument(
        "-p",
        "--pipeline",
        type=str,
        help="the name of pipline to test",
        default=os.environ["WINNAKER_PIPELINE_NAME"])
    parser.add_argument(
        "-nl", "--nologin",
        help="will not attempt to login",
        action="store_true")
    parser.add_argument(
        "-oa", "--authorize",
        help="authorize the oauth application with the logged in user if required. " +
            "This argument and '--nologin' are mutually exclusive",
        action="store_true"
    )
    parser.add_argument(
        "-nlb",
        "--nolastbuild",
        help="will not attempt to check last build status or stages",
        action="store_true")
    parser.add_argument(
        "-hl",
        "--headless",
        help="will run in an xfvb display ",
        action="store_true")
    parser.add_argument(
        "-v",
        "--verbose",
        help="print more logs, DEBUG level",
        action="store_true")
    args = parser.parse_args()

    # Logging setup
    if args.verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    logFormatter = logging.Formatter(
        "%(asctime)s [%(levelname)s]  %(message)s")
    rootLogger = logging.getLogger()
    rootLogger.setLevel(log_level)

    fileHandler = logging.FileHandler(
        join(cfg_output_files_path, "winnaker.log"))
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)

    version = pkg_resources.require("winnaker")[0].version
    logging.info("Winnaker Version: {}".format(version))
    logging.info("Current Config: {}".format(args))

    if not os.path.exists(cfg_output_files_path):
        os.makedirs(cfg_output_files_path)

    if cfg_email_smtp and cfg_email_to and cfg_email_from:
        atexit.register(send_mail, cfg_email_from, cfg_email_to, "Winnaker Screenshots " +
                        str(datetime.utcnow()), "Here are the screenshots of the spinnaker's last run at " +
                        str(datetime.utcnow()) +
                        " UTC Time", server=cfg_email_smtp)

    if args.headless:
        logging.debug("Starting virtual display")
        from pyvirtualdisplay import Display
        display = Display(visible=0, size=(2560, 1440))
        display.start()
        logging.debug("Started virtual display")

    s = Spinnaker()
    if not args.nologin:
        logging.debug("Starting login")
        s.login()
        if args.authorize: s.authorize()

    s.get_pipeline(args.app, args.pipeline)
    if not args.nolastbuild:
        logging.info(
            "- Last build status: {}".format(s.get_last_build().status.encode('utf-8')))
        logging.info("- Screenshot Stages")
        logging.info("- Current working directory: {}".format(os.getcwd()))
        s.get_stages()

    if args.start:
        logging.debug("Going into start block")
        s.start_manual_execution(force_bake=args.forcebake)

    if args.headless:
        logging.debug("Stopping virtualdisplay")
        display.stop()
        logging.debug("virtualdisplay stopped")


if __name__ == "__main__":
    main()
