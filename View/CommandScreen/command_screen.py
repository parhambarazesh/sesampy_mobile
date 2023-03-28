import threading

import time
import sys,stat
from kivy.clock import mainthread
from kivymd.uix.spinner import MDSpinner

from View.base_screen import BaseScreenView
from Model.main_screen import MainScreenModel
import os
import subprocess


class CommandScreenView(BaseScreenView):

    def on_enter(self, *args):
        """
        Called whenever the screen is entered.
        """
        self.current_connector = MainScreenModel.current_connector

    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """

    @mainthread
    def spinner_toggle(self):
        print('Spinner Toggle')
        spinner_obj=self.ids[f"spinner_{self.command}"]
        if not spinner_obj.active:
            spinner_obj.active = True
        else:
            spinner_obj.active = False
        # if event.is_set():
            self.ids.log.text = self.logs
            self.ids.logs.badge_icon = "numeric-1"


    def run_command(self, *args) -> None:
        print("CURRENT PATH:"+os.getcwd())
        print(f"ALL FILES in current path:{os.listdir('.')}")
        print(f"ALL FILES in core path:{os.listdir('./core')}")
        os.chdir(os.path.join(os.getcwd(), "core"))
        # open debugger
        # os.chmod("sesam.pyc", 0o755)
        # cmd = ["./sesam", "download", "-vv", "-d", "tripletex-connector"]
        # subprocess.run(cmd)
        cmd = [sys.executable, "sesam.py", self.command, "-vv", "-d", f"{self.current_connector}-connector"]
        # give permission to execute file : dist/sesam
        # os.chmod("sesam.py", stat.S_IRWXU)
        with open("../command_logs.txt", "w") as f:
            print("CURRENT PATH BEFORE SUBPROCESS:"+os.getcwd())
            result = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT)
        os.chdir("..")
        print(os.getcwd())
        # event.set()
        with open("command_logs.txt", "r") as f:
            self.logs=f.read()

        self.spinner_toggle()

    def command_thread(self, *args) -> None:
        # global event
        # event = threading.Event()
        # event.clear()
        self.command=args[0]
        self.spinner_toggle()
        self.thread=threading.Thread(target=(self.run_command))
        self.thread.start()

    def download(self, *args) -> None:
        os.chdir(os.path.join(os.getcwd(), "core"))
        # open debugger
        # os.chmod("sesam.pyc", 0o755)
        # cmd = ["./sesam", "download", "-vv", "-d", "tripletex-connector"]
        # subprocess.run(cmd)
        cmd = [sys.executable, "simplecli.py", "download"]
        # give permission to execute file : dist/sesam
        print("CURRENT PATH BEFORE SUBPROCESS:" + os.getcwd())
        print("CURRENT FILES BEFORE SUBPROCESS:" + str(os.listdir('.')))
        # os.chmod("sesam.py", stat.S_IRWXU)
        os.path.join(os.getcwd(), "sesam.py")
        with open("../command_logs.txt", "w") as f:
            print("CURRENT PATH BEFORE SUBPROCESS:" + os.getcwd())
            print("CMD:" + str(cmd))
            result = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT)
        os.chdir("..")
        with open("command_logs.txt", "r") as f:
            self.logs=f.read()
            self.ids.log.text = self.logs
            self.ids.logs.badge_icon = "numeric-1"


    def get_logs(self, *args) -> None:
        # remove the badge
        self.ids.logs.badge_icon = ""
