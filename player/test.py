# -*- coding: utf-8 -*-
import time

import requests
r = requests.session()
response = r.get('https://accounts.ea.com/connect/auth?client_id=FOS-SERVER&redirect_uri=nucleus:rest&response_type=code&access_token=QVQxOjEuMDozLjA6NjA6ajZETE5tcW1JVk1oaFNwNXMzenRMblNCVnM4VEp2WklwUjY6MzA2ODk6bzVoaDg')
print(response.text)