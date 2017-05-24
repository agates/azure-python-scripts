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

API_DOMAIN = "management.azure.com"
API_URL = "https://{api_domain}".format(api_domain=API_DOMAIN)
AZURE_API_VERSION = "2016-06-01"
TOKEN_URL = "https://login.microsoftonline.com/{tenant_id}/oauth2/token"
