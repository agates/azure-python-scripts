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

from constants import API_URL


def get_recovery_points(subscription_id,
                        resource_group_name,
                        vault_name,
                        container_name,
                        protected_item_name,
                        request_session):
    url = "{api_url}" \
          "/subscriptions/{subscription_id}" \
          "/resourceGroups/{resource_group_name}" \
          "/providers/Microsoft.RecoveryServices" \
          "/vaults/{vault_name}" \
          "/backupFabrics/Azure" \
          "/protectionContainers/{container_name}" \
          "/protectedItems/{protected_item_name}" \
          "/recoveryPoints" \
        .format(api_url=API_URL, subscription_id=subscription_id,
                resource_group_name=resource_group_name, vault_name=vault_name,
                container_name=container_name, protected_item_name=protected_item_name)

    response = request_session.get(url)

    return response.json()['value']


def restore_recovery_point_disks(subscription_id,
                                 resource_group_name,
                                 vault_name,
                                 container_name,
                                 protected_item_name,
                                 recovery_point_name,
                                 request_session):
    s = "/subscriptions/fc74b460-0edc-41b5-81b3-baddc1fc4257" \
        "/resourceGroups/labRG1/providers/Microsoft.RecoveryServices" \
        "/vaults/idcdlslbRSVault" \
        "/backupFabrics/Azure" \
        "/protectionContainers/IaasVMContainer%3Biaasvmcontainerv2%3Barpittestresourcegroup%3Bvkencryrestore" \
        "/protectedItems/vm%3Biaasvmcontainerv2%3Barpittestresourcegroup%3Bvkencryrestore" \
        "/recoveryPoints/13738976139650/restore?api-version=2016-05-01"

    data = {
        "properties": {
            "objectType": "IaasVMRestoreRequest",
            "recoveryPointId": "13738976139650",
            "recoveryType": "RestoreDisks",
            "storageAccountId": "/subscriptions/fc74b460-0edc-41b5-81b3-baddc1fc4257/resourceGroups/arpit-test-vm2/providers/Microsoft.Storage/storageAccounts/arpittestvm25485",
            "createNewCloudService": False,
            "subnetId": "",
            "sourceResourceId": "/subscriptions/fc74b460-0edc-41b5-81b3-baddc1fc4257/resourceGroups/arpittestresourcegroup/providers/Microsoft.Compute/virtualMachines/vkencryrestore",
        }
    }

    url = "{api_url}" \
          "/subscriptions/{subscription_id}" \
          "/resourceGroups/{resource_group_name}" \
          "/providers/Microsoft.RecoveryServices" \
          "/vaults/{vault_name}" \
          "/backupFabrics/Azure" \
          "/protectionContainers/{container_name}" \
          "/protectedItems/{protected_item_name}" \
          "/recoveryPoints/{recovery_point_name}" \
          "/restore" \
        .format(api_url=API_URL, subscription_id=subscription_id,
                resource_group_name=resource_group_name, vault_name=vault_name,
                container_name=container_name, protected_item_name=protected_item_name,
                recovery_point_name=recovery_point_name)

    response = request_session.post(url)

    return response
