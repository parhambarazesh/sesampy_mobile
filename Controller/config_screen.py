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


    def get_view(self) -> View.ConfigScreen.config_screen:
        return self.view
