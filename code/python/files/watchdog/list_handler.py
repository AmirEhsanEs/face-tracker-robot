import re
import os
from watchdog.events import FileSystemEventHandler 
from PyQt5.QtCore import QSize,pyqtSignal as Signal,QObject


def natural_key(string):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', string)]
class ListHandler(QObject,FileSystemEventHandler):
    update_signal=Signal()
    def __init__(self, directory):
        QObject.__init__(self)
        FileSystemEventHandler.__init__(self)
        self.directory = directory

    def on_modified(self, event):
        self.update_list()

    def on_created(self, event):
        if not event.is_directory:
            self.update_list()

    def on_moved(self, event):
        if not event.is_directory:
            self.update_list()

    def on_deleted(self, event):
        self.update_list()

    def update_list(self):
       self.update_signal.emit()

