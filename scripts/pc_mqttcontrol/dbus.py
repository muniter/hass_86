#!/usr/bin/env python3
# This code indeed works but have to understand it first

from gi.repository import GLib
from gi.repository import Gio

def onPrepareForSleep(conn, sender, obj, interface, signal, parameters, data):
    print("Going to sleep")
    if not parameters[0]: # parameters[0] is True just before sleep, False just after wake
        print("Just woke up!")

system_bus = Gio.bus_get_sync(Gio.BusType.SYSTEM, None)
system_bus.signal_subscribe('org.freedesktop.login1',
                            'org.freedesktop.login1.Manager',
                            'PrepareForSleep',
                            '/org/freedesktop/login1',
                            None,
                            Gio.DBusSignalFlags.NONE,
                            onPrepareForSleep,
                            None)

GLib.MainLoop().run()
