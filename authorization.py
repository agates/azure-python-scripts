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

import requests

from constants import API_URL, TOKEN_URL


def retrieve_access_token(client_id, client_secret, tenant_id):
    # An error is returned if the resource URL is not exact, including the ending forward slash
    data = {'grant_type': "client_credentials",
            'client_id': client_id,
            'client_secret': client_secret,
            'resource': API_URL + '/'}
    url = TOKEN_URL.format(tenant_id=tenant_id)
    response = requests.post(url, data=data)

    return response.json()['access_token']
