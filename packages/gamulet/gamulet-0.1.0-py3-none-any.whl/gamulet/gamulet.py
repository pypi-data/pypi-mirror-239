import json

import requests
from utils import interpolate, get_dict_value_from_json_path
from exceptions import FailedAssertion
from logger import get_logger


GLOBAL_VALUES_DICT = {}
LOGGER = get_logger()


class EndpointCall:
    def __init__(self, call, config):
        self.global_config = config
        self.endpoint = config['base_url'] + call['resource'] if call['resource'].startswith('/') else call['resource']
        self.body = call['body']
        self.method = call['method']
        self.saves = call['saves']
        self.assertions = call['assertions']

    def execute(self):
        call_method_to_req_method_mapping = {
            'GET': requests.get,
            'POST': requests.post,
            'PUT': requests.put,
            'DELETE': requests.delete,
        }
        response = call_method_to_req_method_mapping[self.method.upper()](
            self.endpoint,
            data=json.dumps(interpolate(self.body, self.global_config)),
        )
        json_response = response.json()
        for key, value in self.saves.items():
            GLOBAL_VALUES_DICT[value] = get_dict_value_from_json_path(json_response, key)
        for assertion_name, assertion in self.assertions.items():
            left_side, right_side = [item.strip() for item in assertion.split("==")]
            left_side_interpolated = interpolate(left_side.strip(), self.global_config)
            right_side_interpolated = interpolate(right_side, self.global_config)
            try:
                assert get_dict_value_from_json_path(json_response, left_side_interpolated) == right_side_interpolated
                LOGGER.info(f"{assertion_name} which asserts {assertion} passed")
            except AssertionError as e:
                raise FailedAssertion(f"{assertion_name} which asserts {assertion} failed")


class IntegrationTests:

    def __init__(self, runner_dict):
        self.response_store = []
        self.run_config = runner_dict['config']
        self.calls = runner_dict['calls']

    def run(self):
        for call_dict in self.calls:
            endpoint_call = EndpointCall(call_dict, self.run_config)
            endpoint_call.execute()


if __name__ == '__main__':
    with open('../../tests/test.json', 'r') as test_file:
        integration_test = IntegrationTests(json.load(test_file))
        integration_test.run()
