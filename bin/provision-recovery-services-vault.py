"""
Copyright 2017 CGI Group Inc.

This file is part of Azure Python Scripts.

Azure Python Scripts is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Azure Python Scripts is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Azure Python Scripts.  If not, see <http://www.gnu.org/licenses/>.
"""

import argparse
import time

import authorization
import resource_group
import session
from compute import virtual_machines
from recovery_services import backup_policies, backup_protectable_items, backup_protected_items, vaults


def filter_items_with_vm_names(items, vm_names):
    return (item
            for item in items
            if item['properties']['friendlyName'].lower() in vm_names)


def get_protectable_items_to_backup(subscription_id,
                                    resource_group_name,
                                    vault_name,
                                    vm_names_to_backup,
                                    request_session):
    return filter_items_with_vm_names(
        backup_protectable_items.get_protectable_items_in_resource_group(subscription_id,
                                                                         resource_group_name,
                                                                         vault_name,
                                                                         request_session),
        vm_names_to_backup
    )


def get_protected_items_to_backup(subscription_id,
                                  resource_group_name,
                                  vault_name,
                                  vm_names_to_backup,
                                  request_session):
    return filter_items_with_vm_names(
        backup_protected_items.get_protected_items_in_resource_group(subscription_id, resource_group_name,
                                                                     vault_name, request_session),
        vm_names_to_backup
    )


def main(client_id,
         client_secret,
         tenant_id,
         subscription_id,
         resource_group_name,
         vault_name):
    access_token = authorization.retrieve_access_token(client_id, client_secret, tenant_id)
    request_session = session.create_request_session(access_token)

    resource_group_location = resource_group.get_resource_group_location(request_session,
                                                                         resource_group_name,
                                                                         subscription_id)
    print("Resource group name:", resource_group_name)
    print("Resource group location:", resource_group_location)

    print("Creating/updating recovery vault:", vault_name)
    vaults.create_vault(subscription_id, resource_group_name, resource_group_location, vault_name, request_session)

    print("Detecting which Virtual Machines are configured for backup ... ", end='')
    # Convert all VM names to lowercase for comparison,
    # The value returned from some APIs has inconsistent casing
    vm_names_to_backup = {
        virtual_machine['name'].lower()
        for virtual_machine in virtual_machines.get_vms_in_resource_group_to_backup(subscription_id,
                                                                                    resource_group_name,
                                                                                    request_session)
        }

    print(vm_names_to_backup)

    protectable_items_to_backup = []
    total_vms = len(vm_names_to_backup)
    num_protectable = 0
    num_protected = 0
    vault_ready = False
    # Even though the vault returns successful provisioning status,
    # some items are not yet available to be protected (and often the policy is not yet ready)
    #
    # This is a workaround:
    # check how many total items are available to protect and are already protected
    # compare this number to the total number of VMs we want to back up
    # if the totals don't match, wait and check again
    #
    # Remember: Any VM with a tag of "backup: no" is excluded!
    print("Detecting which items are not backed up ... ", end='')
    while not vault_ready:
        protectable_items_to_backup = list(
            get_protectable_items_to_backup(subscription_id,
                                            resource_group_name,
                                            vault_name,
                                            vm_names_to_backup,
                                            request_session)
        )

        num_protectable = len(protectable_items_to_backup)

        if num_protectable == total_vms:
            vault_ready = True
            continue

        num_protected = len(list(
            get_protected_items_to_backup(subscription_id,
                                          resource_group_name,
                                          vault_name,
                                          vm_names_to_backup,
                                          request_session)
        ))

        if num_protectable + num_protected == total_vms:
            vault_ready = True
            continue

        print("waiting ... ", end='')
        time.sleep(1)

    print("Success!")
    print("Total VMs:", total_vms)
    print("Number already protected:", num_protected)
    print("Number to protect:", num_protectable)

    print("Using the default backup and retention policies")
    policy = backup_policies.get_default_policy(subscription_id, resource_group_name, vault_name, request_session)

    for protectable_item in protectable_items_to_backup:
        print("Backing up", protectable_item['properties']['friendlyName'], '... ', end='')
        backup_protected_items.create_protected_item(protectable_item,
                                                     policy,
                                                     request_session)
        # In the future we may need to check the job operation IDs to determine backup success
        # There is an API endpoint for this
        print("Success!")
    print("Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add a new Recovery Services Vault to a given resource group and "
                                                 "apply it to all virtual machines in the resource group")
    parser.add_argument("--client-id", dest="client_id", type=str, required=True,
                        help="Client ID (username) which should be used to effect the deployment.")
    parser.add_argument("--client-secret", dest="client_secret", type=str, required=True,
                        help="Client Secret (password) which should be used to effect the deployment.")
    parser.add_argument("--tenant-id", dest="tenant_id", type=str, required=True,
                        help="Tenant ID for the account under which the deployment should be effected.")
    parser.add_argument("--subscription-id", dest="subscription_id", type=str, required=True,
                        help="Subscription ID of the subscription to which this should be deployed.")
    parser.add_argument("--resource-group-name", dest="resource_group_name", type=str, required=True,
                        help="Name of the Resource Group that should be backup up, also where the recovery services "
                             "vault will be deployed is not otherwise specified.")
    parser.add_argument("--vault-name", dest="vault_name", type=str, required=True,
                        help="Name to be given to the created Recovery Services Vault")
    # Backup policy will default to DefaultPolicy for now,
    # until we can figure out how to create a new one via the API
    # parser.add_argument("--backup-policy-name", dest="backup_policy_name", type=str, required=True,
    #                    help="Name to be given to the created backup policy policy.")

    args = parser.parse_args()

    main(args.client_id,
         args.client_secret,
         args.tenant_id,
         args.subscription_id,
         args.resource_group_name,
         args.vault_name)
