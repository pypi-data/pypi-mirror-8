#!/usr/bin/env python

import argparse
import logging
import signal
import sys
import threading
import time

from kegmeter.app import KegMeter, SerialListener
from kegmeter.common import Config, KegmeterStatus

def run_app():
    parser = argparse.ArgumentParser()

    parser.add_argument("--base-dir", dest="base_dir",
                        help="Specify base directory.")
    parser.add_argument("--no-interface", dest="no_interface", action="store_true",
                        help="Do not run interface.")
    parser.add_argument("--no-serial", dest="no_serial", action="store_true",
                        help="Do not run serial port listener.")
    parser.add_argument("--debug", dest="debug", action="store_true",
                        help="Display debugging information.")
    parser.add_argument("--logfile", dest="logfile",
                        help="Output to log file instead of STDOUT.")

    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.logfile:
        logging.basicConfig(filename=args.logfile)

    if args.base_dir:
        Config.base_dir = args.base_dir

    status = KegmeterStatus()

    signal.signal(signal.SIGINT, status.interrupt)

    if not args.no_interface:
        interface = KegMeter(status)
        interface_thread = threading.Thread(target=interface.main)
        interface_thread.daemon = True
        interface_thread.start()

    if not args.no_serial:
        try:
            listener = SerialListener(status)
            listener_thread = threading.Thread(target=listener.listen)
            listener_thread.daemon = True
            listener_thread.start()
        except IOError:
            logging.error("Couldn't find serial device. Skipping.")
            args.no_serial = True

    status.tap_update_event.set()

    try:
        while not status.interrupt_event.is_set():
            time.sleep(0.1)
    except KeyboardInterrupt:
        status.interrupt()
    except:
        raise

    if not args.no_interface:
        interface_thread.join()

    if not args.no_serial:
        listener_thread.join()


if __name__ == "__main__":
    run_app()
