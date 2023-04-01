from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField

from View.base_screen import BaseScreenView
import os
from constants import ROOT_DIR
from Model.config_screen import ConfigScreenModel as model
from kivymd.uix.button import MDFloatingActionButtonSpeedDial, MDFlatButton


class ConfigScreenView(BaseScreenView):
    def on_pre_leave(self, *args):
        os.chdir(ROOT_DIR)

    def on_pre_enter(self, *args):
        self.speed_dial = MDFloatingActionButtonSpeedDial()
        self.data = {
        'Node Config': [
            'pipe-disconnected',
            "on_release", self.callback_for_menu_items
        ],
        'OAth2 Config': [
            'connection',
            "on_release", self.callback_for_menu_items
        ],
        'Tripletex Config': [
            'alpha-t',
            "on_release", self.callback_for_menu_items
        ],
    }
        self.speed_dial.data = self.data
        self.speed_dial.root_button_anim = True
        # self.speed_dial.on_release_stack_button = self.callback_for_menu_items
        self.ids.box.parent.add_widget(self.speed_dial)

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

    def callback_for_menu_items(self, instance):
        if instance.icon == "pipe-disconnected":
            print("NODE")
            self.dialog = self.get_dialog_box("Node")
        elif instance.icon == "connection":
            print("OAUTH2")
            self.dialog = self.get_dialog_box("OAuth2")
        elif instance.icon == "alpha-t":
            print("TRIPLETEX")
            self.dialog = self.get_dialog_box("Tripletex")
        self.dialog.open()

    def get_dialog_box(self, config):
        print("CONFIG", config)
        return MDDialog(
            title="Node Config" if config == "Node" else "OAuth2 Config" if config == "OAuth2" else "Tripletex Config",
            type="custom",
            content_cls=MDBoxLayout(
                MDTextField(
                    hint_text="Node URL" if config == "Node" else "CLIENT ID" if config == "OAuth2" else "CONSUMER_TOKEN",
                ),
                MDTextField(
                    hint_text="JWT Token" if config == "Node" else "CLIENT SECRET" if config == "OAuth2" else "EMPLOYEE_TOKEN",
                ),
                orientation="vertical",
                spacing="12dp",
                size_hint_y=None,
                height="120dp",
                id="config_data",
            ),
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    on_release=self.cancel_dialog,
                ),
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    on_release=lambda x: self.submit_dialog(x, config),
                ),
            ],
        )

    def cancel_dialog(self, instance):
        self.dialog.dismiss()

    def submit_dialog(self,instance, config):
        self.dialog.dismiss()
        config_data1 = self.dialog.content_cls.children[1].text
        config_data2 = self.dialog.content_cls.children[0].text
        if config_data1=="" or config_data2=="":
            return

        if config=="Node":
            with open(os.path.join(os.getcwd(), ".syncconfig"), "w+") as f:
                f.write(f'JWT="{config_data2}"\n')
                f.write(f'NODE="{config_data1}"')
                self.ids.node_url.text = config_data2
                self.ids.node_jwt_token.text = config_data1
        elif config=="OAuth2":
            with open(os.path.join(os.getcwd(), ".authconfig"), "w+") as f:
                f.write(f'CLIENT_ID="{config_data1}"\n')
                f.write(f'CLIENT_SECRET="{config_data2}"\n')
                self.ids.oauth2_client_id.text = config_data1
                self.ids.oauth2_client_secret.text = config_data2

                self.ids.tripletex_consumer_token.text = "Tripletex Consumer Token"
                self.ids.tripletex_employee_token.text = "Tripletex Employee Token"
        elif config=="Tripletex":
            with open(os.path.join(os.getcwd(), ".authconfig"), "w+") as f:
                f.write(f'CONSUMER_TOKEN="{config_data1}"\n')
                f.write(f'EMPLOYEE_TOKEN="{config_data2}"\n')
                self.ids.tripletex_consumer_token.text = config_data1
                self.ids.tripletex_employee_token.text = config_data2

                self.ids.oauth2_client_id.text = "OAuth2 Client ID"
                self.ids.oauth2_client_secret.text = "OAuth2 Client Secret"
    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """