from govdata import DKANPortalClient 
import requests
# get opendata-city-client
cityclient = DKANPortalClient(city="braunschweig", apiversion=3)

# get all available packages (topics)
packagelist = cityclient.get_packages()

# request data for package from packagelist
first_package_id_from_list = packagelist[0]
package_meta = cityclient.get_package_metadata(package_id=first_package_id_from_list)
resources_for_package = package_meta["resources"]

# fetch informations from choosen resource by id
index_of_choosen_resource = 1
resource_id = resources_for_package[index_of_choosen_resource]["id"]
resource = cityclient.get_resource_by_id(resource_id=resource_id)

# now send get-request to resource-url to download file as <resourcename>.csv
response = requests.get(resource["url"])
if response.ok:
    with open(f"{resource['name']}.csv", mode="wb") as file:
        file.write(response.content)
