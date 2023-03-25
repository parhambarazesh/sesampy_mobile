# The screens dictionary contains the objects of the models and controllers
# of the screens of the application.


from Model.main_screen import MainScreenModel
from Controller.main_screen import MainScreenController
from Model.command_screen import CommandScreenModel
from Controller.command_screen import CommandScreenController
from Model.connector_screen import ConnectorScreenModel
from Controller.connector_screen import ConnectorScreenController

screens = {
    "main_screen": {
        "model": MainScreenModel,
        "controller": MainScreenController,
    },
    "command_screen": {
        "model": CommandScreenModel,
        "controller": CommandScreenController,
    },
    "connector_screen": {
        "model": ConnectorScreenModel,
        "controller": ConnectorScreenController,
    },
}