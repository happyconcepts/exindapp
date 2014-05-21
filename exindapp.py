#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  exindapp.py
#  
#  Copyright 2014 Paul Green <thatgreenguy@gmx.co.uk>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import sys
import gtk
import appindicator

import imaplib
import re

PING_FREQUENCY = 10 # seconds

class CheckGMail:
    def __init__(self):
        self.ind = appindicator.Indicator("debian-doc-menu",
                                           "debian-doc-menu",
                                           appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        self.ind.set_attention_icon("new-messages-blue")

        self.menu_setup()
        self.ind.set_menu(self.menu)

    def menu_setup(self):
        self.menu = gtk.Menu()

        self.hello_item = gtk.MenuItem("Hello")
        self.hello_item.connect("activate", self.quit)
        self.quit_item = gtk.MenuItem("Quit")
        self.quit_item.connect("activate", self.quit)
        self.hello_item.show()
        self.quit_item.show()
        self.menu.append(self.quit_item)
        self.menu.append(self.hello_item)

    def main(self):
        self.check_mail()
        gtk.timeout_add(PING_FREQUENCY * 1000, self.check_mail)
        gtk.main()

    def quit(self, widget):
        sys.exit(0)

    def check_mail(self):
        messages, unread = self.gmail_checker('paul.green.dev@gmail.com','python619#G')
        if unread > 0:
            self.ind.set_status(appindicator.STATUS_ATTENTION)
        else:
            self.ind.set_status(appindicator.STATUS_ACTIVE)
        return True

    def gmail_checker(self, username, password):
        i = imaplib.IMAP4_SSL('imap.gmail.com')
        try:
            i.login(username, password)
            x, y = i.status('INBOX', '(MESSAGES UNSEEN)')
            messages = int(re.search('MESSAGES\s+(\d+)', y[0]).group(1))
            unseen = int(re.search('UNSEEN\s+(\d+)', y[0]).group(1))
            return (messages, unseen)
        except:
            return False, 0

if __name__ == "__main__":
    indicator = CheckGMail()
    indicator.main()
    
