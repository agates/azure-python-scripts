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

import dateutil.parser
from tabulate import tabulate

import authorization
import session
from recovery_services import backup_protected_items, backup_protection_containers, recovery_points


def get_containers_with_protected_items(subscription_id,
                                        resource_group_name,
                                        vault_name,
                                        request_session):
    containers = backup_protection_containers.get_containers(subscription_id,
                                                             resource_group_name,
                                                             vault_name,
                                                             request_session)

    protected_items = backup_protected_items.get_protected_items(subscription_id,
                                                                 resource_group_name,
                                                                 vault_name,
                                                                 request_session)
    return ((container['name'],
             ('VM;' + protected_item['name']
              for protected_item in protected_items
              if protected_item['properties']['friendlyName'].lower() == container['properties']['friendlyName'].lower()
              )
             ) for container in containers)


def main(client_id,
         client_secret,
         tenant_id,
         subscription_id,
         resource_group_name,
         vault_name):
    access_token = authorization.retrieve_access_token(client_id, client_secret, tenant_id)
    request_session = session.create_request_session(access_token)

    containers_with_protected_items = get_containers_with_protected_items(subscription_id,
                                                                          resource_group_name,
                                                                          vault_name,
                                                                          request_session)

    vms_with_recovery_points = (
        (protected_item.split(';')[-1],
         recovery_points.get_recovery_points(subscription_id,
                                             resource_group_name,
                                             vault_name,
                                             container,
                                             protected_item,
                                             request_session)
         )
        for container, protected_items in containers_with_protected_items
        for protected_item in protected_items)

    print(tabulate(
        (
            (
                resource_name,
                recovery_point['name'],
                dateutil.parser.parse(recovery_point['properties']['recoveryPointTime']).strftime('%Y-%m-%d %H:%M'),
                recovery_point['properties']['recoveryPointType'],
                recovery_point['properties']['isManagedVirtualMachine'],
                recovery_point['properties']['isSourceVMEncrypted'],
                recovery_point['properties']['sourceVMStorageType'],
                recovery_point['properties']['virtualMachineSize']
            )
            for resource_name, rps in vms_with_recovery_points
            for recovery_point in rps
        ),
        headers=(
            'Resource Name',
            'Recovery Name',
            'Recovery Time',
            'Recovery Type',
            'Managed VM',
            'VM Encrypted',
            'VM Storage Type',
            'VM Size'
        )))


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
