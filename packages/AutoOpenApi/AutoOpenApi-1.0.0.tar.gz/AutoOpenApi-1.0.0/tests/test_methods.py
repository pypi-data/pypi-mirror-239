import unittest
from src.AutoOpenApi.autoopenapi import Method, Parameter, Response

class TestMethods(unittest.TestCase):
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
        verb = "post"
        m = Method(verb)
        assert m is not None

    def test_init_wrong_verb(self):
        verb = "wrong verb"
        with self.assertRaises(Exception):
            Method(verb)

    def test_set_parameters(self):
        verb = "post"
        m = Method(verb)
        p = Parameter(name="param_name", IN="query", desc="Param Desc", required=True, parameter_value=10)
        m.set_parameters([p])
        self.assertEqual(len(m.parameters), 1)
    
    def test_method_exists_false(self):
        verb = "post"
        endpoint_name = '/some/endpoint'
        m = Method(verb)
        current_yaml = {
            'paths': {
                endpoint_name: {},
            }
        }
        result = m.exists(endpoint_name, current_yaml)
        self.assertEqual(result, False)

    def test_method_exists_true(self):
        verb = "post"
        endpoint_name = '/some/endpoint'
        m = Method(verb)
        current_yaml = {
            'paths': {
                endpoint_name: {
                    verb: {},
                },
            }
        }
        result = m.exists(endpoint_name, current_yaml)
        self.assertEqual(result, True)
    
    def test_set_responses(self):
        verb = "post"
        m = Method(verb)
        r = Response(code=200, desc="some description", schema_name="SCHEMA")
        m.set_responses([r])
        self.assertEqual(len(m.responses), 1)

    def test_to_open_api_3(self):
        verb = "post"
        m = Method(verb)
        expected = {
            verb: {}
        }
        result = m.to_open_api_3()
        self.assertDictEqual(result, expected)

    def test_to_open_api_3_with_params(self):
        verb = "post"
        m = Method(verb)
        p = Parameter(name="param_name", IN="query", desc="Param Desc", required=True, parameter_value=10)
        m.set_parameters([p])
        expected = {
            verb: {
                'parameters': [
                    {
                        'description': 'Param Desc',
                        'in': 'query',
                        'name': 'param_name',
                        'required': True,
                        'schema': {
                            'example': 10,
                            'format': 'int32',
                            'type': 'integer'
                        }
                    }
                ]
            }
        }
        result = m.to_open_api_3()
        self.assertDictEqual(result, expected)

    # def test_to_open_api_3_with_responses(self):
    #     verb = "post"
    #     m = Method(verb)
    #     p = Parameter(name="param_name", IN="query", desc="Param Desc", required=True, parameter_value=10)
    #     m.set_parameters([p])
    #     expected = {
    #         verb: {
    #             'parameters': [
    #                 {
    #                     'description': 'Param Desc',
    #                     'in': 'query',
    #                     'name': 'param_name',
    #                     'required': True,
    #                     'schema': {
    #                         'example': 10,
    #                         'format': 'int32',
    #                         'type': 'integer'
    #                     }
    #                 }
    #             ]
    #         }
    #     }
    #     result = m.to_open_api_3()
    #     self.assertDictEqual(result, expected)