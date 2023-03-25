import importlib
import webbrowser
from functools import partial

from kivy.metrics import dp
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFloatingActionButtonSpeedDial, MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.menu import MDDropdownMenu
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
        speed_dial = MDFloatingActionButtonSpeedDial()
        speed_dial.data = self.speed_dial_data
        speed_dial.root_button_anim = True
        speed_dial.callback = self.callback_for_menu_items

        connectors_list = self.model.connectors_list
        for connector in connectors_list:
            self.view.ids.connector_list.add_widget(
                TwoLineAvatarIconListItem(
                    IconLeftWidget(
                        icon="cog"
                    ),
                    IconRightWidget(
                        icon="download",
                        on_release=lambda x: self.download_connector(connector)
                    ),
                    text=connector[0],
                    secondary_text=connector[1],
                    on_release=partial(self.open_connector, connector)
                )
            )

        self.view.add_widget(speed_dial)




    def get_view(self) -> View.ConnectorScreen.connector_screen:
        return self.view

    def download_connector(self, connector):
        webbrowser.open_new_tab(connector[1])

    def open_connector(self, connector,*args):
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
