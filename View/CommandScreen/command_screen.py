import threading
import logging

import time
import sys,stat
from kivy.clock import mainthread
from kivymd.uix.spinner import MDSpinner

from constants import ROOT_DIR
from core.sesam_func import start_cli

from View.base_screen import BaseScreenView
from Model.main_screen import MainScreenModel
from Model.connector_screen import ConnectorScreenModel as connector_model
import os
import subprocess




class CommandScreenView(BaseScreenView):
    def on_pre_leave(self, *args):
        os.chdir(ROOT_DIR)
    def on_enter(self, *args):

        """
        Called whenever the screen is entered.
        """
        os.chdir("core")
        self.current_connector = connector_model.current_connector
        self.args_dict = {'version': False, 'verbose': False, 'extra_verbose': True, 'extra_extra_verbose': False,
                          'skip_tls_verification': False, 'sync_config_file': '.syncconfig', 'whitelist_file': None,
                          'dont_remove_scheduler': False, 'dump': False, 'print_scheduler_log': False,
                          'output_run_statistics': False, 'use_internal_scheduler': False, 'custom_scheduler': False,
                          'scheduler_image_tag': None, 'scheduler_mode': None, 'node': None, 'scheduler_node': None,
                          'jwt': None, 'single': None, 'no_large_int_bugs': False, 'disable_user_pipes': False,
                          'enable_eager_ms': False, 'enable_user_pipes': False, 'compact_execution_datasets': False,
                          'disable_cpp_extensions': False, 'unicode_encoding': False, 'disable_json_html_escape': False,
                          'profile': 'test', 'scheduler_id': None, 'scheduler_request_mode': 'sync',
                          'scheduler_zero_runs': 2, 'scheduler_max_runs': 100, 'scheduler_max_run_time': 900,
                          'scheduler_check_input_pipes': False, 'restart_timeout': 900, 'runs': 1, 'logformat': 'short',
                          'scheduler_poll_frequency': 5000, 'sesamconfig_file': None, 'diff': False,
                          'add_test_entities': False, 'force_add': False, 'command': 'download', 'force': False,
                          'system_placeholder': 'xxxxxx', 'connector_dir': 'tripletex-connector',
                          'expanded_dir': '.expanded', 'client_id': None, 'client_secret': None, 'service_url': None,
                          'service_jwt': None, 'consumer_token': None, 'employee_token': None,
                          'base_url': 'https://api.tripletex.io', 'days': 10}

    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """

    ######################################################################

    @mainthread
    def spinner_authenticate_toggle(self):
        if not self.ids.spinner_authenticate.active:
            self.ids.spinner_authenticate.active = True
        else:
            self.ids.spinner_authenticate.active = False
            self.ids.log.text = self.logs
            self.ids.logs.badge_icon = "numeric-1"
    def authenticate(self):
        self.args_dict["command"] = "authenticate"
        self.args_dict["connector_dir"] = f"{self.current_connector}-connector"
        start_cli(self.args_dict)
        os.chdir(os.path.join(ROOT_DIR, "core"))
        with open('output.log', 'r') as f:
            self.logs = f.read()
        self.spinner_download_toggle()

    def authenticate_thread(self):
        self.spinner_authenticate_toggle()
        threading.Thread(target=(self.authenticate)).start()

    @mainthread
    def spinner_download_toggle(self):
        if not self.ids.spinner_download.active:
            self.ids.spinner_download.active = True
        else:
            self.ids.spinner_download.active = False
            self.ids.log.text = self.logs
            self.ids.logs.badge_icon = "numeric-1"
    def download(self):
        self.args_dict["command"] = "download"
        self.args_dict["connector_dir"] = f"{self.current_connector}-connector"
        start_cli(self.args_dict)
        os.chdir(os.path.join(ROOT_DIR,"core"))
        with open('output.log', 'r') as f:
            self.logs = f.read()
        self.spinner_download_toggle()

    def download_thread(self):
        self.spinner_download_toggle()
        threading.Thread(target=(self.download)).start()

    @mainthread
    def spinner_upload_toggle(self):
        logging.basicConfig(filename='example.log', level=logging.DEBUG)
        if not self.ids.spinner_upload.active:
            self.ids.spinner_upload.active = True
        else:
            self.ids.spinner_upload.active = False
            self.ids.log.text = self.logs
            self.ids.logs.badge_icon = "numeric-1"
    def upload(self):
        self.args_dict["command"] = "upload"
        self.args_dict["connector_dir"] = f"{self.current_connector}-connector"
        start_cli(self.args_dict)
        os.chdir(os.path.join(ROOT_DIR, "core"))
        with open('output.log', 'r') as f:
            self.logs = f.read()
        self.spinner_upload_toggle()
    def upload_thread(self):
        self.spinner_upload_toggle()
        threading.Thread(target=(self.upload)).start()

    @mainthread
    def spinner_status_toggle(self):
        if not self.ids.spinner_status.active:
            self.ids.spinner_status.active = True
        else:
            self.ids.spinner_status.active = False
            self.ids.log.text = self.logs
            self.ids.logs.badge_icon = "numeric-1"
    def status(self):
        self.args_dict["command"] = "status"
        self.args_dict["connector_dir"] = f"{self.current_connector}-connector"
        start_cli(self.args_dict)
        os.chdir(os.path.join(ROOT_DIR, "core"))
        with open('output.log', 'r') as f:
            self.logs = f.read()
        self.spinner_status_toggle()
    def status_thread(self):
        self.spinner_status_toggle()
        threading.Thread(target=(self.status)).start()

    @mainthread
    def spinner_verify_toggle(self):
        if not self.ids.spinner_verify.active:
            self.ids.spinner_verify.active = True
        else:
            self.ids.spinner_verify.active = False
            self.ids.log.text = self.logs
            self.ids.logs.badge_icon = "numeric-1"

    def verify(self):
        self.args_dict["command"] = "verify"
        self.args_dict["connector_dir"] = f"{self.current_connector}-connector"
        start_cli(self.args_dict)
        os.chdir(os.path.join(ROOT_DIR, "core"))
        with open('output.log', 'r') as f:
            self.logs = f.read()
        self.spinner_verify_toggle()

    def verify_thread(self):
        self.spinner_verify_toggle()
        threading.Thread(target=(self.verify)).start()

    @mainthread
    def spinner_test_toggle(self):
        if not self.ids.spinner_test.active:
            self.ids.spinner_test.active = True
        else:
            self.ids.spinner_test.active = False
            self.ids.log.text = self.logs
            self.ids.logs.badge_icon = "numeric-1"
    def test(self):
        self.args_dict["command"] = "test"
        self.args_dict["connector_dir"] = f"{self.current_connector}-connector"
        start_cli(self.args_dict)
        os.chdir(os.path.join(ROOT_DIR, "core"))
        with open('output.log', 'r') as f:
            self.logs = f.read()
        self.spinner_test_toggle()
    def test_thread(self):
        self.spinner_test_toggle()
        threading.Thread(target=(self.test)).start()


    @mainthread
    def spinner_stop_toggle(self):
        if not self.ids.spinner_stop.active:
            self.ids.spinner_stop.active = True
        else:
            self.ids.spinner_stop.active = False
            self.ids.log.text = self.logs
            self.ids.logs.badge_icon = "numeric-1"
    def stop(self):
        self.args_dict["command"] = "stop"
        self.args_dict["connector_dir"] = f"{self.current_connector}-connector"
        start_cli(self.args_dict)
        os.chdir(os.path.join(ROOT_DIR, "core"))
        with open('output.log', 'r') as f:
            self.logs = f.read()
        self.spinner_stop_toggle()
    def stop_thread(self):
        self.spinner_stop_toggle()
        threading.Thread(target=(self.stop)).start()

    @mainthread
    def spinner_run_toggle(self):
        if not self.ids.spinner_run.active:
            self.ids.spinner_run.active = True
        else:
            self.ids.spinner_run.active = False
            self.ids.log.text = self.logs
            self.ids.logs.badge_icon = "numeric-1"
    def run(self):
        self.args_dict["command"] = "run"
        self.args_dict["connector_dir"] = f"{self.current_connector}-connector"
        start_cli(self.args_dict)
        os.chdir(os.path.join(ROOT_DIR, "core"))
        with open('output.log', 'r') as f:
            self.logs = f.read()
        self.spinner_run_toggle()
    def run_thread(self):
        self.spinner_run_toggle()
        threading.Thread(target=(self.run)).start()

    @mainthread
    def spinner_wipe_toggle(self):
        if not self.ids.spinner_wipe.active:
            self.ids.spinner_wipe.active = True
        else:
            self.ids.spinner_wipe.active = False
            self.ids.log.text = self.logs
            self.ids.logs.badge_icon = "numeric-1"
    def wipe(self):
        self.args_dict["command"] = "wipe"
        self.args_dict["connector_dir"] = f"{self.current_connector}-connector"
        start_cli(self.args_dict)
        os.chdir(os.path.join(ROOT_DIR, "core"))
        with open('output.log', 'r') as f:
            self.logs = f.read()
        self.spinner_run_toggle()
    def wipe_thread(self):
        self.spinner_wipe_toggle()
        threading.Thread(target=(self.wipe)).start()

    @mainthread
    def spinner_restart_toggle(self):
        if not self.ids.spinner_restart.active:
            self.ids.spinner_restart.active = True
        else:
            self.ids.spinner_restart.active = False
            self.ids.log.text = self.logs
            self.ids.logs.badge_icon = "numeric-1"
    def restart(self):
        self.args_dict["command"] = "restart"
        self.args_dict["connector_dir"] = f"{self.current_connector}-connector"
        start_cli(self.args_dict)
        os.chdir(os.path.join(ROOT_DIR, "core"))
        with open('output.log', 'r') as f:
            self.logs = f.read()
        self.spinner_restart_toggle()
    def restart_thread(self):
        self.spinner_restart_toggle()
        threading.Thread(target=(self.restart)).start()

    @mainthread
    def spinner_reset_toggle(self):
        if not self.ids.spinner_reset.active:
            self.ids.spinner_reset.active = True
        else:
            self.ids.spinner_reset.active = False
            self.ids.log.text = self.logs
            self.ids.logs.badge_icon = "numeric-1"
    def reset(self):
        self.args_dict["command"] = "reset"
        self.args_dict["connector_dir"] = f"{self.current_connector}-connector"
        start_cli(self.args_dict)
        os.chdir(os.path.join(ROOT_DIR, "core"))
        with open('output.log', 'r') as f:
            self.logs = f.read()
        self.spinner_run_toggle()
    def reset_thread(self):
        self.spinner_reset_toggle()
        threading.Thread(target=(self.reset)).start()

    @mainthread
    def spinner_convert_toggle(self):
        if not self.ids.spinner_convert.active:
            self.ids.spinner_convert.active = True
        else:
            self.ids.spinner_convert.active = False
            self.ids.log.text = self.logs
            self.ids.logs.badge_icon = "numeric-1"
    def convert(self):
        self.args_dict["command"] = "convert"
        self.args_dict["connector_dir"] = f"{self.current_connector}-connector"
        start_cli(self.args_dict)
        os.chdir(os.path.join(ROOT_DIR, "core"))
        with open('output.log', 'r') as f:
            self.logs = f.read()
        self.spinner_convert_toggle()
    def convert_thread(self):
        self.spinner_convert_toggle()
        threading.Thread(target=(self.convert)).start()

    @mainthread
    def spinner_dump_toggle(self):
        if not self.ids.spinner_dump.active:
            self.ids.spinner_dump.active = True
        else:
            self.ids.spinner_dump.active = False
            self.ids.log.text = self.logs
            self.ids.logs.badge_icon = "numeric-1"
    def dump(self):
        self.args_dict["command"] = "dump"
        self.args_dict["connector_dir"] = f"{self.current_connector}-connector"
        start_cli(self.args_dict)
        os.chdir(os.path.join(ROOT_DIR, "core"))
        with open('output.log', 'r') as f:
            self.logs = f.read()
        self.spinner_dump_toggle()
    def dump_thread(self):
        self.spinner_dump_toggle()
        threading.Thread(target=(self.dump)).start()


    def get_logs(self, *args) -> None:
        # remove the badge
        self.ids.logs.badge_icon = ""
