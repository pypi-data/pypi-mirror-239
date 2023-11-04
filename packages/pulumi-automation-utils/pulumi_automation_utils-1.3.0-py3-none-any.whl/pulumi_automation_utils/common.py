#!/usr/bin/env python3
from datetime import datetime, timedelta
import json
import os
import subprocess
import yaml

from pulumi_automation_utils.login_config import LoginConfig

def parse_yaml_file(filepath : str):
    print("Parsing YAML file: " + filepath)
    if filepath and os.path.isfile(filepath) and os.path.exists(filepath):
        with open(filepath, 'r') as yaml_file:
            return yaml.safe_load(yaml_file)
    else:
        print("YAML file provided does not exist. Exiting...")
        exit()

def sanitize_stdout_for_json(std_out : list[str]):
    json_started = False
    json_lines = []
    for line in std_out:
        if line.startswith('[', 0, 1) or line.startswith('{', 0, 1):
            json_started = True
            json_lines.append(line)
        elif (line.startswith(']') or line.startswith('}')) and not line.startswith((' ', '\t')):
            json_lines.append(line)
            json_started = False
        elif json_started:
            json_lines.append(line)
    return "".join(json_lines)

def send_os_command(command : str, cwd : str=os.getcwd(), env : dict=os.environ.copy(), shell : bool=True, is_secret : bool=False) -> str:
    all_stdout = []
    if not is_secret:
        print(command)
    if shell:
        process_command = command
    else:
        process_command = command.split()
    popen = subprocess.Popen(
        process_command, 
        stdout=subprocess.PIPE, 
        env=env, 
        cwd=cwd, 
        shell=shell, 
        universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        if not is_secret:
            print(stdout_line, end="")
        all_stdout.append(stdout_line)
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, command)
    return all_stdout 

def get_resource_group_from_subscription(login_config : LoginConfig):
    if login_config:
        print("Getting the resource group information from the subscription")
        if not login_config.is_logged_in():
            login_config.login_to_azure()
        az_cli_command = "az group list --subscription " + login_config.get_subscription() 
        output = json.loads(sanitize_stdout_for_json(send_os_command(az_cli_command, is_secret=True)))
        for rg in output:
            if "name" in rg.keys():
                return rg["name"]
        return None
    else:
        print("ERROR: Could not get resource group from Azure Subscription. One of the following variables was not defined")
        print("login_config: " + login_config)
        exit()

def get_location_from_resource_group(login_config : LoginConfig, resource_group : str):
    if login_config and resource_group:
        print("Getting the resource group information from the resource group: " + resource_group)
        if not login_config.is_logged_in():
            login_config.login_to_azure()
        az_cli_command = "az group show --resource-group " + resource_group 
        output = json.loads(sanitize_stdout_for_json(send_os_command(az_cli_command, is_secret=True)))
        if "location" in output.keys():
            return output["location"]
        else:
            return None
    else:
        print("ERROR: Could not get location from Azure Resource Group. One of the following variables was not defined")
        print("login_config: " + login_config)
        print("resource_group: " + resource_group)
        exit()

def get_key_vault_id(login_config : LoginConfig, key_vault_name : str):
    if login_config and key_vault_name:
        az_cli_command = "az keyvault show --name " + key_vault_name
        output = json.loads(sanitize_stdout_for_json(send_os_command(az_cli_command, is_secret=True)))
        if "id" in output:
            return output["id"]
        else:
            return None
    else: 
        print("ERROR: Could not get location from Azure Resource Group. One of the following variables was not defined")
        print("login_config: " + login_config)
        print("key_vault_name: " + key_vault_name)
        exit()

def get_key_vault_resource_group(login_config : LoginConfig, key_vault_name : str):
    if login_config and key_vault_name:
        az_cli_command = "az keyvault show --name " + key_vault_name
        output = json.loads(sanitize_stdout_for_json(send_os_command(az_cli_command, is_secret=True)))
        if "resourceGroup" in output:
            return output["resourceGroup"]
        else:
            return None
    else: 
        print("ERROR: Could not get location from Azure Resource Group. One of the following variables was not defined")
        print("login_config: " + login_config)
        print("key_vault_name: " + key_vault_name)
        exit()

def get_secret_from_key_vault(login_config : LoginConfig, key_vault_name: str, secret_name : str):
    if login_config and secret_name and key_vault_name:
        secret_value = None
        print("Getting secret " + secret_name + " from Azure Key Vault " + key_vault_name + ".")
        if not login_config.is_logged_in():
            login_config.login_to_azure()
        if does_key_vault_exist(login_config=login_config, key_vault_name=key_vault_name):
            try:
                az_cli_command = "az keyvault secret show --name " + secret_name + " --vault-name " + key_vault_name
                output = json.loads(sanitize_stdout_for_json(send_os_command(az_cli_command, is_secret=True)))
                if "value" in output:
                    if "attributes" in output and "enabled" in output["attributes"]:
                        if "expires" in output["attributes"]:
                            expiration_date = output["attributes"]["expires"]
                            if expiration_date is not None and expiration_date != "null":
                                expiration_date = datetime.strptime(output["attributes"]["expires"], '%Y-%m-%dT%H:%M:%S+00:00').date()
                                if output["attributes"]["enabled"] == True and expiration_date > datetime.now().date():
                                    secret_value = str(output["value"]).strip().replace('"', '')
                            elif output["attributes"]["enabled"] == True:
                                secret_value = str(output["value"]).strip().replace('"', '')

            except subprocess.CalledProcessError:
                print("Unable to retrieve secret " + secret_name + " from Azure Key Vault " + key_vault_name)
        else:
            print("Azure Key Vault " + key_vault_name + " does not exist. Cannot get secret. Exiting...")
            exit()
        return secret_value
    else:
        print("ERROR: Could not get secret from Azure Key Vault. One of the following variables was not defined")
        print("login_config: " + login_config)
        print("secret_name: " + secret_name)
        print("key_vault_name" + key_vault_name)
        exit()

def upload_secret_file_to_key_vault(login_config : LoginConfig, filename : str, key_vault_name : str):
    if login_config and filename and key_vault_name:
        print("Uploading secret filename: " + filename + " to Azure Key Vault: " + key_vault_name)
        if not login_config.is_logged_in():
            login_config.login_to_azure()
        if os.path.exists(filename):
            if does_key_vault_exist(login_config=login_config, key_vault_name=key_vault_name):
                base_name = os.path.basename(filename).replace("_", "-").replace(".", "-dot-")
                az_cli_command = "az keyvault secret set --name " + base_name + " --vault-name " + key_vault_name + " --encoding ascii --file " + filename
                output = sanitize_stdout_for_json(send_os_command(command=az_cli_command, is_secret=True))
                return base_name
            else:
                print("Azure Key Vault " + key_vault_name + " does not exist. Cannot upload secret. Exiting...")
                exit()
        else:
            print("File provided does not exist: " + filename)
            exit
    else:
        print("ERROR: Could not upload secret to Azure Key Vault. One of the following variables was not defined")
        print("login_config: " + login_config)
        print("filename: " + filename)
        print("key_vault_name" + key_vault_name)
        exit()
    
def does_key_vault_exist(login_config : LoginConfig, key_vault_name : str):
    if login_config and key_vault_name:
        if not login_config.is_logged_in():
            login_config.login_to_azure()
        key_vault_exists = False
        try:
            tries = 0
            while not key_vault_exists and tries < 3:
                az_cli_command = "az keyvault list"
                output = json.loads(sanitize_stdout_for_json(send_os_command(az_cli_command, is_secret=False)))
                for kv in output:
                    if kv["name"] == key_vault_name:
                        key_vault_exists = True
                        break
                tries = tries + 1
        except subprocess.CalledProcessError as e:
            print("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
            print("Cannot determine if a key vault with the name " + key_vault_name + " exists in the subscription. Exiting...")
        return key_vault_exists
    else:
        print("One of the following variables was not defined. Exiting...")
        print("key_vault_name: " + str(key_vault_name))
        exit()

def get_storage_account_id(login_config : LoginConfig, storage_account_name : str):
    if login_config and storage_account_name:
        if not login_config.is_logged_in():
            login_config.login_to_azure()
        az_cli_command = "az storage account list"
        output = json.loads(sanitize_stdout_for_json(send_os_command(az_cli_command, is_secret=True)))
        for account in output:
            if "name" in account and account["name"] == storage_account_name:
                if "id" in account:
                    return account["id"]
        return None        
    else:
        print("ERROR: Could not get Storage Account ID. One of the following variables was not defined")
        print("login_config: " + login_config)
        print("storage_account_name: " + storage_account_name)

def get_storage_account_resource_group(login_config : LoginConfig, storage_account_name : str):
    if login_config and storage_account_name:
        if not login_config.is_logged_in():
            login_config.login_to_azure()
        az_cli_command = "az storage account list"
        output = json.loads(sanitize_stdout_for_json(send_os_command(az_cli_command, is_secret=True)))
        for account in output:
            if "name" in account and account["name"] == storage_account_name:
                if "resourceGroup" in account:
                    return account["resourceGroup"]
        return None        
    else:
        print("ERROR: Could not get Storage Account Resource Group. One of the following variables was not defined")
        print("login_config: " + login_config)
        print("storage_account_name: " + storage_account_name)

def get_storage_account_key(login_config : LoginConfig, storage_account_name : str):
    if login_config and storage_account_name:
        if not login_config.is_logged_in():
            login_config.login_to_azure()
        az_cli_command = "az storage account keys list --account-name " + storage_account_name
        output = json.loads(sanitize_stdout_for_json(send_os_command(az_cli_command, is_secret=True)))
        for key in output:
            if "value" in key:
                return key["value"]
    return None

def get_sas_token(login_config : LoginConfig, storage_account_name : str, storage_container_name : str, expiration_date : str=(datetime.utcnow() + timedelta(days=7)).date().strftime("%Y-%m-%d")):
    if login_config and storage_account_name and storage_container_name:
        if not login_config.is_logged_in():
            login_config.login_to_azure()
        storage_key = get_storage_account_key(login_config=login_config, storage_account_name=storage_account_name)
        if storage_key is not None:
            start_date = datetime.utcnow().date().strftime("%Y-%m-%d")
            az_cli_command = "az storage container generate-sas --account-name " + storage_account_name + " --name " + storage_container_name + " --permissions acdlrw --start " + start_date + " --expiry " + expiration_date + " --https-only --account-key " + storage_key
            sas_token = send_os_command(az_cli_command, is_secret=True)
            return ("".join(sas_token)).strip().replace('"', '')
        else:
            print("Could not retrieve the storage account key. Exiting...")
            exit()
    else:
        print("One of the following variables was not defined. Exiting...")
        print("storage_account_name: " + str(storage_account_name))
        print("storage_container_name: " + str(storage_container_name))
        exit()

def create_storage_account_container(login_config : LoginConfig, storage_account_resource_group_name: str, storage_account_name : str, storage_container_name : str):
    if login_config and storage_account_resource_group_name and storage_account_name and storage_container_name:
        if not login_config.is_logged_in():
            login_config.login_to_azure()
        az_cli_command = "az storage container exists --account-name " + storage_account_name + " --auth-mode login --name " + storage_container_name
        output = json.loads(sanitize_stdout_for_json(send_os_command(az_cli_command)))
        container_exists = False
        if "exists" in output and output["exists"] == True:
            print("Storage container " + storage_container_name + " in storage account " + storage_account_name + " already exists. Nothing to do.")
            container_exists = True
        if not container_exists:
            print("Creating storage container " + storage_container_name + " in storage account " + storage_account_name + ".")
            az_cli_command = "az storage container create --account-name " + storage_account_name + " --name " + storage_container_name + " --auth-mode login"
            output = send_os_command(az_cli_command)
    else:
        print("One of the following variables was not defined. Exiting...")
        print("storage_account_resource_group_name: " + str(storage_account_resource_group_name))
        print("storage_account_name: " + str(storage_account_name))
        print("storage_container_name: " + str(storage_container_name))
        exit()

def upload_blob_to_storage_account(login_config : LoginConfig, 
                                   storage_account_name : str, 
                                   storage_account_container : str, 
                                   blob_name : str, 
                                   local_filepath : str):
    if login_config and storage_account_name and storage_account_container and blob_name and local_filepath:
        upload_to_azure = False
        az_cli_command = "az storage blob show --account-name " + storage_account_name + " --container-name " + storage_account_container + " --name " + blob_name
        try:
            output = json.loads(sanitize_stdout_for_json(send_os_command(az_cli_command, is_secret=True)))
            if input("Would you like to overwrite the existing Azure blob? [y/n]: ") == "y":
                upload_to_azure = True
            else:
                print("Skipping upload of " + blob_name + " blob to Azure Storage Account " + storage_account_name + ". Continuing...")
        except subprocess.CalledProcessError:
            upload_to_azure = True
            print("Need to upload " + blob_name + " blob to Azure Storage Account " + storage_account_name + ".")
        if upload_to_azure:
            if os.path.exists(local_filepath):
                # Get the SAS for the Storage Account
                sas_token = get_sas_token(login_config=login_config,
                            storage_account_name=storage_account_name,
                            storage_container_name=storage_account_container)

                # Get the storage account URL
                az_cli_command = "az storage account show --name " + storage_account_name + " --resource-group " + get_storage_account_resource_group(login_config=login_config, storage_account_name=storage_account_name)
                output = json.loads(sanitize_stdout_for_json(send_os_command(az_cli_command, is_secret=True)))
                blob_url = None
                if "primaryEndpoints" in output:
                    if "blob" in output["primaryEndpoints"]:
                        blob_url = output["primaryEndpoints"]["blob"]
                
                if blob_url is not None:
                    upload_url = blob_url + storage_account_container + "/" + blob_name + "?" + sas_token
                    azcopy_command = "azcopy copy '" + local_filepath + "' '" + upload_url + "'"
                    output = send_os_command(azcopy_command, shell=True, env=os.environ.copy())
                
                else:
                    print("Blob URL is invalid. Cannot proceed. Exiting...")
                    exit()

            else:
                print("The blob to upload does not exist at " + local_filepath + " Exiting...")
                exit()
    else:
        print("One of the following variables was not defined. Exiting...")
        print("storage_account_name: " + str(storage_account_name))
        print("storage_container_name: " + str(storage_account_container))
        print("blob_name: " + str(blob_name))
        print("local_filepath: " + str(local_filepath))
        exit()