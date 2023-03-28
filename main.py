"""
Script for managing hot reloading of the project.
For more details see the documentation page -

https://kivymd.readthedocs.io/en/latest/api/kivymd/tools/patterns/create_project/

To run the application in hot boot mode, execute the command in the console:
DEBUG=1 python main.py
"""

import importlib
import os

from kivy import Config

from PIL import ImageGrab

from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.toolbar import MDTopAppBar

# You may know an easier way to get the size of a computer display.
resolution = ImageGrab.grab().size

# Change the values of the application window size as you need.
Config.set("graphics", "height", resolution[1])
Config.set("graphics", "width", "600")

from kivy.core.window import Window

# set window size to fill the screen
Window.size = (500, resolution[1])

# Place the application window on the right side of the computer screen.
Window.top = 0
Window.left = resolution[0] - Window.width

from kivymd.tools.hotreload.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivy.uix.screenmanager import NoTransition


class sesampy(MDApp):
    KV_DIRS = [os.path.join(os.getcwd(), "View")]
    nav_drawer = ObjectProperty()

    def build_app(self) -> MDScreenManager:
        """
        In this method, you don't need to change anything other than the
        application theme.
        """
        top_app_bar = MDTopAppBar(title="Sesampy",
                                  pos_hint={'top': 1},
                                  elevation=2,
                                  left_action_items=[['menu', lambda x: self.nav_drawer_open()]],
                                  right_action_items=[
                                      ['home', lambda x: self.switch_window("main_screen")],
                                      ["file-document", lambda x: None],
                                      ['theme-light-dark', lambda x: None],
                                  ]
                                  )
        import View.screens

        self.manager_screens = MDScreenManager(transition=NoTransition())
        Window.bind(on_key_down=self.on_keyboard_down)
        importlib.reload(View.screens)
        screens = View.screens.screens

        for i, name_screen in enumerate(screens.keys()):
            model = screens[name_screen]["model"]()
            controller = screens[name_screen]["controller"](model)
            view = controller.get_view()
            view.manager_screens = self.manager_screens
            view.name = name_screen
            self.manager_screens.add_widget(view)

        self.layout = BoxLayout(orientation='vertical')
        self.layout.add_widget(top_app_bar)
        self.layout.add_widget(self.manager_screens)

        return self.layout

    def on_keyboard_down(self, window, keyboard, keycode, text, modifiers) -> None:
        """
        The method handles keyboard events.

        By default, a forced restart of an application is tied to the
        `CTRL+R` key on Windows OS and `COMMAND+R` on Mac OS.
        """

        if "meta" in modifiers or "ctrl" in modifiers and text == "r":
            self.rebuild()

    def switch_window(self, window_name: str) -> None:
        """
        Switches the application window to the specified window.
        """
        print(f"Switching to {window_name} window")
        # check if the app opened in first time
        self.manager_screens.current = window_name
        # set transition to no transition
        # self.manager_screens.transition=SlideTransition()

    def nav_drawer_open(self):
        current_screen = self.manager_screens.current_screen
        nav_drawer=current_screen.ids.nav_drawer
        nav_drawer.set_state("open")


sesampy().run()

# sesampy().run()

# After you finish the project, remove the above code and uncomment the below
# code to test the application normally without hot reloading.

# """
# The entry point to the application.
# 
# The application uses the MVC template. Adhering to the principles of clean
# architecture means ensuring that your application is easy to test, maintain,
# and modernize.
# 
# You can read more about this template at the links below:
# 
# https://github.com/HeaTTheatR/LoginAppMVC
# https://en.wikipedia.org/wiki/Model–view–controller
# """
# 
# from kivymd.app import MDApp
# from kivymd.uix.screenmanager import MDScreenManager
# 
# from View.screens import screens
# 
# 
# class sesampy(MDApp):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.load_all_kv_files(self.directory)
#         # This is the screen manager that will contain all the screens of your
#         # application.
#         self.manager_screens = MDScreenManager()
#         
#     def build(self) -> MDScreenManager:
#         self.generate_application_screens()
#         return self.manager_screens
# 
#     def generate_application_screens(self) -> None:
#         """
#         Creating and adding screens to the screen manager.
#         You should not change this cycle unnecessarily. He is self-sufficient.
# 
#         If you need to add any screen, open the `View.screens.py` module and
#         see how new screens are added according to the given application
#         architecture.
#         """
# 
#         for i, name_screen in enumerate(screens.keys()):
#             model = screens[name_screen]["model"]()
#             controller = screens[name_screen]["controller"](model)
#             view = controller.get_view()
#             view.manager_screens = self.manager_screens
#             view.name = name_screen
#             self.manager_screens.add_widget(view)
# 
# 
# sesampy().run()
