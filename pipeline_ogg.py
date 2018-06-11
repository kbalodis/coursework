import os
import gi
import sys
import time
import datetime

gi.require_version('Gtk', '3.0')

gi.require_version('Gst', '1.0')

from gi.repository import Gst, GObject, Gtk

FILE = open("timestamps.txt", "a")

def setup_probe(element):
    pad = element.get_static_pad("sink")
    pad.add_probe(Gst.PadProbeType.BUFFER, callback, None)

def callback(pad, info, data):
    FILE.write(str(datetime.datetime.now())+'\n')
    return Gst.PadProbeReturn.OK

Gtk.init(sys.argv)

# initialize GStreamer
Gst.init(sys.argv)

pipeline = Gst.Pipeline.new("player")

src = Gst.ElementFactory.make("v4l2src", "src")
# src.set_property("device", "/dev/vidoe0")
pipeline.add(src)

videoconvert = Gst.ElementFactory.make("videoconvert", None)
pipeline.add(videoconvert)

videoscale = Gst.ElementFactory.make("videoscale", None)
pipeline.add(videoscale)

caps = Gst.Caps.from_string("video/x-raw, width=320, height=240, framerate=15/1")
camerafilter = Gst.ElementFactory.make("capsfilter", "filter") 
camerafilter.set_property("caps", caps)
pipeline.add(camerafilter)

theoraenc = Gst.ElementFactory.make("theoraenc", None)
pipeline.add(theoraenc)

ogg = Gst.ElementFactory.make("oggmux", None)
pipeline.add(ogg)

# decode = Gst.ElementFactory.make("decodebin", "decode")

sink = Gst.ElementFactory.make("filesink", "filesink")
sink.set_property("location", "video.ogg")
pipeline.add(sink)

setup_probe(sink)

# pad = sink.get_static_pad("sink")

# pipeline.add(src)

# pipeline.add(decode)

src.link(videoconvert)
# camerafilter.link(videoconvert)
videoconvert.link(videoscale)
videoscale.link(theoraenc)
theoraenc.link(ogg)
ogg.link(sink)

# decode.link(sink)

pipeline.set_state(Gst.State.PLAYING)
time.sleep(15)
pipeline.send_event(Gst.Event.new_eos())
time.sleep(5)
pipeline.set_state(Gst.State.NULL)

FILE.close()