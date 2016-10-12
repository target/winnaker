# -*- coding: utf-8 -*-
import argparse
from models import *
from selenium import webdriver




if __name__ == "__main__":

    print ("""
____    __    ____  __  .__   __. .__   __.      ___       __  ___  _______ .______
\   \  /  \  /   / |  | |  \ |  | |  \ |  |     /   \     |  |/  / |   ____||   _  \
 \   \/    \/   /  |  | |   \|  | |   \|  |    /  ^  \    |  '  /  |  |__   |  |_)  |
  \            /   |  | |  . `  | |  . `  |   /  /_\  \   |    <   |   __|  |      /
   \    /\    /    |  | |  |\   | |  |\   |  /  _____  \  |  .  \  |  |____ |  |\  \----.
    \__/  \__/     |__| |__| \__| |__| \__| /__/     \__\ |__|\__\ |_______|| _| `._____|

    """)

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--start", help="starts manual execution of the pipline",
                        action="store_true")
    parser.add_argument("-fb", "--forcebake", help="force bake, to be used wth --start ",
                        action="store_true")
    parser.add_argument("-a", "--app", type=str,
                        help="the name of application to look for", default=os.environ["WINNAKER_APP_NAME"])
    parser.add_argument("-p", "--pipeline", type=str,
                        help="the name of pipline to test", default=os.environ["WINNAKER_PIPELINE_NAME"])
    parser.add_argument("-nl", "--nologin",
                        help="will not attempt to login", action="store_true")
    parser.add_argument(
        "-hl", "--headless",  help="will run in an xfvb display ", action="store_true")


    args = parser.parse_args()

    if args.headless:
        from pyvirtualdisplay import Display
        display = Display(visible=0, size=(2560, 1440))
        display.start()

    s = Spinnaker()
    if not args.nologin:
        s.login()
    s.get_pipeline(args.app, args.pipeline)
    print ("- Last build status "+s.get_last_build().status.encode('utf-8'))
    print ("- Screenshot Stages")
    s.get_stages()

    if args.start:
        s.start_manual_execution(force_bake=args.forcebake)

    if args.headless:
        display.stop()
