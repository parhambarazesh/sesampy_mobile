import importlib

import View.ConfigScreen.config_screen
from kivymd.uix.button import MDFloatingActionButtonSpeedDial
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
        self.speed_dial_data=model.speed_dial_data

        speed_dial = MDFloatingActionButtonSpeedDial()
        speed_dial.data = self.speed_dial_data
        speed_dial.root_button_anim = True
        speed_dial.callback = self.callback_for_menu_items
        self.view.add_widget(speed_dial)

    def get_view(self) -> View.ConfigScreen.config_screen:

        return self.view

    def callback_for_menu_items(self, instance):
        print(instance.icon)
        if instance.icon == 'pipe-disconnected':
            self.view.manager_screens.current = 'Node Config'
        elif instance.icon == 'connection':
            self.view.manager_screens.current = 'Connector Config'