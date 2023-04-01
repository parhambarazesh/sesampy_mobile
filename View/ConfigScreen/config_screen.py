from View.base_screen import BaseScreenView
import os
from constants import ROOT_DIR

class ConfigScreenView(BaseScreenView):
    def on_pre_leave(self, *args):
        os.chdir(ROOT_DIR)
    def on_enter(self, *args):
        os.chdir("core")
        if not os.path.exists(os.path.join(os.getcwd(),".syncconfig")):
            open(".syncconfig", 'a').close()
        if not os.path.exists(os.path.join(os.getcwd(),".authconfig")):
            open(".authconfig", 'a').close()

        with open(os.path.join(os.getcwd(),".syncconfig"), "r") as f:
            content = f.read()
            if content != "":
                key_value_pairs = [line.strip().split('=', 1) for line in content.splitlines()]
                obj = {key.strip(): value.strip('"') for key, value in key_value_pairs}
                self.ids.node_url.text = obj['NODE']
                self.ids.node_jwt_token.text = obj['JWT']
        with open(os.path.join(os.getcwd(),".authconfig"), "r") as f:
            content = f.read()
            if content != "":
                key_value_pairs = [line.strip().split('=', 1) for line in content.splitlines()]
                obj = {key.strip(): value.strip('"') for key, value in key_value_pairs}
                if "CLIENT_ID" in obj and "CLIENT_SECRET" in obj:
                    self.ids.oauth2_client_id.text = obj['CLIENT_ID']
                    self.ids.oauth2_client_secret.text = obj['CLIENT_SECRET']
                elif "CONSUMER_TOKEN" in obj and "EMPLOYEE_TOKEN" in obj:
                    self.ids.tripletex_consumer_token.text = obj['CONSUMER_TOKEN']
                    self.ids.tripletex_employee_token.text = obj['EMPLOYEE_TOKEN']
    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """