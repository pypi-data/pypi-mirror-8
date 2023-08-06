#!/usr/bin/env python3

From PopupBubble.PopupTk import poptk
import argparse

parser = argparse.ArgumentParser(description="Popup notification on the commandline")
parser.add_argument("message", help="Message in the popup")
parser.add_argument("--title", "-t", help="Title of the popup", default="Notification")
parser.add_argument("--duration", "-d", help="How many seconds must the popup be there?", default=3, type=int)
args = parser.parse_args()
poptk(args.title, args.message, args.duration)
