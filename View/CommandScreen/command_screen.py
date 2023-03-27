from View.base_screen import BaseScreenView
import os
import subprocess

class CommandScreenView(BaseScreenView):
    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """
    def download(self, *args) -> None:
        """
        Download the file.
        """
        os.chdir("core")
        cmd = ["python", "sesam.py", "download","-vv","-d","tripletex-connector"]
        with open("../command_logs.txt", "w") as f:
            # Run the command and redirect the output to the file
            result = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT)
        # subprocess.run(cmd)
        os.chdir("..")
        with open("command_logs.txt", "r") as f:
            self.ids.log.text = f.read()
            self.ids.logs.badge_icon = "numeric-1"

    def get_logs(self, *args) -> None:
        # remove the badge
        self.ids.logs.badge_icon = ""
