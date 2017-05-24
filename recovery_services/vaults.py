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


def create_vault(subscription_id,
                 resource_group_name,
                 resource_group_location,
                 vault_name,
                 request_session):
    url = "{api_url}" \
          "/subscriptions/{subscription_id}" \
          "/resourceGroups/{resource_group_name}" \
          "/providers/Microsoft.RecoveryServices" \
          "/vaults/{vault_name}" \
        .format(api_url=API_URL, subscription_id=subscription_id,
                resource_group_name=resource_group_name, vault_name=vault_name)

    data = {
        "location": resource_group_location,
        "properties": {},
        "sku": {
            "name": "Standard"
        },
        "tags": {}
    }

    response = request_session.put(url, data=json.dumps(data))

    return response.json()


def get_vault(subscription_id,
              resource_group_name,
              vault_name,
              request_session):
    url = "{api_url}" \
          "/subscriptions/{subscription_id}" \
          "/resourceGroups/{resource_group_name}" \
          "/providers/Microsoft.RecoveryServices" \
          "/vaults/{vault_name}" \
        .format(api_url=API_URL, subscription_id=subscription_id,
                resource_group_name=resource_group_name, vault_name=vault_name)

    response = request_session.get(url)

    return response.json()
