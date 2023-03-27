import importlib
import shutil
import webbrowser
from functools import partial
import os
import certifi
# os.environ['SSL_CERT_FILE'] = certifi.where()
# os.environ["GIT_PYTHON_REFRESH"] = "quiet"
# os.environ["GIT_PYTHON_GIT_EXECUTABLE"] = "/usr/bin/git"
# import git
from dulwich import porcelain
# configure dulwich to use certifi

# os.environ["SSL_CERT_FILE"] = "/assets/gitub-com.pem2"
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFloatingActionButtonSpeedDial, MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.textfield import MDTextField

import View.ConnectorScreen.connector_screen
from kivymd.uix.list import OneLineAvatarIconListItem, IconLeftWidget, IconRightWidget, TwoLineAvatarIconListItem, \
    OneLineIconListItem

# We have to manually reload the view module in order to apply the
# changes made to the code on a subsequent hot reload.
# If you no longer need a hot reload, you can delete this instruction.
importlib.reload(View.ConnectorScreen.connector_screen)


class ConnectorScreenController:
    """
    The `CommandsScreenController` class represents a controller implementation.
    Coordinates work of the view with the model.
    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """

    def __init__(self, model):
        self.model = model  # Model.command_screen.CommandScreenModel
        self.view = View.ConnectorScreen.connector_screen.ConnectorScreenView(controller=self, model=self.model)

        self.speed_dial_data = model.speed_dial_data
        self.downloaded_connectors = model.downloaded_connectors
        speed_dial = MDFloatingActionButtonSpeedDial()
        speed_dial.data = self.speed_dial_data
        speed_dial.root_button_anim = True
        speed_dial.callback = self.callback_for_menu_items

        connectors_list = self.model.connectors_list
        for connector in connectors_list:
            self.view.ids.connector_list.add_widget(
                OneLineAvatarIconListItem(
                    IconLeftWidget(
                        id="icon_left",
                        icon="cog",
                        theme_text_color="Custom",
                        text_color="blue" if not connector[0] in self.downloaded_connectors else "red"
                    ),
                    IconRightWidget(
                        id="icon_right",
                        icon="download" if connector[0] not in self.downloaded_connectors else "delete",
                        on_release=partial(self.download_or_delete_connector, connector),
                        theme_text_color = "Custom",
                        text_color = "blue" if not connector[0] in self.downloaded_connectors else "red",
                    ),
                    text=connector[0],
                    secondary_text=connector[1],
                    on_release=partial(self.open_connector, connector),
                    id=f"connector_item_{connector[0]}",
                )
            )

        self.view.add_widget(speed_dial)

    def get_view(self) -> View.ConnectorScreen.connector_screen:
        return self.view

    def download_or_delete_connector(self, connector, *args):
        try:
            connector_object_list=[{"id": x.id, "connector": x} for x in self.view.ids.connector_list.children]
            downloaded_connector=[d for d in connector_object_list if d["id"] == f"connector_item_{connector[0]}"][0]
            if downloaded_connector["connector"].ids.icon_right.icon == "download":
                print("Downloading connector")
                if os.path.exists(f"core/{connector[0]}-connector"):
                    shutil.rmtree(f"core/{connector[0]}-connector")
                os.mkdir(f"core/{connector[0]}-connector")
                repo_url = connector[1]+".git"
                # repo_url="https://github.com/jelmer/dulwich.git"
                porcelain.clone(repo_url, f"core/{connector[0]}-connector")
                print("\n\n\n\n\nCloned repo")
                #disable ssl verification
                # os.chdir("core")
                # git.Git().clone(connector[1], "--config", "http.sslVerify=false")
                # os.chdir("..")
                downloaded_connector["connector"].ids.icon_right.icon = "delete"
                downloaded_connector["connector"].ids.icon_right.text_color = "red"
                downloaded_connector["connector"].ids.icon_left.text_color = "red"
            else:
                print("Deleting connector")
                shutil.rmtree(f"core/{connector[0]}-connector")
                downloaded_connector["connector"].ids.icon_right.icon = "download"
                downloaded_connector["connector"].ids.icon_right.text_color = "blue"
                downloaded_connector["connector"].ids.icon_left.text_color = "blue"
        except Exception as e:
            print(f"Some unexpected error happened: {e}")

    def open_connector(self, connector, *args):
        webbrowser.open_new_tab(connector[1])

    def callback_for_menu_items(self, instance):
        if instance.icon == "connection":
            self.dialog = self.get_dialog_box()
        self.dialog.open()

    def get_dialog_box(self):
        return MDDialog(
            title="Add Connector",
            type="custom",
            content_cls=MDBoxLayout(
                MDRaisedButton(
                    text="Add from Sesam Community",
                    theme_text_color="Custom",
                    on_release=self.cancel_dialog,
                ),
                orientation="vertical",
                spacing="12dp",
                size_hint_y=None,
                height="120dp",
                id="connector_data",
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
                    on_release=lambda x: self.submit_dialog(x),
                ),
            ],
        )

    def cancel_dialog(self, instance):
        self.dialog.dismiss()

    def submit_dialog(self, instance):
        print(self.dialog.ids.config_data.children[0].text)
        print(self.dialog.ids.config_data.children[1].text)
        self.dialog.dismiss()
