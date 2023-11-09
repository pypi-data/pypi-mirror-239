import json
import base64


def get_base_64_encoded_auth(client_id, secret):
    if not client_id or not secret:
        raise Exception("Cannot generate base64 encoded auth because at least one of them is None!")
    message = client_id + ":" + secret
    message_bytes = message.encode("ascii")
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = "Basic " + base64_bytes.decode("ascii")
    return base64_message


def get_auth_headers(client_id, secret):
    base64_authorization = get_base_64_encoded_auth(client_id, secret)
    headers = {}
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = base64_authorization
    return headers


def parse_response(response):
    try:
        response_content = response.json()
    except:
        response_content = response.content
    if response.status_code < 300:
        return response_content
    else:
        raise Exception("API returned the following error: {}".format(response_content))


def get_akeneo_payload_from_list(payload):
    payload_string = ""
    if type(payload).__name__ == "list":
        for item in payload:
            if not item:
                continue
            if '_links' in item:
                item.pop('_links', None)
            payload_string += json.dumps(item) + "\n"
    elif type(payload).__name__ == "dict":
        if "_links" in payload:
            payload.pop('_links', None)
        payload_string += json.dumps(payload) + "\n"
    else:
        raise Exception("Can not transform request payload. Payload is not a dict and not a list")
    return payload_string


def get_json_from_repsonse_body(
    content,
    payload
):
    if not content:
        return None
    try:
        response_body = content.decode(encoding='UTF-8',errors='strict')
    except Exception as e:
        response_body = str(content)

    if is_content_json_line_format(response_body):
        splitted_response_body = get_splitted_response_body(response_body)
        parsed_repsonse_body = get_parsed_json_from_list(splitted_response_body, payload)
        return parsed_repsonse_body
    else:
        return parse_response_body_as_json(response_body, payload)


def is_content_json_line_format(response_body):
    if not response_body:
        return False
    if "\\n" in response_body or "\n" in response_body:
        return True
    else:
        return False


def get_splitted_response_body(response_body):
    if "\\n" in response_body:
        return response_body.split("\\n")
    elif "\n" in response_body:
        return response_body.split("\n")
    else:
        return None


def parse_response_body_as_json(
    response_body,
    payload
):
    try:
        parsed_repsonse_body = json.loads(response_body)
        if str(type(parsed_repsonse_body).__name__) != "list":
            return [ parsed_repsonse_body ]
        else:
            return parsed_repsonse_body
    except Exception as e:
        print(f"{response_body} -> Content is not a valid JSON")
        print(f"Faulty payload is {payload}")
        return None


def get_parsed_json_from_list(
    splitted_response_body,
    payload
):
    parsed_repsonse_body = []
    try:
        for line in splitted_response_body:
            if line:
                parsed_repsonse_body.append(json.loads(line))
        return parsed_repsonse_body
    except Exception as e:
        print(f"{splitted_response_body} -> Content is not a valid JSON")
        print(f"Faulty payload is {payload}")
        return None


def get_worst_item_response_from_parsed_response(input_content):
    if not input_content:
        raise Exception(input_content)
    elif type(input_content).__name__ != "list":
        raise Exception(input_content)
    final_status_code = 0
    item_response = None
    for upload_result in input_content:
        if upload_result["status_code"] > final_status_code:
            final_status_code = upload_result["status_code"]
            item_response = upload_result
    return item_response


def create_response_data(api_response_data, api_response_data_model, onboarding_to_new_map):
    response_product_data = []
    for api_response in api_response_data:
        if api_response['identifier'] not in onboarding_to_new_map:
            print("Strange error, the list of simple products does not have identifier" + api_response['identifier'])
            continue
        status_value = 'products_created'
        response_text = api_response['identifier']
        if api_response['status_code'] > 299:
            additional_message = get_additional_message(onboarding_to_new_map[api_response['identifier']],
                                                        api_response_data_model)
            status_value = 'product_creation_failed'
            response_text = json.dumps(api_response['errors']) + additional_message if 'errors' in api_response \
                else api_response['message']
            print("additional_message", additional_message, response_text)
        identifier = onboarding_to_new_map[api_response['identifier']]['identifier']
        response_product_data.append({
            'identifier': identifier,
            'values': {
                'onboarding_steps': [{
                    'locale': None,
                    'scope': None,
                    'data': status_value
                }],
                'feedback_onboarding_process': [{
                    'locale': None,
                    'scope': None,
                    'data': response_text,
                }]
            }
        })

    print("Response product Datum")
    for response_product_datum in response_product_data:
        print(response_product_datum)
    return response_product_data


def get_additional_message(product_data: dict, api_response_data_model: dict) -> str:
    if "prent" in product_data:
        first_parent = product_data["parent"]
        if first_parent and first_parent in api_response_data_model:
            return api_response_data_model[first_parent]
    return ""


def create_response_data_for_errors(cannot_create_errors):
    response_product_data = []
    for err in cannot_create_errors:
        if 'identifier' not in err:
            print("error information doesn't have any product identifier, cannot set error response for the product")
            continue
        response_product_data.append({
            'identifier': err['identifier'],
            'values': {
                'onboarding_steps': [{
                    'locale': None,
                    'scope': None,
                    'data': 'product_creation_failed'
                }],
                'feedback_onboarding_process': [{
                    'locale': None,
                    'scope': None,
                    'data': err['error'],
                }]
            }
        })
    print("Response product Datum for Create Errors")
    for response_product_datum in response_product_data:
        print(response_product_datum)
    return response_product_data
