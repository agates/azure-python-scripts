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

import json

from constants import API_URL


def create_protected_item(protectable_item,
                          policy,
                          request_session):
    url = "{api_url}{route}".format(
        api_url=API_URL,
        route=protectable_item['id'].replace("protectableItems", "protectedItems")
    )

    data = {
        "properties": {
            "protectedItemType": protectable_item['properties']['protectableItemType'],
            "sourceResourceId": protectable_item['properties']['virtualMachineId'],
            "policyId": policy['id']
        }
    }

    response = request_session.put(url, data=json.dumps(data))

    return response


def get_protected_items(subscription_id,
                        resource_group_name,
                        vault_name,
                        request_session):
    params = {'$filter': "backupManagementType eq 'AzureIaasVM'"}

    url = "{api_url}" \
          "/subscriptions/{subscription_id}" \
          "/resourceGroups/{resource_group_name}" \
          "/providers/Microsoft.RecoveryServices" \
          "/vaults/{vault_name}" \
          "/backupProtectedItems" \
        .format(api_url=API_URL, subscription_id=subscription_id,
                resource_group_name=resource_group_name, vault_name=vault_name)

    response = request_session.get(url, params=params)

    return response.json()['value']


def get_protected_items_in_resource_group(subscription_id,
                                          resource_group_name,
                                          vault_name,
                                          request_session):
    protected_items = get_protected_items(subscription_id, resource_group_name, vault_name, request_session)
    resource_group_name = resource_group_name.lower()

    # Protected items do not store the resource group in a property
    # however, it is stored in the protected item name and id
    return (
        protected_item
        for protected_item in protected_items
        if resource_group_name in protected_item['name'].lower()
    )
