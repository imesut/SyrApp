# -*- coding: utf-8 -*-

from google.cloud.credentials import get_credentials
creds = get_credentials()
print creds.get_access_token().access_token
