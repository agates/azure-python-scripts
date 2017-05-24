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


def get_containers(subscription_id,
                   resource_group_name,
                   vault_name,
                   request_session):
    params = {'$filter': "backupManagementType eq 'AzureIaasVM'"}

    url = "{api_url}" \
          "/subscriptions/{subscription_id}" \
          "/resourceGroups/{resource_group_name}" \
          "/providers/Microsoft.RecoveryServices" \
          "/vaults/{vault_name}" \
          "/backupProtectionContainers" \
        .format(api_url=API_URL, subscription_id=subscription_id,
                resource_group_name=resource_group_name, vault_name=vault_name)

    response = request_session.get(url, params=params)

    return response.json()['value']
