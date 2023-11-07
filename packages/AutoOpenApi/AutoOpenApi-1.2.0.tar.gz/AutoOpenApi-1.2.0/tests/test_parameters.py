import unittest
from src.AutoOpenApi.autoopenapi import Parameter

class TestParameters(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_init(self):
        p = Parameter(name="param_name", IN="query", desc="Param Desc", required=True, parameter_value=10)
        assert p is not None

    def test_init_wrong_param_in(self):
        IN = "some incorrect type"
        with self.assertRaises(Exception):
            p = Parameter(name="param_name", IN=IN, desc="Param Desc", required=True, parameter_value=10)

    def test_init_wrong_param_value(self):
        name = "param_name"
        IN = "query"
        desc="Param Desc"
        required=True
        parameter_value=[1,2,3]

        with self.assertRaises(Exception):
            p = Parameter(name, IN, desc, required, parameter_value)

    def test_to_open_api_3_bool(self):
        name = "param_name"
        IN = "query"
        desc="Param Desc"
        required=True
        parameter_value=True

        p = Parameter(name, IN, desc, required, parameter_value)
        result = p.to_open_api_3()
        expected = {
            "name": name,
            "in": IN,
            "description": desc,
            "required": required,
            "schema": {
                "type": "boolean",
                "example": parameter_value,
            }
        }
        self.assertDictEqual(result, expected)

    def test_to_open_api_3_int(self):
        name = "param_name"
        IN = "query"
        desc="Param Desc"
        required=True
        parameter_value=10

        p = Parameter(name, IN, desc, required, parameter_value)
        result = p.to_open_api_3()
        expected = {
            "name": name,
            "in": IN,
            "description": desc,
            "required": required,
            "schema": {
                "type": "integer",
                "example": parameter_value,
                "format": "int32"
            }
        }
        self.assertDictEqual(result, expected)

    def test_to_open_api_3_float(self):
        name = "param_name"
        IN = "query"
        desc="Param Desc"
        required=True
        parameter_value=1.0

        p = Parameter(name, IN, desc, required, parameter_value)
        result = p.to_open_api_3()
        expected = {
            "name": name,
            "in": IN,
            "description": desc,
            "required": required,
            "schema": {
                "type": "number",
                "example": parameter_value,
            }
        }
        self.assertDictEqual(result, expected)

    def test_to_open_api_3_string(self):
        name = "param_name"
        IN = "query"
        desc="Param Desc"
        required=True
        parameter_value="string value"

        p = Parameter(name, IN, desc, required, parameter_value)
        result = p.to_open_api_3()
        expected = {
            "name": name,
            "in": IN,
            "description": desc,
            "required": required,
            "schema": {
                "type": "string",
                "example": parameter_value,
            }
        }
        self.assertDictEqual(result, expected)