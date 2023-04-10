import logging
import os
import shutil
import webbrowser
from functools import partial
import zipfile

import requests
from kivymd.uix.list import OneLineAvatarIconListItem, IconLeftWidget, IconRightWidget

from Model.main_screen import MainScreenModel as main_model
from Model.connector_screen import ConnectorScreenModel as connector_model
from View.base_screen import BaseScreenView
from constants import ROOT_DIR


class ConnectorScreenView(BaseScreenView):
    def on_pre_leave(self, *args):
        os.chdir(ROOT_DIR)

    def on_pre_enter(self, *args):
        self.ids.connector_list.clear_widgets()
        self.ids.loading_connectors.opacity = 1
    def on_enter(self, *args):
        print("on_enter")
        os.chdir("core")
        # remove all children from connector_list
        self.ids.connector_list.clear_widgets()

        print("Downloaded connectors: ", connector_model.downloaded_connectors)
        print("current_connector: ", connector_model.current_connector)
        connectors_list = self.model.connectors_list
        for connector in connectors_list:
            self.ids.connector_list.add_widget(
                OneLineAvatarIconListItem(
                    IconLeftWidget(
                        id="icon_left",
                        icon="cog",
                        on_release=partial(self.set_active_connector, connector),
                        theme_text_color="Custom",
                        text_color="gold" if connector[0] in connector_model.current_connector else "blue"
                    ),
                    IconRightWidget(
                        id="icon_right",
                        icon="download" if connector[0] not in connector_model.downloaded_connectors else "delete",
                        on_release=partial(self.download_or_delete_connector, connector),
                        theme_text_color="Custom",
                        text_color="blue" if not connector[0] in connector_model.downloaded_connectors else "red",
                    ),
                    text=connector[0],
                    secondary_text=connector[1],
                    on_release=partial(self.open_connector, connector),
                    id=f"connector_item_{connector[0]}",
                )
            )
        self.ids.loading_connectors.opacity = 0

    def set_active_connector(self, connector, *args):
        connector_model.current_connector = connector[0]
        # MainScreenView.model_is_changed(View.MainScreen.main_screen.MainScreenView)
        # MainScreenController.update(self)
        connector_object_list = [{"id": x.id, "connector": x} for x in self.ids.connector_list.children]
        for connector_item in connector_object_list:
            if connector_item["id"] != f"connector_item_{connector_model.current_connector}":
                connector_item["connector"].ids.icon_left.text_color = "blue"
            else:
                connector_item["connector"].ids.icon_left.text_color = "gold"

    def download_or_delete_connector(self, connector, *args):
        try:
            connector_object_list=[{"id": x.id, "connector": x} for x in self.ids.connector_list.children]
            downloaded_connector=[d for d in connector_object_list if d["id"] == f"connector_item_{connector[0]}"][0]
            if downloaded_connector["connector"].ids.icon_right.icon == "download":
                if os.path.exists(f"{connector[0]}-connector"):
                    shutil.rmtree(f"{connector[0]}-connector")

                repository_url = f"https://api.github.com/repos/sesam-io/{connector[0]}-connector/zipball"

                # Send the request to get the archive link
                response = requests.get(repository_url)
                # check if repo file exists, if so remove it
                if os.path.isfile("repo"):
                    os.remove("repo")
                with open("repo", "wb") as f:
                    f.write(response.content)
                # Unzip the file
                with zipfile.ZipFile("repo", "r") as zip_ref:
                    zip_ref.extractall()
                    os.rename(zip_ref.namelist()[0].split('/')[0], f"{connector[0]}-connector")
                # Remove the zip file
                os.remove("repo")

                downloaded_connector["connector"].ids.icon_right.icon = "delete"
                downloaded_connector["connector"].ids.icon_right.text_color = "red"
                # add connector to connector_model.downloaded_connectors
                connector_model.downloaded_connectors.append(connector[0])
            else:
                shutil.rmtree(f"{connector[0]}-connector")
                downloaded_connector["connector"].ids.icon_right.icon = "download"
                downloaded_connector["connector"].ids.icon_right.text_color = "blue"
                # remove connector from connector_model.downloaded_connectors
                connector_model.downloaded_connectors.remove(connector[0])
        except Exception as e:
            logging.error(f"Error uploading/downloading connector: {e}")

    def open_connector(self, connector, *args):
        webbrowser.open_new_tab(connector[1])

    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """
