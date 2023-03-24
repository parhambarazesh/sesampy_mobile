# The screens dictionary contains the objects of the models and controllers
# of the screens of the application.


from Model.main_screen import MainScreenModel
from Controller.main_screen import MainScreenController
from Model.commands_screen import CommandsScreenModel
from Controller.commands_screen import CommandsScreenController

screens = {
    "main_screen": {
        "model": MainScreenModel,
        "controller": MainScreenController,
    },
    "commands_screen": {
        "model": CommandsScreenModel,
        "controller": CommandsScreenController,
    },
}