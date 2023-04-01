import importlib
import os
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.textfield import MDTextField

import View.ConfigScreen.config_screen
from kivymd.uix.button import MDFloatingActionButtonSpeedDial, MDFlatButton

# We have to manually reload the view module in order to apply the
# changes made to the code on a subsequent hot reload.
# If you no longer need a hot reload, you can delete this instruction.
importlib.reload(View.ConfigScreen.config_screen)


class ConfigScreenController:
    """
    The `CommandsScreenController` class represents a controller implementation.
    Coordinates work of the view with the model.
    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """

    def __init__(self, model):
        self.model = model  # Model.command_screen.CommandScreenModel
        self.view = View.ConfigScreen.config_screen.ConfigScreenView(controller=self, model=self.model)
        self.speed_dial_data = model.speed_dial_data

        speed_dial = MDFloatingActionButtonSpeedDial()
        speed_dial.data = self.speed_dial_data
        speed_dial.root_button_anim = True
        speed_dial.callback = self.callback_for_menu_items
        self.view.add_widget(speed_dial)


    def get_view(self) -> View.ConfigScreen.config_screen:
        return self.view

    def callback_for_menu_items(self, instance):
        print("INSTANCE", instance.icon)
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
            with open(os.path.join(os.getcwd(), "core/.syncconfig"), "w+") as f:
                f.write(f'JWT="{config_data2}"\n')
                f.write(f'NODE="{config_data1}"')
                self.view.ids.node_url.text = config_data2
                self.view.ids.node_jwt_token.text = config_data1
        elif config=="OAuth2":
            with open(os.path.join(os.getcwd(), "core/.authconfig"), "w+") as f:
                f.write(f'CLIENT_ID="{config_data1}"\n')
                f.write(f'CLIENT_SECRET="{config_data2}"\n')
                self.view.ids.oauth2_client_id.text = config_data1
                self.view.ids.oauth2_client_secret.text = config_data2

                self.view.ids.tripletex_consumer_token.text = "Tripletex Consumer Token"
                self.view.ids.tripletex_employee_token.text = "Tripletex Employee Token"
        elif config=="Tripletex":
            with open(os.path.join(os.getcwd(), "core/.authconfig"), "w+") as f:
                f.write(f'CONSUMER_TOKEN="{config_data1}"\n')
                f.write(f'EMPLOYEE_TOKEN="{config_data2}"\n')
                self.view.ids.tripletex_consumer_token.text = config_data1
                self.view.ids.tripletex_employee_token.text = config_data2

                self.view.ids.oauth2_client_id.text = "OAuth2 Client ID"
                self.view.ids.oauth2_client_secret.text = "OAuth2 Client Secret"
