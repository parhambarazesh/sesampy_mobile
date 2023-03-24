import importlib

import View.CommandsScreen.commands_screen

# We have to manually reload the view module in order to apply the
# changes made to the code on a subsequent hot reload.
# If you no longer need a hot reload, you can delete this instruction.
importlib.reload(View.CommandsScreen.commands_screen)




class CommandsScreenController:
    """
    The `CommandsScreenController` class represents a controller implementation.
    Coordinates work of the view with the model.
    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """

    def __init__(self, model):
        self.model = model  # Model.commands_screen.CommandsScreenModel
        self.view = View.CommandsScreen.commands_screen.CommandsScreenView(controller=self, model=self.model)

    def get_view(self) -> View.CommandsScreen.commands_screen:
        return self.view
