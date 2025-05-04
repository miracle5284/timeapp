# save as upload_env_to_vault.py

import os
import sys
from dotenv import load_dotenv, dotenv_values
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.keyvault.models import (
    VaultCreateOrUpdateParameters,
    Sku,
    AccessPolicyEntry,
    Permissions,
    SecretPermissions,
    NetworkRuleSet,
    VaultProperties
)
load_dotenv()

# CONFIGURATION
VAULT_NAME = os.getenv('VAULT_VAULT_NAME')  # e.g., "chrona-vault-prod"
VAULT_FP = os.getenv('VAULT_FP')
OBJECT_ID = os.getenv('VAULT_AZURE_OBJECT_ID')
RESOURCE_GROUP_NAME = os.getenv('VAULT_RESOURCE_GROUP_NAME')  # e.g., "chrona-prod-rg"
AZURE_TENANT_ID = os.getenv('VAULT_AZURE_TENANT_ID')  # e.g., "chrona-prod-rg"
LOCATION = os.getenv('VAULT_LOCATION', 'eastus')  # default location if not set

if not VAULT_NAME or not RESOURCE_GROUP_NAME:
    print("❌ VAULT_NAME and RESOURCE_GROUP_NAME must be set as environment variables.")
    sys.exit(1)

credential = DefaultAzureCredential()
subscription_id = os.getenv('VAULT_AZURE_SUBSCRIPTION_ID')  # you must export this too
if not subscription_id:
    print("❌ AZURE_SUBSCRIPTION_ID must be set as environment variable.")
    sys.exit(1)

kv_mgmt_client = KeyVaultManagementClient(credential, subscription_id)
resource_client = ResourceManagementClient(credential, subscription_id)

try:
    rg = resource_client.resource_groups.get(RESOURCE_GROUP_NAME)
except Exception:
    print(f"❌ Resource Group '{RESOURCE_GROUP_NAME}' does not exist. Please create it first.")
    sys.exit(1)

vault_exists = False
for vault in kv_mgmt_client.vaults.list_by_resource_group(RESOURCE_GROUP_NAME):
    if vault.name.lower() == VAULT_NAME.lower():
        vault_exists = True
        print(f"✅ Vault '{VAULT_NAME}' already exists.")
        break
if not vault_exists:
    print(f"⚙️ Vault '{VAULT_NAME}' does not exist. Creating...")

    access_policies = [
        AccessPolicyEntry(
            tenant_id=AZURE_TENANT_ID,
            object_id=OBJECT_ID,
            permissions=Permissions(
                secrets=[
                    SecretPermissions.get,
                    SecretPermissions.list,
                    SecretPermissions.set,
                    SecretPermissions.delete
                ]
            )
        )
    ]

    vault_properties = VaultProperties(
        tenant_id=AZURE_TENANT_ID,
        sku=Sku(name="standard", family="A"),
        access_policies=access_policies,
        enabled_for_deployment=True,
        enabled_for_disk_encryption=True,
        enabled_for_template_deployment=True,
        network_acls=NetworkRuleSet(bypass="AzureServices", default_action="Allow")
    )
    # Create minimal Vault
    vault_params = VaultCreateOrUpdateParameters(
        location=LOCATION,
        properties=vault_properties
    )

    kv_mgmt_client.vaults.begin_create_or_update(RESOURCE_GROUP_NAME, VAULT_NAME, vault_params).result()
    print(f"✅ Vault '{VAULT_NAME}' created successfully.")

# Upload secrets from .env file
vault_url = f"https://{VAULT_NAME}.vault.azure.net"
client = SecretClient(vault_url=vault_url, credential=credential)

env_vars = dotenv_values()
for key, value in env_vars.items():
    if key.startswith("VAULT") or key is None:
        continue

    key = key.replace("_", "-")
    print(f"Uploading {key}...")
    client.set_secret(key, value)

print("✅ All secrets uploaded successfully to Azure Key Vault!")