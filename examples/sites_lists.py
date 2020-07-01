import os
from msgraph import api, sites

authority_host_uri = 'https://login.microsoftonline.com'
tenant = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
resource_uri = 'https://graph.microsoft.com'
client_id = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
client_thumbprint = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
client_certificate_path = os.path.join('data', 'sites_lists.pem')
with open(client_certificate_path, 'rb') as input_file:
    client_certificate = input_file.read()
api_instance = api.GraphAPI.from_certificate(authority_host_uri, tenant, resource_uri, client_id, client_certificate, client_thumbprint)

site_id = 'a258178f-da15-42dd-a85b-90dbe49ebd9e'
site = sites.Site.get(api_instance, site=site_id)

list_ids = ('8f8b90e2-9880-4eda-bcb2-ae07462f89a2', '2f9c8b8b-f269-4ed4-bda4-4ba738871df0', '9359ba09-168a-4be3-9625-1263b17a5082', 'd22ec8d5-6716-48d4-aec1-e0eeaac0d009')
for list_id in list_ids:
    site_list = sites.SiteList.get(api_instance, site, list_instance=list_id)
    list_items = sites.ListItem.get(api_instance, site, site_list)
    for item in list_items:
        print(item.fields)
new_list_item = sites.ListItem.create(api_instance, site, list_ids[0], dict(Title='johndoe@wm.edu'))
new_list_item.delete(api_instance, site, list_ids[0])
