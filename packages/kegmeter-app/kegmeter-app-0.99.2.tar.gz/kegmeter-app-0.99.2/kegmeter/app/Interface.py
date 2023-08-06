import base64
import logging
import md5
import os
from PIL import Image, ImageTk
import pkg_resources
import re
import requests
from StringIO import StringIO
import threading
import time
import Tkinter
import ttk

from kegmeter.common import Config, Beer, Checkin, DBClient

mysterybeer_file = pkg_resources.resource_filename(__name__, "images/mysterybeer.png")
pbu_file = pkg_resources.resource_filename(__name__, "images/pbu_40_grey.png")
highlight_color = "#ffff6f"

class ImageLabel(object):
    def __init__(self, *args, **kwargs):
        self.label = Tkinter.Label(*args, **kwargs)

    def pack(self, *args, **kwargs):
        self.label.pack(*args, **kwargs)

    def load_from_url(self, url, size=None):
        logging.debug("loading image from URL: {}".format(url))

        try:
            imgreq = requests.get(url)
            imgreq.raise_for_status()

            pil_image = Image.open(StringIO(imgreq.content))
            if size is not None:
                pil_image.thumbnail(size, Image.ANTIALIAS)

            self.image = ImageTk.PhotoImage(pil_image)
            self.label.config(image=self.image)

        except Exception as e:
            logging.error("Couldn't load image: {}".format(e))


class TapDisplay(object):
    def __init__(self, tap_id, parent):
        self.tap_id = tap_id

        self.beer_id = None
        self.active = False

        self.frame = Tkinter.Frame(parent, borderwidth=1, relief=Tkinter.GROOVE)
        self.frame.pack(side=Tkinter.LEFT, expand=True, fill=Tkinter.BOTH, pady=10, padx=5)
        self.frame.pack_propagate(0)

        # From top down
        self.beer_name = Tkinter.Label(self.frame, text="<beer name>", font=("PT Sans", 24, "bold"))
        self.beer_name.pack(pady=(30, 0))

        self.beer_style = Tkinter.Label(self.frame, text="<beer style>", font=("PT Sans", 17))
        self.beer_style.pack()

        self.images = Tkinter.Frame(self.frame, pady=50)
        self.images.pack()

        self.brewery_image = ImageLabel(self.images, background="#dfdfdf", height=100, width=100)
        self.brewery_image.pack(side=Tkinter.LEFT, padx=10)

        self.beer_image = ImageLabel(self.images, background="#dfdfdf", height=100, width=100)
        self.beer_image.pack(side=Tkinter.LEFT, padx=10)

        # From bottom up
        self.tap_num = Tkinter.Label(self.frame, text=tap_id, background="#efefef", font=("PT Sans", 16, "bold"))
        self.tap_num.pack(side=Tkinter.BOTTOM, fill=Tkinter.X)

        self.pct_full_meter = ttk.Progressbar(self.frame, maximum=1.0)
        self.pct_full_meter.pack(side=Tkinter.BOTTOM, fill=Tkinter.X, padx=10, pady=20)

        self.abv = Tkinter.Label(self.frame, text="0.0%", font=("PT Sans", 20, "bold"), pady=10)
        self.abv.pack(side=Tkinter.BOTTOM)

        self.brewery_loc = Tkinter.Label(self.frame, text="<brewery location>", font=("PT Sans", 14))
        self.brewery_loc.pack(side=Tkinter.BOTTOM)

        self.brewery_name = Tkinter.Label(self.frame, text="<brewery name>", font=("PT Sans", 18, "bold"))
        self.brewery_name.pack(side=Tkinter.BOTTOM)

        # Description or amount poured gets remaining space in between
        self.beer_description = Tkinter.Text(self.frame, font=("PT Sans", 12), borderwidth=0, wrap=Tkinter.WORD, pady=20)
        self.beer_description.pack(expand=True, fill=Tkinter.BOTH, padx=10)
        self.beer_description.tag_config("description", justify=Tkinter.CENTER)

        self.amount_poured_frame = Tkinter.Frame(self.frame, pady=20, background=highlight_color)
        self.amount_poured_number = Tkinter.Label(self.amount_poured_frame, font=("PT Sans", 36, "bold"), background=highlight_color)
        self.amount_poured_number.pack(side=Tkinter.LEFT, anchor=Tkinter.NW)
        self.amount_poured_text = Tkinter.Label(self.amount_poured_frame, font=("PT Sans", 36), background=highlight_color, text=" ounces poured")
        self.amount_poured_text.pack(side=Tkinter.LEFT, anchor=Tkinter.NW)

    def update(self, tap):
        self.pct_full_meter.config(value=tap["pct_full"])

        if tap["beer_id"] == self.beer_id:
            return

        try:
            beer = Beer.new_from_id(tap["beer_id"])
        except Exception as e:
            logging.error("Couldn't look up beer ID {}: {}".format(tap["beer_id"], e))
            return

        self.beer = beer

        self.beer_name.config(text=beer.beer_name)
        self.beer_style.config(text=beer.beer_style)
        self.brewery_name.config(text=beer.brewery_name)
        self.brewery_loc.config(text=beer.brewery_loc)
        self.abv.config(text="{}%".format(beer.abv))

        self.beer_description.delete(1.0, Tkinter.END)
        self.beer_description.insert(Tkinter.END, self.beer.description, "description")

        self.brewery_image.load_from_url(beer.brewery_label, (100, 100))
        self.beer_image.load_from_url(beer.beer_label, (100, 100))

        self.beer_id = tap["beer_id"]

    def update_active_tap(self, tap):
        self.amount_poured = tap.pulses * Config.get("units_per_pulse")
        self.amount_poured_number.config(text="{:.2f}".format(self.amount_poured))

        if self.active:
            return

        logging.debug("making tap {} active".format(self.tap_id))
        self.active = True

        self.beer_description.pack_forget()
        self.amount_poured_frame.pack(expand=True, fill=Tkinter.Y)

        for obj in ["frame", "beer_name", "beer_style", "images", "beer_description", "brewery_name", "brewery_loc", "abv"]:
            getattr(self, obj).config(background=highlight_color)

        self.tap_num.config(background="#dfdf4f")

    def make_inactive(self):
        if not self.active:
            return

        logging.debug("making tap {} inactive".format(self.tap_id))
        self.active = False
        self.amount_poured = None
        self.set_description()

        self.amount_poured_frame.pack_forget()
        self.beer_description.pack(expand=True, fill=Tkinter.BOTH, padx=10)

        for obj in ["frame", "beer_name", "beer_style", "images", "beer_description", "brewery_name", "brewery_loc", "abv"]:
            getattr(self, obj).config(background="White")

        self.tap_num.config(background="#efefef")

class CheckinDisplay(object):
    def __init__(self, parent):
        self.checkin_id = None
        self.time_since = None

        self.frame = Tkinter.Frame(parent, borderwidth=1, relief=Tkinter.GROOVE)
        self.frame.pack(side=Tkinter.LEFT, expand=True, fill=Tkinter.BOTH, padx=5, pady=10)
        self.frame.pack_propagate(1)

        self.avatar_image = ImageLabel(self.frame, height=100, width=100, borderwidth=1, relief=Tkinter.GROOVE)
        self.avatar_image.pack(side=Tkinter.LEFT, pady=5, padx=5)

        self.description_frame = Tkinter.Frame(self.frame)
        self.description_frame.pack(side=Tkinter.LEFT, expand=True, fill=Tkinter.BOTH, padx=5, pady=10)
        self.description_frame.pack_propagate(0)

        self.description = Tkinter.Text(self.description_frame, font=("PT Sans", 11), borderwidth=0, wrap=Tkinter.WORD)
        self.description.pack(fill=Tkinter.BOTH)
        self.description.tag_config("b", font=("PT Sans", 11, "bold"))
        self.description.tag_config("i", font=("PT Sans", 11, "italic"))

    def update(self, checkin):
        if checkin.checkin_id == self.checkin_id and checkin.time_since == self.time_since:
            return

        if checkin.checkin_id != self.checkin_id:
            self.avatar_image.load_from_url(checkin.user_avatar, (100, 100))

        self.checkin_id = checkin.checkin_id
        self.time_since = checkin.time_since

        self.description.delete(1.0, Tkinter.END)
        self.description.insert(Tkinter.END, checkin.user_name, "b")
        self.description.insert(Tkinter.END, " enjoyed a ")
        self.description.insert(Tkinter.END, checkin.beer.beer_name, "b")
        self.description.insert(Tkinter.END, " by ")
        self.description.insert(Tkinter.END, checkin.beer.brewery_name, "b")
        self.description.insert(Tkinter.END, "\n")
        self.description.insert(Tkinter.END, checkin.time_since, "i")


class KegMeter(object):
    def __init__(self, kegmeter_status):
        self.kegmeter_status = kegmeter_status
        self.checkins = None

    def initialize_window(self):
        self.window = Tkinter.Tk()
        self.window.attributes("-fullscreen", True)
        self.window.tk_setPalette(background="White")
        self.window.rowconfigure(1, weight=1)

        self.title = Tkinter.Label(text="On Tap", font=("PT Sans", 32, "bold"), background="#cfcfcf", borderwidth=1, relief=Tkinter.GROOVE)
        self.title.pack(fill=Tkinter.X)

        # Taps
        self.tap_container = Tkinter.Frame(background="#dfdfdf", padx=10)
        self.tap_container.pack(expand=True, fill=Tkinter.BOTH)

        self.taps = dict()
        for i, tap in enumerate(DBClient.get_taps()):
            self.taps[tap["tap_id"]] = TapDisplay(tap["tap_id"], self.tap_container)

        # Checkins
        self.checkin_container = Tkinter.Frame(background="#dfe7ef", borderwidth=1, relief="sunken")
        self.checkin_container.pack(fill=Tkinter.X)

        self.checkin_displays = []
        for i in range(Config.get("num_checkins")):
            self.checkin_displays.append(CheckinDisplay(self.checkin_container))

        self.powered_image_pil = Image.open(pbu_file)
        self.powered_image = ImageTk.PhotoImage(self.powered_image_pil)
        self.powered_image_container = Tkinter.Label(self.checkin_container, height=40, width=166, image=self.powered_image, background="#dfe7ef")
        self.powered_image_container.pack(side=Tkinter.RIGHT, padx=10)

    def update_active_taps(self):
        for tap in self.kegmeter_status.tap_statuses.values():
            if tap.is_active():
                self.taps[tap.tap_id].update_active_tap(tap)
            else:
                self.taps[tap.tap_id].make_inactive()

    def update_tap_info(self):
        for tap in DBClient.get_taps():
             self.taps[tap["tap_id"]].update(tap)

    def update_checkin_display(self):
        if self.checkins is not None:
            for checkin, display in zip(self.checkins, self.checkin_displays):
                display.update(checkin)

    def update_checkins(self):
        self.checkins = Checkin.get_latest()

    def repeat_call(self, interval, target):
        target()
        thread = threading.Timer(interval, self.repeat_call, [interval, target])
        thread.start()

    def main(self):
        self.initialize_window()

        self.repeat_call(60.0, self.update_tap_info)
        self.repeat_call(120.0, self.update_checkins)
        self.repeat_call(15.0, self.update_checkin_display)

        self.listener = threading.Thread(target=self.update_listener)
        self.listener.daemon = True
        self.listener.start()

        Tkinter.mainloop()

    def shutdown(self):
        logging.error("Interface exiting")
        self.window.quit()

    def update_listener(self):
        while not self.kegmeter_status.interrupt_event.is_set():
            self.kegmeter_status.tap_update_event.wait()
            self.kegmeter_status.tap_update_event.clear()
            self.update_active_taps()

        self.shutdown()
