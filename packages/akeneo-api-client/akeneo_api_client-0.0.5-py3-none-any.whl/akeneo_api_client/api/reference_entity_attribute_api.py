import json
from collections.abc import Iterable
from pagination.resource_cursor import ResourceCursor
from api.request.dict_serialize import DictSerialize
from api.request.line_serialize import LineSerialize


class ReferenceEntityAttributeApi:

    REFERENCE_ENTITY_ATTRIBUTES_URI = "api/rest/v1/reference-entities/%s/attributes"
    REFERENCE_ENTITY_ATTRIBUTE_URI = "api/rest/v1/reference-entities/%s/attributes/%s"

    def __init__(self, resource_client, page_factory):
        self.resource_client = resource_client
        self.page_factory = page_factory

    def get(self, reference_entity_code: str, attribute_code: str) -> dict[str, any]:
        response = self.resource_client.get_resource(self.REFERENCE_ENTITY_ATTRIBUTE_URI, [reference_entity_code, attribute_code])

        return json.loads(response.content)

    def all(self, reference_entity_code: str, query_params: dict = {}) -> Iterable[list]:
        response = self.resource_client.get_resources(self.REFERENCE_ENTITY_ATTRIBUTES_URI, [reference_entity_code], query_params)
        page = self.page_factory.create_page(response.json())

        return iter(ResourceCursor(0, page))

    def upsert(self, reference_entity_code: str, attribute_code: str, data: dict = {}) -> None:
        self.resource_client.upsert_resource(
            self.REFERENCE_ENTITY_ATTRIBUTE_URI,
            [reference_entity_code, attribute_code],
            DictSerialize(data)
        )
