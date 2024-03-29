import json
from functools import partial
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from Model.connector_screen import ConnectorScreenModel as connector_model
from kivymd.uix.list import OneLineAvatarIconListItem, IconLeftWidget
from View.base_screen import BaseScreenView
import os

from constants import ROOT_DIR


from kivymd.uix.list import OneLineAvatarIconListItem, IconLeftWidget
from View.base_screen import BaseScreenView
import os

class MainScreenView(BaseScreenView):
    def on_pre_leave(self, *args):
        os.chdir(ROOT_DIR)

    def on_pre_enter(self, *args):
        self.ids.pipes_list.clear_widgets()
        self.ids.systems_list.clear_widgets()
        self.ids.metadata_list.clear_widgets()
        self.ids.show_file.text = ""
        if connector_model.current_connector != "":
            if os.path.exists(f"{connector_model.current_connector}-connector/.expanded"):
                self.ids.loading_configs.opacity = 1

    def load_config_files(self):
        current_connector = connector_model.current_connector
        if connector_model.current_connector != "":
            self.pipes_list = []
            if os.path.exists(f"{current_connector}-connector/.expanded"):
                pipes_dir = f"{current_connector}-connector/.expanded/pipes/"
                print(f"PIPES_DIR: {pipes_dir}")
                for file in os.listdir(pipes_dir):
                    print("Pipe: " + file)
                    if file.endswith(".json"):  # check if the file is a JSON file
                        self.pipes_list.append(file)
                        self.ids.pipes_list.add_widget(
                            OneLineAvatarIconListItem(
                                IconLeftWidget(
                                    id="icon_left",
                                    icon="pipe",
                                    theme_text_color="Custom",
                                    text_color="blue"
                                ),
                                text=file,
                                text_color=(
                                    250 / 255, 250 / 255, 250 / 255, 1) if self.theme_cls.theme_style == "Dark" else (
                                    18 / 255, 18 / 255, 18 / 255, 1),
                                on_release=partial(self.open_pipe, file),
                                id=f"pipe_item_{file}",
                            )
                        )
                systems_dir = f"{current_connector}-connector/.expanded/systems/"
                self.systems_list = []
                for file in os.listdir(systems_dir):
                    print("System: " + file)
                    if file.endswith(".json"):
                        self.systems_list.append(file)
                        self.ids.systems_list.add_widget(
                            OneLineAvatarIconListItem(
                                IconLeftWidget(
                                    id="icon_left",
                                    icon="alpha-s",
                                    theme_text_color="Custom",
                                    text_color="blue"
                                ),
                                text=file,
                                theme_text_color="Custom",
                                text_color=(
                                250 / 255, 250 / 255, 250 / 255, 1) if self.theme_cls.theme_style == "Dark" else (
                                18 / 255, 18 / 255, 18 / 255, 1),
                                on_release=partial(self.open_system, file),
                                id=f"system_item_{file}",
                            )
                        )
                metadata_dir = f"{current_connector}-connector/.expanded/"
                self.metadata_list = []
                for file in os.listdir(metadata_dir):
                    print("Metadata: " + file)
                    if file.endswith(".json"):
                        self.metadata_list.append(file)
                        self.ids.metadata_list.add_widget(
                            OneLineAvatarIconListItem(
                                IconLeftWidget(
                                    id="icon_left",
                                    icon="code-json",
                                    theme_text_color="Custom",
                                    text_color="blue"
                                ),
                                text=file,
                                theme_text_color="Custom",
                                text_color=(
                                250 / 255, 250 / 255, 250 / 255, 1) if self.theme_cls.theme_style == "Dark" else (
                                18 / 255, 18 / 255, 18 / 255, 1),
                                on_release=partial(self.open_metadata, file),
                                id=f"metadata_item_{file}",
                            )
                        )
                self.ids.loading_configs.opacity = 0


    def on_enter(self, *args):
        os.chdir("core")
        self.load_config_files()
        print("Entered Main Screen")

    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """


    def switch_window(self, window_name: str) -> None:
        """
        Switches the application window to the specified window.
        """
        print(f"Switching to {window_name} window!")
        self.manager_screens.current = window_name

    def get_file(self, *args) -> None:
        """
        Get the file.
        """
        self.ids.show.badge_icon = ""

    def open_pipe(self, file, *args):
        self.selected_file = f"{connector_model.current_connector}-connector/.expanded/{file}"
        with open(f"{connector_model.current_connector}-connector/.expanded/pipes/{file}", "r") as f:
            data = json.load(f)
        self.ids.show.badge_icon = "numeric-1"
        self.ids.show_file.text = json.dumps(data, indent=4)

    def open_system(self, file, *args):
        self.selected_file = f"{connector_model.current_connector}-connector/.expanded/{file}"
        with open(f"{connector_model.current_connector}-connector/.expanded/systems/{file}", "r") as f:
            data = json.load(f)
        self.ids.show.badge_icon = "numeric-1"
        self.ids.show_file.text = json.dumps(data, indent=4)

    def open_metadata(self, file, *args):
        self.selected_file = f"{connector_model.current_connector}-connector/.expanded/{file}"
        with open(f"{connector_model.current_connector}-connector/.expanded/{file}", "r", encoding="utf-8-sig") as f:
            data = json.load(f)
        self.ids.show.badge_icon = "numeric-1"
        self.ids.show_file.text = json.dumps(data, indent=4)

    def save_file(self, *args):
        try:
            if self.selected_file.endswith("test-env.json"):
                with open(f"{connector_model.current_connector}-connector/test-env.json", "w") as f:
                    json.dump(json.loads(self.ids.show_file.text), f, indent=4)

                with open(self.selected_file, "w") as f:
                    json.dump(json.loads(self.ids.show_file.text), f, indent=4)
            else:
                with open(self.selected_file, "w") as f:
                    json.dump(json.loads(self.ids.show_file.text), f, indent=4)
        except:
            # show a dialog
            dialog = MDDialog(
                title="Cannot save file",
                text="Invalid json format",
                size_hint=(0.7, 1),
                buttons=[
                    MDFlatButton(
                        text="Ok",
                        # theme_text_color="Custom",
                        # text_color=self.theme_cls.primary_color,
                        on_release=lambda x: dialog.dismiss(),
                    ),
                ],
            )
            dialog.open()

    def reset_file(self, *args):
        try:
            with open(self.selected_file, "r") as f:
                data = json.load(f)
            self.ids.show_file.text = json.dumps(data, indent=4)
        except:
            # show a dialog
            dialog = MDDialog(
                title="Cannot reset file",
                text="Invalid json format",
                size_hint=(0.7, 1),
                buttons=[
                    MDFlatButton(
                        text="Ok",
                        # theme_text_color="Custom",
                        # text_color=self.theme_cls.primary_color,
                        on_release=lambda x: dialog.dismiss(),
                    ),
                ],
            )
            dialog.open()
