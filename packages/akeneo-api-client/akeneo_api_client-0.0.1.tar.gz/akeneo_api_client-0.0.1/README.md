# Akeneo API Client

NOTE: This is still a work in progress

## installtion
```commandline
pip install akeneo_api_client
```

## Usage

Firstly import the relevant packages and build the client:
```python
from akeneo_api_client.client_builder import ClientBuilder
from akeneo_api_client.client.akeneo_api_error import AkeneoApiError

cb = ClientBuilder(uri)
api = cb.build_authenticated_by_password(username, password, client_id, secret)
```

Fetching a product:
```python
try:
    res = api.product_uuid_api.get(uuid)
    print(res)
except AkeneoApiError as e:
    print(e.response.status_code)
```