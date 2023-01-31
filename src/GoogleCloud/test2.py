# https://developers.google.com/discovery/v1/building-a-client-library?hl=ko

import httplib2
import json
import uritemplate
import urllib

# Step 1: Fetch Discovery document
DISCOVERY_URI = "https://servicemanagement.googleapis.com/$discovery/rest?version=v1"
h = httplib2.Http()
resp, content = h.request(DISCOVERY_URI)
discovery = json.loads(content)

# Step 2.a: Construct base URI
BASE_URL = discovery['rootUrl'] + discovery['servicePath']

class Collection(object): pass

def createNewMethod(name, method):
  # Step 2.b Compose request
  def newMethod(**kwargs):
    body = kwargs.pop('body', None)
    url = urllib.parse.urljoin(BASE_URL, uritemplate.expand(method['path'], kwargs))
    for pname, pconfig in method.get('parameters', {}).items():
      if pconfig['location'] == 'path' and pname in kwargs:
        del kwargs[pname]
    if kwargs:
      url = url + '?' + urllib.parse.urlencode(kwargs)
    return h.request(url, method=method['httpMethod'], body=body,
                     headers={'content-type': 'application/json'})

  return newMethod

# Step 3.a: Build client surface
def build(discovery, collection):
  for name, resource in discovery.get('resources', {}).items():
    setattr(collection, name, build(resource, Collection()))
  for name, method in discovery.get('methods', {}).items():
    setattr(collection, name, createNewMethod(name, method))
  return collection

# Step 3.b: Use the client
service = build(discovery, Collection())
print (service.services.get(serviceName='discovery.googleapis.com', key='API_KEY'))