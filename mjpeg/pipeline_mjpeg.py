import os
import gi
import sys
import time
import datetime

gi.require_version('Gtk', '3.0')

gi.require_version('Gst', '1.0')

from gi.repository import Gst, GObject, Gtk

# FILE = open("timestamps123.txt", "a")

def setup_probe(element):
    pad = element.get_static_pad("sink")
    pad.add_probe(Gst.PadProbeType.BUFFER, callback, None)

def callback(pad, info, data):
    print datetime.datetime.now()
    return Gst.PadProbeReturn.OK

Gtk.init(sys.argv)

# initialize GStreamer
Gst.init(sys.argv)

pipeline = Gst.Pipeline.new("player")

src = Gst.ElementFactory.make("v4l2src", "src")
# src.set_property("num-buffers", 100)
src.set_property("device", "/dev/video1")
pipeline.add(src)

videoconvert = Gst.ElementFactory.make("videoconvert", None)
pipeline.add(videoconvert)

# videoscale = Gst.ElementFactory.make("videoscale", None)
# pipeline.add(videoscale)

caps = Gst.Caps.from_string("video/x-raw, format=YUY2, width=320, height=240, framerate=10/1")
camerafilter = Gst.ElementFactory.make("capsfilter", "filter") 
camerafilter.set_property("caps", caps)
pipeline.add(camerafilter)

# videoconvert = Gst.ELementFactory.make("videocovnert", None)
# pipeline.add(videoconvert)

# h264parse = Gst.ElementFactory.make("h264parse", None)
# pipeline.add(h264parse)

jpegenc = Gst.ElementFactory.make("jpegenc", None)
# x264enc.set_property("tune", "zerolatency")
pipeline.add(jpegenc)

# rtph264pay = Gst.ElementFactory.make("rtph264pay", None)
# pipeline.add(rtph264pay)

# decode = Gst.ElementFactory.make("decodebin", "decode")
matroskamux = Gst.ElementFactory.make("matroskamux", None)
pipeline.add(matroskamux)

sink = Gst.ElementFactory.make("filesink", "filesink")
sink.set_property("location", "video")
sink.set_property("sync", "false")
pipeline.add(sink)

setup_probe(sink)

# pad = sink.get_static_pad("sink")

# pipeline.add(src)

# pipeline.add(decode)

src.link(camerafilter)
camerafilter.link(videoconvert)
videoconvert.link(jpegenc)
# h264parse.link(matroskamux)
jpegenc.link(matroskamux)
# x264enc.link(rtph264pay)
# rtph264pay.link(sink)
# h264parse.link(matroskamux)
matroskamux.link(sink)

# decode.link(sink)

pipeline.set_state(Gst.State.PLAYING)
time.sleep(15)
pipeline.send_event(Gst.Event.new_eos())
time.sleep(2)
pipeline.set_state(Gst.State.NULL)
