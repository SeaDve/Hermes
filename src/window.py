# window.py
#
# Copyright 2021 SeaDve
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Gtk, Handy


@Gtk.Template(resource_path='/io/github/seadve/Hermes/window.ui')
class HermesWindow(Handy.ApplicationWindow):
    __gtype_name__ = 'HermesWindow'

    headerbar_group = Gtk.Template.Child()
    main_leaflet = Gtk.Template.Child()
    contacts_listbox = Gtk.Template.Child()
    message_box = Gtk.Template.Child()

    back_button = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.main_leaflet.connect("notify::folded", self.on_leaflet_notify)
        self.back_button.connect("clicked", self.on_back_button_clicked)

        self.back_button.set_visible(self.main_leaflet.get_folded())

        for index in range(10):
            self.contacts_listbox.insert(ContactRow(), -1)
            if index % 2:
                self.message_box.add(MessageRow(1))
            else:
                self.message_box.add(MessageRow(0))

    def on_leaflet_notify(self, widget, event):
        is_folded = widget.get_folded()
        self.back_button.set_visible(is_folded)
        self.headerbar_group.set_decorate_all(is_folded)

    def on_back_button_clicked(self, widget):
        self.main_leaflet.set_visible_child_name("contacts_pane")


@Gtk.Template(resource_path='/io/github/seadve/Hermes/contact.ui')
class ContactRow(Handy.ActionRow):
    __gtype_name__ = 'ContactRow'

    time_label = Gtk.Template.Child()
    avatar = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_prefix(self.avatar)
        self.set_title("Dave Patrick")
        self.set_subtitle("Hello There")
        self.time_label.set_label("22∶05")


@Gtk.Template(resource_path='/io/github/seadve/Hermes/message.ui')
class MessageRow(Gtk.Box):
    __gtype_name__ = 'MessageRow'

    avatar = Gtk.Template.Child()
    message_label = Gtk.Template.Child()

    def __init__(self, is_from_self, **kwargs):
        super().__init__(**kwargs)

        self.message_style_context = self.message_label.get_style_context()

        if is_from_self:
            self.set_from_self_mode()
        else:
            self.set_from_contact_mode()

    def set_from_self_mode(self):
        self.avatar.set_visible(False)
        self.message_label.set_margin_start(72)
        self.message_label.set_halign(Gtk.Align.END)
        self.message_label.set_justify(Gtk.Justification.RIGHT)
        self.message_style_context.add_class("message-out")
        self.message_style_context.remove_class("message-in")


    def set_from_contact_mode(self):
        self.avatar.set_visible(True)
        self.message_label.set_margin_end(72)
        self.message_label.set_halign(Gtk.Align.START)
        self.message_label.set_justify(Gtk.Justification.LEFT)
        self.message_style_context.add_class("message-in")
        self.message_style_context.remove_class("message-out")
