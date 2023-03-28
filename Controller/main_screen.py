import importlib

from kivymd.uix.list import OneLineAvatarIconListItem, IconLeftWidget
from functools import partial

import View.MainScreen.main_screen
import os
import json

# We have to manually reload the view module in order to apply the
# changes made to the code on a subsequent hot reload.
# If you no longer need a hot reload, you can delete this instruction.
importlib.reload(View.MainScreen.main_screen)


class MainScreenController:
    """
    The `MainScreenController` class represents a controller implementation.
    Coordinates work of the view with the model.
    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """

    def __init__(self, model):
        self.model = model  # Model.main_screen.MainScreenModel
        self.view = View.MainScreen.main_screen.MainScreenView(controller=self, model=self.model)
        current_connector = model.current_connector
        # self.view.ids.title_pipes.text = "Active Connector: " + current_connector
        # self.view.ids.title_systems.text = "Active Connector: " + current_connector
        # self.view.ids.title_metadata.text = "Active Connector: " + current_connector

        # if os.path.exists(f"core/{current_connector}-connector/.expanded"):
        #     pipes_dir = f"core/{current_connector}-connector/.expanded/pipes/"
        #     for file in os.listdir(pipes_dir):
        #         if file.endswith(".json"):  # check if the file is a JSON file
        #             self.view.ids.pipes_list.add_widget(
        #                 OneLineAvatarIconListItem(
        #                     IconLeftWidget(
        #                         id="icon_left",
        #                         icon="pipe",
        #                         theme_text_color="Custom",
        #                         text_color="blue"
        #                     ),
        #                     text=file,
        #                     on_release=partial(self.view.open_pipe, file),
        #                     id=f"pipe_item_{file}",
        #                 )
        #             )
        #     systems_dir = f"core/{current_connector}-connector/.expanded/systems/"
        #     for file in os.listdir(systems_dir):
        #         if file.endswith(".json"):
        #             self.view.ids.systems_list.add_widget(
        #                 OneLineAvatarIconListItem(
        #                     IconLeftWidget(
        #                         id="icon_left",
        #                         icon="alpha-s",
        #                         theme_text_color="Custom",
        #                         text_color="blue"
        #                     ),
        #                     text=file,
        #                     on_release=partial(self.view.open_system, file),
        #                     id=f"system_item_{file}",
        #                 )
        #             )
        #     metadata_dir = f"core/{current_connector}-connector/.expanded/"
        #     for file in os.listdir(metadata_dir):
        #         if file.endswith(".json"):
        #             self.view.ids.metadata_list.add_widget(
        #                 OneLineAvatarIconListItem(
        #                     IconLeftWidget(
        #                         id="icon_left",
        #                         icon="code-json",
        #                         theme_text_color="Custom",
        #                         text_color="blue"
        #                     ),
        #                     text=file,
        #                     on_release=partial(self.view.open_metadata, file),
        #                     id=f"metadata_item_{file}",
        #                 )
        #             )


    # def open_pipe(self, file, *args):
    #     with open(f"core/{self.model.current_connector}-connector/.expanded/pipes/{file}", "r") as f:
    #         data = json.load(f)
    #     self.view.ids.show.badge_icon = "numeric-1"
    #     self.view.ids.show_file.text = json.dumps(data, indent=4)

    # def open_system(self, file, *args):
    #     with open(f"core/{self.model.current_connector}-connector/.expanded/systems/{file}", "r") as f:
    #         data = json.load(f)
    #     self.view.ids.show.badge_icon = "numeric-1"
    #     self.view.ids.show_file.text = json.dumps(data, indent=4)
    #
    # def open_metadata(self, file, *args):
    #     with open(f"core/{self.model.current_connector}-connector/.expanded/{file}", "r", encoding="utf-8-sig") as f:
    #         data = json.load(f)
    #     self.view.ids.show.badge_icon = "numeric-1"
    #     self.view.ids.show_file.text = json.dumps(data, indent=4)

    def get_view(self) -> View.MainScreen.main_screen:
        return self.view
