import requests
import re
url = 'http://houserent.58.com/landlord/center?infoId=33440334386358&PGTID=0d40000a-0374-e22b-2dba-b3f832a01ca0&ClickID=15'
import requests
rs = requests.get(url)
print(rs.text)