import json
from collections.abc import Iterable
from pagination.resource_cursor import ResourceCursor
from api.request.dict_serialize import DictSerialize
from api.request.line_serialize import LineSerialize


class ProductUuidApi:

    PRODUCTS_UUID_URI = "api/rest/v1/products-uuid"
    PRODUCT_UUID_URI = "api/rest/v1/products-uuid/%s"

    def __init__(self, resource_client, page_factory):
        self.resource_client = resource_client
        self.page_factory = page_factory

    def get(self, uuid: str, query_params: dict[str, any] = {}) -> dict[str, any]:
        response = self.resource_client.get_resource(self.PRODUCT_UUID_URI, [uuid], query_params)

        return json.loads(response.content)

    def all(self, page_size: int = 10, query_params: dict = {}) -> Iterable[list]:
        query_params["pagination_type"] = "search_after"
        response = self.resource_client.get_resources(self.PRODUCTS_UUID_URI, [], query_params, page_size)
        page = self.page_factory.create_page(response.json())

        return iter(ResourceCursor(page_size, page))

    def create(self, data={}) -> None:
        self.resource_client.create_resource(self.PRODUCTS_UUID_URI, [], DictSerialize(data))

    def upsert(self, uuid: str, data: dict) -> None:
        self.resource_client.upsert_resource(self.PRODUCT_UUID_URI, [uuid], DictSerialize(data))

    def delete(self, uuid: str) -> None:
        self.resource_client.delete_resource(self.PRODUCT_UUID_URI, [uuid])

    def upsert_batch(self, data: list[dict]) -> list[dict]:
        batch = LineSerialize()
        batch.add_items(data)

        response = self.resource_client.upsert_batch_resource(self.PRODUCTS_UUID_URI, [], batch)

        return [json.loads(item) for item in response.content.decode('utf-8').split("\n")]
