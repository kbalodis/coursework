import os
import gi
import sys
import time
import datetime

gi.require_version('Gtk', '3.0')

gi.require_version('Gst', '1.0')

from gi.repository import Gst, GObject, Gtk

ARRAY = []
with open('timestamps.txt') as my_file:
    for line in my_file:
        ARRAY.append(line)

print ARRAY

def setup_probe(element):
    pad = element.get_static_pad("video_sink")
    pad.add_probe(Gst.PadProbeType.BUFFER, callback, ARRAY)

def callback(pad, info, data):
    element = pad.get_parent_element()
    print(data)
    element.set_property("text", data[0])
    data.pop(0)
    return Gst.PadProbeReturn.OK

Gtk.init(sys.argv)

# initialize GStreamer
Gst.init(sys.argv)

# pipeline = Gst.Pipeline.new("player")

# src = Gst.ElementFactory.make("filesrc", "src")
# src.set_property("location", "video.ogg")
# pipeline.add(src)

# decode = Gst.ElementFactory.make("decodebin", "decode")
# pipeline.add(decode)

# videoconvert = Gst.ElementFactory.make("videoconvert", None)
# pipeline.add(videoconvert)

# videoscale = Gst.ElementFactory.make("videoscale", None)
# pipeline.add(videoscale)

# textoverlay = Gst.ElementFactory.make("textoverlay", "text")
# textoverlay.set_property("text", "yesssss")
# pipeline.add(textoverlay)
# setup_probe(textoverlay)

# avimux = Gst.ElementFactory.make("avimux", None)
# pipeline.add(avimux)

# sink = Gst.ElementFactory.make("filesink", "filesink")
# sink.set_property("location", "timestamp.avi")
# pipeline.add(sink)
# # ! theoradec ! ffmpegcolorspace ! autovideosink 

# src.link(decode)
# decode.link(videoconvert)
# videoconvert.link(videoscale)
# videoscale.link(textoverlay)
# textoverlay.link(avimux)
# avimux.link(sink)

pipeline = Gst.parse_launch("filesrc location=video.ogg ! decodebin ! videoconvert ! videoscale ! textoverlay name=textoverlay ! avimux ! filesink location=test.avi")
# pad = sink.get_static_pad("sink")
textoverlay = pipeline.get_by_name('textoverlay')
setup_probe(textoverlay)

# pipeline.add(src)

# pipeline.add(decode)

# src.link(videoconvert)
# videoconvert.link(videoscale)
# videoscale.link(theoraenc)
# # camerafilter.link(theoraenc)
# theoraenc.link(ogg)
# ogg.link(sink)

# decode.link(sink)

# pipeline.set_state(Gst.State.NULL)

# pipeline.set_state(Gst.State.PAUSED)

pipeline.set_state(Gst.State.PLAYING)
time.sleep(30)
pipeline.set_state(Gst.State.NULL)