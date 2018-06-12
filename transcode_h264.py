import os
import gi
import sys
import time
import datetime

gi.require_version('Gtk', '3.0')

gi.require_version('Gst', '1.0')

from gi.repository import Gst, GObject, Gtk

ARRAY = []
with open('timestamps123.txt') as my_file:
    for line in my_file:
        ARRAY.append(line)

def setup_probe(element):
    pad = element.get_static_pad("video_sink")
    pad.add_probe(Gst.PadProbeType.BUFFER, callback, ARRAY)

def callback(pad, info, data):
    element = pad.get_parent_element()
    element.set_property("text", data[0])
    data.pop(0)
    return Gst.PadProbeReturn.OK

Gtk.init(sys.argv)

# initialize GStreamer
Gst.init(sys.argv)

# pipeline = Gst.parse_launch("filesrc location=video ! rtph264depay ! h264parse  ! mp4mux ! filesink location=test1.avi")
pipeline = Gst.parse_launch("filesrc location=video ! decodebin ! videoconvert ! textoverlay name=textoverlay ! avimux ! filesink location=test1.avi")
# pad = sink.get_static_pad("sink")
# pipeline = Gst.parse_launch("filesrc location=video ! decodebin ! videoconvert ! videoscale ! textoverlay name=textoverlay ! avimux ! filesink location=test1.avi")
textoverlay = pipeline.get_by_name('textoverlay')
setup_probe(textoverlay)

pipeline.set_state(Gst.State.PLAYING)
time.sleep(60)
pipeline.set_state(Gst.State.NULL)