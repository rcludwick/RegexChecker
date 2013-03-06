#!/usr/bin/env python

from gi.repository import Gtk

import re

class RegexWindow(object):

    def __init__(self):
        object.__init__(self)
        self.__builder = Gtk.Builder()
        self.__builder.add_from_file("regex.glade")
        self.__builder.connect_signals(self)
        self.__input_text = self.__builder.get_object('input_text_buffer')
        self.__regex_text = self.__builder.get_object('regex_text_buffer')
        self.__output_text = self.__builder.get_object('output_text_buffer')
        self.__builder.get_object('regexwindow').show_all()
        self.colors=["#CD5C5C", "#ff7f50"]
        self.tags = []
        for color in self.colors:
            tag = self.__output_text.create_tag(color, background=color)
            self.tags.append(tag)

    def on_input_text_buffer_changed(self, widget):
        self.apply_regex()

    def on_regex_text_buffer_changed(self, widget):
        self.apply_regex()

    def on_regexwindow_destroy(self, widget):
        try:
            pass
        finally:
            Gtk.main_quit()

    def get_text(self, buf):
        start = buf.get_start_iter()
        stop = buf.get_end_iter()
        return buf.get_text(start,stop,False)

    def apply_regex(self):
        input_text = self.get_text(self.__input_text)
        regex_text = self.get_text(self.__regex_text)
        self.__output_text.set_text(input_text)

        start_iter = self.__output_text.get_start_iter()
        end_iter = self.__output_text.get_start_iter()
        try:
            count = 0
            for match_object in re.finditer(regex_text, input_text):
                start = match_object.start(0)
                end = match_object.end(0)
                if start == end:
                    continue
                count = count+1
                color = self.tags[count % len(self.tags) ]
                start_iter.set_offset(start)
                end_iter.set_offset(end)
                self.__output_text.apply_tag(color, start_iter, end_iter)

        except re.error:
            pass

if __name__ == "__main__":
    r = RegexWindow()
    Gtk.main()

