import unittest
import os
import json 
from src.AutoOpenApi.autoopenapi import ToDoc

class ComplicatedObject:
    name: str
    age: int
    details: dict
    more_details: list

    def __init__(self) -> None:
        self.name = "Jarrod"
        self.age = 31
        self.details = {
            'more': 'stuff',
            'key': 3
        }
        self.more_details = [
            {
                'arraykey': 1,
                'another': 'string'
            }
        ]


def mock_200_string_response(*args, **kwargs):
    return {
        "statusCode": 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': '"Some response"'
    }

def mock_200_complex_response(*args, **kwargs):
    response_obj = ComplicatedObject()
    return {
        "statusCode": 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(vars(response_obj))
    }

class TestDocBuilder(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.docs = ToDoc(os.environ["docs_input_location"], os.environ["docs_output_location"])
        cls.event_200 = {
            "httpMethod": "GET",
            "resource": '/root/endpoint/{pparam}',
            "queryParameters": {},
            "pathParameters": {
                "pparam": "pparma_value"
            },
            "body": json.dumps(None)
        }
        cls.event_200_complex = {
            "httpMethod": "GET",
            "resource": '/root/endpoint/complicated',
            "queryParameters": {},
            "pathParameters": {},
            "body": json.dumps(None)
        }

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_build_endpoint_200(self):
        response = mock_200_string_response(event=self.event_200)
        self.docs.build_endpoint(event=self.event_200, response=response)

    def test_build_endpoint_200_complex(self):
        response = mock_200_complex_response(event=self.event_200_complex)
        self.docs.build_endpoint(event=self.event_200_complex, response=response)        

