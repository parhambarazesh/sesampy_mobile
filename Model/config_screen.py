from Model.base_model import BaseScreenModel


class ConfigScreenModel(BaseScreenModel):
    """
    Implements the logic of the
    :class:`~View.command_screen.CommandScreen.CommandScreenView` class.
    """
    speed_dial_data = {
        'Node Config': 'pipe-disconnected',
        'OAth2 Config': 'connection',
        'Tripletex Config': 'alpha-t',
    }