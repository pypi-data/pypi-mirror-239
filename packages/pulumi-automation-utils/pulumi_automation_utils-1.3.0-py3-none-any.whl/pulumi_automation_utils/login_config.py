#!/usr/bin/env python3
from enum import Enum
import subprocess
import json

from pulumi_automation_utils import common
from pulumi_automation_utils.environment import Environment

class LoginMode(Enum):
    INTERACTIVE = 1
    SERVICE_PRINCIPAL = 2
    MANAGED_IDENTITY = 3

class LoginConfig:
    def __init__(self, yaml_vars):
        self.logged_in = False
        self.initialized = False
        self.__set_cloud_name(yaml_vars) # should be either public or AzureUSGovernment

        # Set the login mode from the yaml inputs
        self.__set_login_mode(yaml_vars)

        self.subscription = None
        if "subscription" in yaml_vars.keys():
            self.subscription = yaml_vars["subscription"]
        self.app_id = None
        if "app_id" in yaml_vars.keys():
            self.app_id = yaml_vars["app_id"]
        self.client_secret = None
        if "client_secret" in yaml_vars.keys():
            self.client_secret = yaml_vars["client_secret"]
        self.tenant_id = None
        if "tenant_id" in yaml_vars.keys():
            self.tenant_id = yaml_vars["tenant_id"]

    def get_app_id(self):
        return self.app_id
    
    def get_client_secret(self):
        return self.client_secret

    def get_cloud_name(self):
        return self.cloud_name
    
    def is_logged_in(self):
        if self.initialized:
            try:
                output = json.loads(common.sanitize_stdout_for_json(common.send_os_command("az account show", is_secret=True)))
                if self.get_subscription() is None:
                    if type(output) is dict and "isDefault" in output and output["isDefault"] is True:
                        if "cloudName" in output:
                            self.set_cloud_name(output["cloudName"])
                        if "id" in output:
                            self.set_subscription(output["id"])
                        if "tenantId" in output:
                            self.set_tenant_id(output["tenantId"])
                else:
                    common.send_os_command("az account set --subscription " + self.subscription, is_secret=True)
                self.logged_in = True
            except subprocess.CalledProcessError as e:
                print("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
                self.logged_in = False

        return self.logged_in

    def get_login_mode(self):
        return self.login_mode

    def get_subscription(self):
        return self.subscription
    
    def get_tenant_id(self):
        return self.tenant_id
    
    # TODO: Make this into an ENUM
    def set_cloud_name(self, cloud_name : str):
        self.cloud_name = cloud_name
    
    def set_subscription(self, subscription : str):
        self.subscription = subscription

    def set_tenant_id(self, tenant_id : str):
        self.tenant_id = tenant_id

    def login_to_azure(self):
        if not self.logged_in:
            if self.get_login_mode() is LoginMode.INTERACTIVE:
                if self.is_logged_in():
                    try:
                        common.send_os_command("az logout")
                    except subprocess.CalledProcessError as e:
                        print("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
                        print("No user logged into az cli. Logging in now...")
                try:
                    common.send_os_command("az cloud set --name " + self.cloud_name)

                    output = json.loads(common.sanitize_stdout_for_json(common.send_os_command("az login --use-device-code")))
                    if self.get_subscription() is None:
                        for account in output:
                            if type(account) is dict and "isDefault" in account and account["isDefault"] is True:
                                if "id" in account:
                                    self.set_subscription(account["id"])
                                if "tenantId" in account:
                                    self.set_tenant_id(account["tenantId"])
                    else:
                        common.send_os_command("az account set --subscription " + self.subscription)
                    
                    self.logged_in = True
                    self.initialized = True
                except subprocess.CalledProcessError as e:
                    print("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
                    exit()
            else:
                print("This login mode is not yet ")
        else:
            print("Already logged in, nothing to do.")

    def __set_cloud_name(self, yaml_vars):
        self.cloud_name = None
        if "environment" in yaml_vars:
            environment = Environment.SANDBOX
            if type(yaml_vars) is dict:
                if "environment" in yaml_vars:
                    if yaml_vars["environment"].lower() == "zonec":
                        environment = Environment.ZONEC
                    if yaml_vars["environment"].lower() == "zoneb":
                        environment = Environment.ZONEB
                    if yaml_vars["environment"].lower() == "zonea":
                        environment = Environment.ZONEA
                    if yaml_vars["environment"].lower() == "prod":
                        environment = Environment.PROD
            if environment == Environment.SANDBOX:
                self.cloud_name = "AzureCloud"
            else:
                self.cloud_name = "AzureUSGovernment"

    def __set_login_mode(self, yaml_vars):
        self.login_mode = LoginMode.INTERACTIVE
        if type(yaml_vars) is dict and yaml_vars["login_mode"]:
            if yaml_vars["login_mode"] == "interactive":
                self.login_mode = LoginMode.INTERACTIVE
            elif yaml_vars["login_mode"] == "service_principal":
                self.login_mode = LoginMode.SERVICE_PRINCIPAL
            elif yaml_vars["login_mode"] == "managed_identity":
                self.login_mode = LoginMode.MANAGED_IDENTITY