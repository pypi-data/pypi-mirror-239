import json
from collections.abc import Iterable
from pagination.resource_cursor import ResourceCursor
from api.request.dict_serialize import DictSerialize
from api.request.line_serialize import LineSerialize
from client.resource_client import ResourceClient
from pagination.page_factory import PageFactory


class ProductModelApi:

    PRODUCT_MODELS_URI = "api/rest/v1/product-models"
    PRODUCT_MODEL_URI = "api/rest/v1/product-models/%s"

    def __init__(self, resource_client: ResourceClient, page_factory: PageFactory):
        self.resource_client = resource_client
        self.page_factory = page_factory

    def get(self, code: str, query_params: dict[str, any] = {}) -> dict[str, any]:
        response = self.resource_client.get_resource(self.PRODUCT_MODEL_URI, [code], query_params)

        return json.loads(response.content)

    def all(self, page_size: int = 10, query_params: dict = {}) -> Iterable[list]:
        query_params["pagination_type"] = "search_after"
        response = self.resource_client.get_resources(self.PRODUCT_MODELS_URI, [], query_params, page_size)
        page = self.page_factory.create_page(response.json())

        return iter(ResourceCursor(page_size, page))

    def create(self, data={}) -> None:
        self.resource_client.create_resource(self.PRODUCT_MODELS_URI, [], DictSerialize(data))

    def upsert(self, code: str, data: dict) -> None:
        self.resource_client.upsert_resource(self.PRODUCT_MODEL_URI, [code], DictSerialize(data))

    def delete(self, code: str) -> None:
        self.resource_client.delete_resource(self.PRODUCT_MODEL_URI, [code])

    def upsert_batch(self, data: list[dict]) -> list[dict]:
        batch = LineSerialize()
        batch.add_items(data)

        response = self.resource_client.upsert_batch_resource(self.PRODUCT_MODELS_URI, [], batch)

        return [json.loads(item) for item in response.content.decode('utf-8').split("\n")]
