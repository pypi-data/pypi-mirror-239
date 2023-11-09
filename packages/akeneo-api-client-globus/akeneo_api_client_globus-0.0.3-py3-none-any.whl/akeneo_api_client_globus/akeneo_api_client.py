from . import akeneo_api_client_utils
import requests
import json


class AkeneoApiClient:


    def __init__(self, **kwargs):
        self.password = kwargs.get("password")
        self.username = kwargs.get("username")
        self.secret = kwargs.get("secret")
        self.client_id = kwargs.get("client_id")
        self.base_url = kwargs.get("base_url")
        self.access_token = None
        self.refresh_token = None


    def login_with_password(self):
        login_payload = {}
        login_payload["username"] = self.username
        login_payload["password"] = self.password
        login_payload["grant_type"] = "password"
        self.session = requests.Session()
        headers = akeneo_api_client_utils.get_auth_headers(self.client_id, self.secret)
        auth_url = self.base_url + "/api/oauth/v1/token"
        response = self.session.request("POST", auth_url, headers=headers, json=login_payload)
        response_json = akeneo_api_client_utils.parse_response(response)
        self.access_token = response_json["access_token"]
        self.refresh_token = response_json["refresh_token"]

        return None


    def get_auth_token_by_refresh_token(self):
        login_payload = {}
        login_payload["refresh_token"] = self.refresh_token
        login_payload["grant_type"] = "refresh_token"
        headers = akeneo_api_client_utils.get_auth_headers(self.client_id, self.secret)
        auth_url = self.base_url + "/api/oauth/v1/token"
        response = self.session.request("POST", auth_url, headers=headers, json=login_payload)
        response_json = akeneo_api_client_utils.parse_response(response)
        access_token = response_json["access_token"]
        refresh_token = response_json["refresh_token"]
        self.access_token = access_token
        self.refresh_token = refresh_token

        return access_token, refresh_token


    def send_request(self, http_method, url, headers = {}, params = {}, payload = {}):
        response = self.session.request(http_method, url, params=params, headers=headers, json=payload)
        if response.status_code != 401:
            return response
        else:
            self.get_auth_token_by_refresh_token()
            headers = {}
            headers["Authorization"] =  "Bearer " + self.access_token
            response = self.session.request(http_method, url, params=params, headers=headers, json=payload)
            return response


    def send_request_with_raw_payload(self, http_method, url, headers = {}, params = {}, payload = {}):
        response = self.session.request(http_method, url, params=params, headers=headers, data=payload)
        if response.status_code != 401:
            return response
        else:
            self.get_auth_token_by_refresh_token()
            headers = {}
            headers["Authorization"] =  "Bearer " + self.access_token
            response = self.session.request(http_method, url, params=params, headers=headers, data=payload)
            return response


    def post_file_with_request(self, url, headers = {}, params = {}, files = {}):
        response = self.session.request("POST", url, params=params, data={},  headers=headers, files=files)
        if response.status_code != 401:
            return response
        else:
            self.get_auth_token_by_refresh_token()
            headers = {}
            headers["Authorization"] =  "Bearer " + self.access_token
            response = self.session.request("POST", url, params=params, data={},  headers=headers, files=files)
            return response


    def send_search_request(self, url, headers = {}, search_filter=None):
        if search_filter:
            params = {
                "search": json.dumps(search_filter),
                "pagination_type": "search_after",
                "limit": 100
            }
            response = self.send_request("GET", url, headers, params, {})
        else:
            params = {
                "pagination_type": "search_after",
                "limit": 100
            }
            response = self.send_request("GET", url, headers, params, {})

        return response


    def get_products(self, search_filter=None):
        headers = {}
        headers["Authorization"] =  "Bearer " + self.access_token
        url = self.base_url + "/api/rest/v1/products"
        response = self.send_search_request(url=url, headers=headers, search_filter=search_filter)
        items = akeneo_api_client_utils.parse_response(response=response)

        return items


    def get_product_models(self, search_filter=None):
        headers = {}
        headers["Authorization"] =  "Bearer " + self.access_token
        url = self.base_url + "/api/rest/v1/product-models"
        response = self.send_search_request(url=url, headers=headers, search_filter=search_filter)
        items = akeneo_api_client_utils.parse_response(response=response)

        return items


    def get_assets(self, asset_family_code, search_filter=None):
        headers = {}
        headers["Authorization"] =  "Bearer " + self.access_token
        url = self.base_url + "/api/rest/v1/asset-families/" + asset_family_code + "/assets"
        response = self.send_search_request(url=url, headers=headers, search_filter=search_filter)
        items = akeneo_api_client_utils.parse_response(response=response)
        return items


    def get_asset(self, asset_family_code, code):
        headers = {}
        headers["Authorization"] =  "Bearer " + self.access_token
        url = f"{self.base_url}/api/rest/v1/asset-families/{asset_family_code}/assets/{code}"
        response = self.send_search_request(url=url, headers=headers, search_filter=None)
        items = akeneo_api_client_utils.parse_response(response=response)
        return items


    def set_asset_media(self, file_path):
        headers = {}
        headers["Authorization"] = "Bearer " + self.access_token
        url = self.base_url + "/api/rest/v1/asset-media-files"
        file = open(file_path, 'rb')
        response = requests.post(url, headers=headers, files=[('file', file)])
        if response.status_code != 401:
            return response
        else:
            self.login_with_password()
            response = self.session.request('post', url, headers=headers, files=[('file', file)])
            return response


    def get_asset_media(self, file_name):
        headers = {}
        headers["Authorization"] =  "Bearer " + self.access_token
        url = self.base_url + "/api/rest/v1/asset-media-files/" + file_name
        response = self.send_request("GET", url, headers, {}, {})
        return response


    def get_reference_entity_records(self, reference_entity, search_filter=None):
        headers = {}
        headers["Authorization"] =  "Bearer " + self.access_token
        url = self.base_url + "/api/rest/v1/reference-entities/" + reference_entity + "/records"
        response = self.send_search_request(url=url, headers=headers, search_filter=search_filter)
        items = akeneo_api_client_utils.parse_response(response=response)

        return items


    def get_reference_entity_attribute_definition(self, reference_entity):
        headers = {}
        headers["Authorization"] =  "Bearer " + self.access_token
        url = self.base_url + "/api/rest/v1/reference-entities/" + reference_entity + "/attributes"
        response = self.send_search_request(url=url, headers=headers, search_filter=None)
        items = akeneo_api_client_utils.parse_response(response=response)

        return items


    def get_reference_entities(self, search_filter=None):
        headers = {}
        headers["Authorization"] =  "Bearer " + self.access_token
        url = self.base_url + "/api/rest/v1/reference-entities"
        response = self.send_search_request(url=url, headers=headers, search_filter=search_filter)
        items = akeneo_api_client_utils.parse_response(response=response)

        return items


    def get_reference_entity_attributes(self, reference_entity, search_filter=None):
        headers = {}
        headers["Authorization"] =  "Bearer " + self.access_token
        url = self.base_url + "/api/rest/v1/reference-entities/" + reference_entity + "/attributes"
        response = self.send_search_request(url=url, headers=headers, search_filter=search_filter)
        items = akeneo_api_client_utils.parse_response(response=response)

        return items


    def get_attributes(self):
        headers = {}
        headers["Authorization"] =  "Bearer " + self.access_token
        url = self.base_url + "/api/rest/v1/attributes"
        response = self.send_request("GET", url, headers, { "limit": 100 }, {})
        attributes = akeneo_api_client_utils.parse_response(response=response)

        return attributes


    def get_attribute_groups(self):
        headers = {}
        headers["Authorization"] =  "Bearer " + self.access_token
        url = self.base_url + "/api/rest/v1/attribute-groups"
        response = self.send_request("GET", url, headers, { "limit": 100 }, {})
        attribute_groups = akeneo_api_client_utils.parse_response(response=response)

        return attribute_groups


    def get_categories(self):
        headers = {}
        headers["Authorization"] =  "Bearer " + self.access_token
        url = self.base_url + "/api/rest/v1/categories"
        response = self.send_request("GET", url, headers, { "limit": 100 }, {})
        categories = akeneo_api_client_utils.parse_response(response=response)

        return categories


    def get_families(self):
        headers = {}
        headers["Authorization"] =  "Bearer " + self.access_token
        url = self.base_url + "/api/rest/v1/families"
        response = self.send_request("GET", url, headers, { "limit": 100 }, {})
        families = akeneo_api_client_utils.parse_response(response=response)

        return families


    def get_family_variants(self, family_code, search_filter=None):
        headers = {}
        headers["Authorization"] =  "Bearer " + self.access_token
        url = self.base_url + "/api/rest/v1/families/" + family_code + "/variants"
        response = self.send_request("GET", url, headers, { "limit": 100 }, {})
        items = akeneo_api_client_utils.parse_response(response=response)

        return items


    def get_product(self, identifier):
        headers = {}
        headers["Authorization"] =  "Bearer " + self.access_token
        url = self.base_url + "/api/rest/v1/products/" + identifier
        response = self.send_request("GET", url, headers, {}, {})
        item = akeneo_api_client_utils.parse_response(response=response)

        return item


    def get_product_model(self, identifier):
        headers = {}
        headers["Authorization"] =  "Bearer " + self.access_token
        url = self.base_url + "/api/rest/v1/product-models/" + identifier
        response = self.send_request("GET", url, headers, {}, {})
        item = akeneo_api_client_utils.parse_response(response=response)

        return item


    def get_reference_entity_record(self, reference_entity, identifier):
        headers = {}
        headers["Authorization"] =  "Bearer " + self.access_token
        url = self.base_url + "/api/rest/v1/reference-entities/" + reference_entity + "/records/" + identifier
        response = self.send_request("GET", url, headers, {}, {})
        item = akeneo_api_client_utils.parse_response(response=response)

        return item


    def get_reference_entity_image(self, file_name):
        headers = {}
        headers["Authorization"] =  "Bearer " + self.access_token
        url = self.base_url + "/api/rest/v1/reference-entities-media-files/" + file_name
        response = self.send_request("GET", url, headers, {}, {})
        return response


    def set_reference_entity(self, identifier, payload):
        url = self.base_url + "/api/rest/v1/reference-entities/" + identifier
        headers = {}
        final_payload = akeneo_api_client_utils.get_akeneo_payload_from_list(payload)
        headers["Authorization"] =  "Bearer " + self.access_token
        headers["Content-Type"] = "application/json"
        response = self.send_request_with_raw_payload("PATCH", url, headers, {}, final_payload)
        if response.status_code < 300:
            return response
        else:
            response_message = response.json()
            raise Exception("API returned the following error: {}".format(response_message))


    def set_reference_entity_records(self, reference_entity_identifier, payload):
        url = self.base_url + "/api/rest/v1/reference-entities/" + reference_entity_identifier + "/records"
        headers = {}
        final_payload = json.dumps(payload)
        headers["Authorization"] =  "Bearer " + self.access_token
        headers["Content-Type"] = "application/json"
        response = self.send_request_with_raw_payload("PATCH", url, headers, {}, final_payload)
        response_message = json.loads(response.content)
        item_response = akeneo_api_client_utils.get_worst_item_response_from_parsed_response(response_message)
        if item_response["status_code"] < 300:
           return None
        else:
            raise Exception("API returned the following error: {}".format(item_response))


    def set_reference_entity_attribute(self, reference_entity_identifier, attribute_name, payload):
        url = self.base_url + "/api/rest/v1/reference-entities/" + reference_entity_identifier + "/attributes/" + attribute_name
        headers = {}
        headers["Authorization"] =  "Bearer " + self.access_token
        headers["Content-Type"] = "application/json"
        response = self.send_request("PATCH", url, headers, {}, payload)
        if response.status_code < 300:
            return response
        else:
            response_message = response.json()
            raise Exception("API returned the following error: {}".format(response_message))


    def set_products(self, payload):
        url = self.base_url + "/api/rest/v1/products"
        headers = {}
        final_payload = akeneo_api_client_utils.get_akeneo_payload_from_list(payload)
        headers["Authorization"] =  "Bearer " + self.access_token
        headers["Content-Type"] = "application/vnd.akeneo.collection+json"
        response = self.send_request_with_raw_payload("PATCH", url, headers, {}, final_payload)
        if not response:
            return None
        parsed_response = akeneo_api_client_utils.get_json_from_repsonse_body(response.content, final_payload)
        item_response = akeneo_api_client_utils.get_worst_item_response_from_parsed_response(parsed_response)
        if item_response["status_code"] < 300:
            return None
        else:
            raise Exception("API returned the following error: {}".format(item_response))


    def set_products_and_get_response(self, payload):
        url = self.base_url + "/api/rest/v1/products"
        headers = {}
        final_payload = akeneo_api_client_utils.get_akeneo_payload_from_list(payload)
        headers["Authorization"] =  "Bearer " + self.access_token
        headers["Content-Type"] = "application/vnd.akeneo.collection+json"
        response = self.send_request_with_raw_payload("PATCH", url, headers, {}, final_payload)
        if not response:
            return None
        return akeneo_api_client_utils.get_json_from_repsonse_body(response.content, final_payload)


    def delete_product_models(self, identifier):
        url = self.base_url + f"/api/rest/v1/product-models/{identifier}"
        headers = {
            "Authorization": "Bearer " + self.access_token,
            "Content-Type": "application/json"
        }
        response = self.send_request("DELETE", url, headers)
        if response.status_code < 300:
            return response
        else:
            response_message = response.json()
            raise Exception("API returned the following error: {}".format(response_message))


    def set_assets(self, payload, family):
        url = f"{self.base_url}/api/rest/v1/asset-families/{family}/assets"
        headers = {}
        headers["Authorization"] =  "Bearer " + self.access_token
        headers["Content-Type"] = "application/json"
        final_payload = json.dumps(payload)
        response = self.send_request_with_raw_payload("PATCH", url, headers, {}, final_payload)
        return akeneo_api_client_utils.get_json_from_repsonse_body(response.content, final_payload)


    def set_product_models(self, payload):
        url = self.base_url + "/api/rest/v1/product-models"
        headers = {}
        final_payload = akeneo_api_client_utils.get_akeneo_payload_from_list(payload)
        headers["Authorization"] =  "Bearer " + self.access_token
        headers["Content-Type"] = "application/vnd.akeneo.collection+json"
        response = self.send_request_with_raw_payload("PATCH", url, headers, {}, final_payload)
        if not response:
            return None
        parsed_response = akeneo_api_client_utils.get_json_from_repsonse_body(response.content, final_payload)
        item_response = akeneo_api_client_utils.get_worst_item_response_from_parsed_response(parsed_response)
        if item_response["status_code"] < 300:
            return None
        else:
            raise Exception("API returned the following error: {}".format(item_response))


    def set_product_models_and_get_response(self, payload):
        url = self.base_url + "/api/rest/v1/product-models"
        headers = {}
        final_payload = akeneo_api_client_utils.get_akeneo_payload_from_list(payload)
        headers["Authorization"] =  "Bearer " + self.access_token
        headers["Content-Type"] = "application/vnd.akeneo.collection+json"
        response = self.send_request_with_raw_payload("PATCH", url, headers, {}, final_payload)
        if not response:
            return None
        return akeneo_api_client_utils.get_json_from_repsonse_body(response.content, final_payload)


    def get_following_cursor_items(self, url):
        headers = {}
        headers["Authorization"] = "Bearer " + self.access_token
        response = self.send_request(http_method="GET", url=url, headers=headers)
        items = akeneo_api_client_utils.parse_response(response=response)
        return items


    def set_reference_entity_image(self, file_path):
        url = self.base_url + "/api/rest/v1/reference-entities-media-files"
        headers = {}
        headers["Authorization"] = "Bearer " + self.access_token
        headers["Content-Type"] = "multipart/form-data"
        files = [
            ('file', open(file_path,'rb'))
        ]
        response = self.session.request("POST", url, headers=headers, data = {}, files = files)
        if response.status_code < 300:
            return response
        else:
            raise Exception("API returned the following error: {}".format(response.content))


    def get_locales(self):
        headers = {}
        headers["Authorization"] =  "Bearer " + self.access_token
        url = self.base_url + "/api/rest/v1/locales"
        response = self.send_request("GET", url, headers, { "limit": 100 }, {})
        locales = akeneo_api_client_utils.parse_response(response=response)
        return locales


    def get_measure_families(self):
        headers = {}
        headers["Authorization"] =  "Bearer " + self.access_token
        url = self.base_url + "/api/rest/v1/measure-families"
        response = self.send_request("GET", url, headers, { "limit": 100 }, {})
        measure_families = akeneo_api_client_utils.parse_response(response=response)
        return measure_families

