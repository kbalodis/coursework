import os
import gi
import sys
import time
import datetime

gi.require_version('Gtk', '3.0')

gi.require_version('Gst', '1.0')

from gi.repository import Gst, GObject, Gtk

COUNTER = 0

def setup_probe(element):
    pad = element.get_static_pad("text_sink")
    pad.add_probe(Gst.PadProbeType.BUFFER, callback, None)

def callback(pad, info, data):
    print(pad.get_current_caps(), pad.get_parent_element())
    return Gst.PadProbeReturn.OK

Gtk.init(sys.argv)

# initialize GStreamer
Gst.init(sys.argv)

pipeline = Gst.Pipeline.new("player")

src = Gst.ElementFactory.make("filesrc", "src")
src.set_property("location", "video.ogg")
pipeline.add(src)

oggdemux = Gst.ElementFactory.make("oggdemux", "decode")
pipeline.add(oggdemux)

theoradec = Gst.ElementFactory.make("theoradec", None)
pipeline.add(theoradec)

avenc_mpeg4 = Gst.ElementFactory.make("avenc_mpeg4", None)
pipeline.add(avenc_mpeg4)

textoverlay = Gst.ElementFactory.make("textoverlay", "text")
pipeline.add(textoverlay)
setup_probe(textoverlay)

avimux = Gst.ElementFactory.make("avimux", None)
pipeline.add(avimux)

sink = Gst.ElementFactory.make("filesink", "filesink")
sink.set_property("location", "timestamp.avi")
pipeline.add(sink)
# ! theoradec ! ffmpegcolorspace ! autovideosink 

src.link(oggdemux)
oggdemux.link(theoradec)
theoradec.link(avenc_mpeg4)
avenc_mpeg4.link(avimux)
# decode.link(textoverlay)
avimux.link(sink)
# pad = sink.get_static_pad("sink")

# pipeline.add(src)

# pipeline.add(decode)

# src.link(videoconvert)
# videoconvert.link(videoscale)
# videoscale.link(theoraenc)
# # camerafilter.link(theoraenc)
# theoraenc.link(ogg)
# ogg.link(sink)

# decode.link(sink)

pipeline.set_state(Gst.State.PLAYING)
time.sleep(30)
pipeline.set_state(Gst.State.NULL)