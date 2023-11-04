# pulumi-automation-utils
Collection of utilities useful for deploying [pulumi](https://www.pulumi.com/docs/) 
Infrastructure as Code. These utilities aid in configuration and creation of 
resource dependencies needed by pulumi. 

## Files

Below is a list of all of the files and an inclination for how each can be
used within your project.

### certs_and_keys.py

This file contains two functions. These are `create_key_pair` and 
`create_signed_certificate`. The `create_key_pair` function allows for the 
creation of an RSA 4096 bit public/private key pair. The 
`create_signed_certificate` function allows the user to create a signed 
certificate using an existing CA key pair. It is possible to create the CA 
key pair using the `create_key_pair` and use it as the basis for creating 
a self-signed certificate.

### common.py

This file contains any and all generic function definitions that are 
utilized when setting up the development environment to support pulumi 
deployments. These functions include:

- `parse_yaml_file` - read from a YAML file
- sending commands to the OS
- retrieving information from Azure

### environment.py

This file contains an Enum class representing each of the possible 
environment types.

### login_config.py

This file contains two classes. The first is the `LoginMode` class that is an 
Enum used to represent the options one could use for logging into Azure. The 
second is a class by the name `LoginConfig`; this class is responsible for 
maintaining all configuration associated with the deployment user including 
login status, and providing a function for allowing the user to login. The 
`LoginConfig` class takes in a single variable, the `yaml_vars` retrieved 
from the result of the `parse_yaml_file` function in `common.py`. 

The following keys can be at the root of the YAML file to be consumed by 
`LoginConfig`:
- subscription
  - (optional) The ID of the subscription in which to deploy infrastructure
- app_id
  - (optional) The Application Client ID for the service principal to login to 
    Azure
- client_secret
  - (optional) The Service Principal Client Secret to login to Azure
  - Recommend keeping the YAML configuration file safe if any sensitive 
    information is stored within
- login_mode
  - (optional) The mode for logging into Azure. Currently supported options 
    are: "interactive", "service_principal", or "managed_identity".
- tenand_id
  - (optional) The Tenant ID for the Service Principal to login to Azure

Use the `is_logged_in` function to test whether the user is currently logged 
in. The `login_to_azure` function is used to login to Azure via the login_mode 
specified. Interactive is the default login mode if one is not supplied. In 
interactive login, a URL and device code are supplied where the user can 
login from another machine to provide authorization.

### pulumi_config.py

This file is used for managing pulumi in a semi-automated fashion. The 
`PulumiConfig` class takes in the `LoginConfig` and the `yaml_vars` output via 
the `parse_yaml_file` function in `common.py`. The `PulumiConfig` object sorts
through the YAML to get all of the configuration parameters necessary to deploy 
infrastructure via pulumi. 

This class expects the following resources to be defined within the YAML configuration:
- storage_account
  - Houses storage container used for backend state management
- storage_container
  - Houses the blobs that manage backend state
- key_vault
  - Manages encryption key used for securing pulumi sensitive information

These resources are required to be configured and available at the time the 
user issues the `pulumi login` and `pulumi stack select` commands. 

## YAML Configuration

The YAML configuration is used as the basis for deploying the resources 
necessary to support deploying any pulumi project or stack in your Azure 
subscription. This YAML configuration has some rules to smoothly configure 
resources accordingly. The following lays out the structure of the overall 
YAML configuration file.

- environment
  - (required) The name of the environment (one of sandbox, zonec, zoneb, 
  zonea, or prod)
- project_name
  - (required) The name of the project to deploy. Must match the name in 
  `Pulumi.yml`
- stack_name
  - (required) The name of the stack to deploy. Anything you want 
- project_location
  - (required) The path to the directory of the pulumi project.
  - If this is not a full path, the `repo_root` must be passed to the 
  `PulumiConfig` class at creation time
- storage_account
  - (required) The configuration object that specifies information about the 
  storage account used with pulumi
  - resource_group
    - (optional) The name of the resource group that the Azure Key Vault 
    resides in
  - storage_container
    - (required) The configuration block of the Storage Account Blob Container 
    that is used with pulumi
    - name
      - (required) The name of the Storage Account Blob Container
  - sas_token
    - (optional) The configuration block of the SAS token to be created/used 
    with pulumi to access Storage Account Blob Container
    - name 
      - (required) If this block is declared, the name of the SAS token must be
      declared
- key_vault
  - (required) The configuration object that specifies information about the 
  Azure Key Vault used with pulumi
  - resource_group
    - (optional) The name of the resource group that the Azure Key Vault 
    resides in
- pulumi
  - (required) Configuration block that contains a dictionary of all the 
  configuration parameters required by your pulumi scripts
  - If no resource_group_name is specified, the first resource group returned 
  in the list from the subscription will be used for resource_group_name and 
  resource_group_id config items
  - If no storage_account_name is specified, the storage account from the 
  config above will be used for the storage_account_name and storage_account_id
  config items
  - If no key_vault_name is specified, the key vault name and ID from the 
  config above will be used for the key_vault_name and key_vault_id config 
  items
- pulumi-secrets
  - (optional) Configuration block that contains key/value pairs of all the 
  secret configuration parameters required by your pulumi scripts