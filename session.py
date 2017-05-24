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

from constants import API_DOMAIN, AZURE_API_VERSION


# Long running jobs will likely need to renew the access token after a while
def create_request_session(access_token):
    session = requests.Session()
    session.headers.update({
        'Authorization': "Bearer {token}".format(token=access_token),
        'Content-Type': "application/json",
        'Host': API_DOMAIN
    })
    session.params.update({'api-version': AZURE_API_VERSION})
    return session
