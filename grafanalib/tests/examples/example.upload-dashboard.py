from grafanalib.core import Dashboard
from grafanalib._gen import DashboardEncoder
import json
import requests
from os import getenv


def get_dashboard_json(dashboard):
    '''
    get_dashboard_json generates JSON from grafanalib Dashboard object

    :param dashboard - Dashboard() created via grafanalib
    '''

    # grafanalib generates json which need to pack to "dashboard" root element
    return json.dumps({"dashboard": dashboard.to_json_data()}, sort_keys=True, indent=2, cls=DashboardEncoder)


def upload_to_grafana(json, server, api_key):
    '''
    upload_to_grafana tries to upload dashboard to grafana and prints response

    :param json - dashboard json generated by grafanalib
    :param server - grafana server name
    :param api_key - grafana api key with read and write privileges
    '''

    headers = {'Authorization': f"Bearer {api_key}", 'Content-Type': 'application/json'}
    r = requests.post(f"https://{server}/api/dashboards/db", data=json, headers=headers)
    # TODO: add error handling
    print(f"{r.status_code} - {r.content}")


grafana_api_key = getenv("GRAFANA_API_KEY")
grafana_server = getenv("GRAFANA_SERVER")

my_dashboard = Dashboard(title="My awesome dashboard")
my_dashboard_json = get_dashboard_json(my_dashboard)
upload_to_grafana(my_dashboard_json, grafana_server, grafana_api_key)

##
##UPDATE EXISTING DASHBOARD##
##
my_dashboard = Dashboard(title="My awesome dashboard", id="XX", uid="xxxxx")
my_dashboard_json = get_dashboard_json(my_dashboard)
#convert json_dump back to json_object
temp2=json.loads(my_dashboard_json)
#append new properties
temp2['overwrite'] = True
temp2['message'] = "update from script"
#print (temp2)
#change from json_object to json_dump
my_dashboard_json = json.dumps(temp2, sort_keys=True, indent=2, cls=DashboardEncoder)
#print ('my_dashboard_json')
#print (my_dashboard_json)

##
##GET list of dashboards##
####Use this to get id and uid for updating exisitng dashboards####
##
import requests
import json
server = "http://xxxx:3000"
url = server + "/api/search?query=%"
headers = {
    "Authorization":f"Bearer {grafana_api_key}",
    "Content-Type":"application/json",
    "Accept": "application/json"
}
r = requests.get(url = url, headers = headers, verify=False)
for item in r.json():
    if item['type'] == 'dash-db':
        print(item)
