import os
import oyaml as yaml
from typing import Any, List, Union, Optional
from abc import ABC, abstractclassmethod
import json


class ConverterRequirements(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractclassmethod
    def exists(self):
        pass

    @abstractclassmethod
    def to_open_api_3(self):
        pass

class TypeClass(ABC):
    def __init__(self) -> None:
        super().__init__()
    
    def _primitive_types(self, var: Any) -> bool:
        if (type(var) == str) or (type(var) == int) or (type(var) == float) or (type(var) == bool) or (var is None):
            return True
        else:
            return False
    
    def _map_types(self, key: Any) -> str:
        if type(key) == str:
            return "string"
        elif key is None:
            return "string"
        elif type(key) == int:
            return "integer"
        elif type(key) == bool:
            return "boolean"
        elif type(key) == float:
            return "number"
        elif type(key) == list:
            return "array"
        elif type(key) == dict:
            return "object"
        else:
            raise Exception(f"Error mapping type for {key}")

class Parameter(TypeClass, ConverterRequirements):
    def __init__(self, name: str, IN: str, desc: str, required: bool, parameter_value: Any) -> None:
        super().__init__()
        self.name = name 
        self.IN = self.set_in(IN)
        self.required = required
        self.description = desc
        self.schema = self.set_schema(parameter_value)

    def exists(self):
        pass

    def to_open_api_3(self):
        return {
            "name": self.name,
            "in": self.IN,
            "description": self.description,
            "required": self.required,
            "schema": self.schema
        }

    def set_in(self, IN: str):
        allowed_ins = ["query", "path"]
        if IN.lower() in allowed_ins:
            return IN.lower()
        else:
            raise Exception(f"Error: Parameter IN must be either query or path")

    def set_schema(self, parameter_value: Any) -> dict:
        if self._primitive_types(parameter_value):
            self.schema = {
                "type": self._map_types(parameter_value),
                "example": parameter_value
            }
            if type(parameter_value) == int:
                self.schema["format"] = "int32"
            return self.schema
        else:
            raise Exception(f"Error: parameter of type {type(parameter_value)} not implemented")

class Response(ConverterRequirements):
    def __init__(self, code: int, desc: str, schema_name) -> None:
        super().__init__()
        self.code = code
        self.description = desc
        self.content = "application/json"
        self.schema = self.set_schema_name(schema_name)

    def exists(self, endpoint_name: str, method_verb: str, current_yaml: dict):
        for code in current_yaml['paths'][endpoint_name][method_verb]:
            if str(self.code) == code:
                return True
        return False        

    def to_open_api_3(self):
        return {
            str(self.code):{
                "description": self.description,
                "content": {
                    self.content: {
                        "schema": self.schema
                    }
                }
            }
        }

    def set_schema_name(self, schema_name):
        schema_name = schema_name.replace('/', '')
        schema_name = schema_name.replace('{', '')
        schema_name = schema_name.replace('}', '')
        self.schema_name = schema_name.lower()
        self.schema = {"$ref": f"#/components/schemas/{self.schema_name}"}
        return self.schema

class Method(ConverterRequirements):
    def __init__(self, verb: str) -> None:
        super().__init__()
        self._allowed_verbs = ["post", "get", "put", "delete", "patch"]
        self.verb = self.set_method(verb)
        self.parameters = None
        self.responses = None

    def exists(self, endpoint_name: str, current_yaml: dict):
        if self.verb in list(current_yaml['paths'].get(endpoint_name)):
            return True
        else:
            return False

    def set_method(self, verb: str) -> str:
        if verb.lower() in self._allowed_verbs:
            return verb.lower()
        else:
            raise Exception(f"Error: {verb} is not allowed")

    def set_parameters(self, parameters: List[Parameter]) -> None:
        self.parameters = parameters

    def update_responses(self, responses: List[Response]) -> None:
        pass

    def set_responses(self, responses: List[Response]) -> None:
        self.responses = responses

    def to_open_api_3(self) -> dict:
        return_dict = {
            self.verb: {}
        }
        if self.parameters:
            param_list = [param.to_open_api_3() for param in self.parameters]
            return_dict[self.verb]["parameters"] = param_list
        # if self.responses is None:
        #     raise Exception(f"Error: No responses have been defined for method {self.verb}, use {__class__.__name__}.set_parameters")
        if self.responses:
            for resp in self.responses:
                if return_dict[self.verb].get("responses") is None:
                    return_dict[self.verb]["responses"] = {str(resp.code): resp.to_open_api_3()}
                elif return_dict[self.verb].get("responses"):
                    return_dict[self.verb]["responses"].update({str(resp.code): resp.to_open_api_3()})
                else:
                    raise Exception(f"Error: there was an issue updating responses for method {self.verb}")
        return return_dict

class Endpoint(ConverterRequirements):
    def __init__(self, endpoint_name: str) -> None:
        super().__init__()
        self.name = endpoint_name
        self.methods = []

    def exists(self, current_yaml) -> bool:
        if current_yaml.get("paths"):
            for path in current_yaml['paths']:
                if self.name == path:
                    return True
        return False

    def add_method(self, method: Method) -> None:
        self.methods.append(method)

    def set_methods(self, methods: List[Method]) -> None:
        self.methods = methods

    def to_open_api_3(self):
        return_dict = {
            self.name: {}
        }
        for method in self.methods:
            if return_dict[self.name].get(method.verb) is None:
                return_dict[self.name] = method.to_open_api_3()
            elif return_dict[self.name].get(method.verb):
                return_dict[self.name][method.verb].update(method.to_open_api_3())
            else:
                raise Exception(f"Error: there was an issue updating methods for endpoint {self.name}")
        return return_dict

class Schema(TypeClass, ConverterRequirements): 
    def __init__(self, response: Response, example: Any) -> None:
        super().__init__()
        self.name = response.schema_name
        self.type = self._map_types(example) #if dict, if prim, if list
        self.properties = self.set_properties(example) #then dict, then prim, then list

    def exists(self, current_yaml: dict) -> bool:
        if current_yaml.get('components'):
            if current_yaml["components"]['schemas'].get(self.name):
                return True
        return False

    def get_primitive_schema(self, properties: Union[str, int, float]) -> dict:
        if self._primitive_types(properties):
            return_dict = {
                "type": self._map_types(properties),
                "example": properties
            }
            if type(properties) == int:
                return_dict["format"] = "int32"
            return return_dict
        else:
            raise Exception(f"Error: schema of type {type(properties)} not implemented")

    def get_array_schema(self, properties: list):
        return_dict = {
            "type": self._map_types(properties),
            "items": {}
        }
        items_dict = {}
        for item in properties:
            items_dict[self._map_types(item)] = item # need unique types with an example
        for key, value in items_dict.items(): # for each unique item, put them in the return dict
            if self._primitive_types(value):
                return_dict["items"] = self.get_primitive_schema(value)
            elif type(value) == dict:
                return_dict["items"][str(key)] = self.get_object_schema(value)
            elif type(value) == list:
                return_dict["items"][str(key)] = self.get_array_schema(value)
            elif type(value) is None:
                return_dict["properties"][str(key)] = self.get_primitive_schema("None")
            else:
                raise Exception(f"Error: Could not get schema for type {type(value)}")
        return return_dict

    def get_object_schema(self, properties: dict) -> dict:
        return_dict = {
            "type": self._map_types(properties),
            "properties": {}
        }
        for key, value in properties.items():
            if self._primitive_types(value):
                return_dict["properties"][str(key)] = self.get_primitive_schema(value)
            elif type(value) == dict:
                return_dict["properties"][str(key)] = self.get_object_schema(value)
            elif type(value) == list:
                return_dict["properties"][str(key)] = self.get_array_schema(value)
            elif type(value) is None:
                return_dict["properties"][str(key)] = self.get_primitive_schema("None")
            else:
                raise Exception(f"Error: Could not get schema for type {type(value)}")
        return return_dict

    def set_properties(self, example: Any) -> Union[str, int, float, dict, list]:
        if self._primitive_types(example):
            self.template_number = 0
            return example
        elif type(example) == dict:
            self.template_number = 1
            return example
        elif type(example) == list:
            self.template_number = 2
            return example
        else:
            raise Exception(f"Error: Cannot set properties for {example}")

    def to_open_api_3(self):
        return_dict = {
            self.name: {}
        }
        if self.template_number == 0: #primitive
            return_dict[self.name] = self.get_primitive_schema(self.properties)
            return return_dict
        elif self.template_number == 1:
            return_dict[self.name] = self.get_object_schema(self.properties)
            return return_dict
        elif self.template_number == 2:
            return_dict[self.name] = self.get_array_schema(self.properties)
            return return_dict
        else:
            raise Exception(f"Error: Something has gone wrong in the conversion...")

class Component(ConverterRequirements):
    def __init__(self) -> None:
        super().__init__()
        self.name = "components"
        self.schemas = []

    def exists(self, current_yaml) -> bool:
        if current_yaml.get(self.name):
            return True
        return False        

    def set_schemas(self, schemas: List[Schema]) -> None:
        self.schemas = schemas
        
    def to_open_api_3(self):
        return_dict = {
            self.name: {
                "schemas": {}
            }
        }
        for schema in self.schemas:
            if return_dict[self.name].get(schema.name) is None:
                return_dict[self.name]["schemas"] = schema.to_open_api_3()
            elif return_dict[self.name]["schemas"].get(schema.name):
                return_dict[self.name]["schemas"][schema.name].update(schema.to_open_api_3())
            else:
                raise Exception(f"Error: there was an issue updating schemas for endpoint {self.name}")
        return return_dict

class Path(ConverterRequirements): 
    def __init__(self, endpoint: Endpoint, methods: List[Method], parameters: Union[List[Parameter], None], responses: List[Response]) -> None:
        super().__init__()
        self.endpoint = endpoint
        self.methods = methods
        self.parameters = parameters
        self.responses = responses

    def exists(self):
        pass

    def to_open_api_3(self) -> dict:
        raise NotImplementedError(f"Error: {__class__.__name__}.to_open_api_3 not implemented yet")

class OpenApiDocBuilder:
    def __init__(self, file_location: Union[str, None], input_file_location: Union[str, None]) -> None:
        self.api_config_location = self.set_input_file(input_file_location)
        self.out_file_location = self.set_out_file_location(file_location)

    def set_input_file(self, input_file_location: Union[str, None]):
        if input_file_location is None:
            return os.path.join(os.getcwd(), 'api_config.yaml')
        else:
            return input_file_location

    def set_out_file_location(self, file_location: Union[str, None]) -> str:
        if file_location is None:
            return os.path.join(os.getcwd(), 'output.yaml')
        else:
            return file_location

    def _get_current_yaml(self, file_location):
        try:
            with open(file_location,'r') as yamlfile:
                current_yaml = yaml.safe_load(yamlfile) 
            return current_yaml
        except Exception as e:
            raise FileNotFoundError(f"Error {e}: Could not get file from {file_location}")

    def read_current_file(self) -> dict:
        try:
            current_yaml = self._get_current_yaml(file_location=self.out_file_location)
            return current_yaml
        except FileNotFoundError:
            current_yaml = self._get_current_yaml(file_location=self.api_config_location)
            return current_yaml
        except Exception as e:
            raise Exception(f"Error {e}: There was an issue getting the current yaml, please check inputs")

    def write_to_file(self, current_yaml: dict) -> str:
        try:
            if current_yaml:
                file_location = self.out_file_location
                with open(file_location,'w') as yamlfile:
                    yaml.safe_dump(current_yaml, yamlfile)
            return file_location
        except Exception as e:
            raise Exception(f"Error {e}: \n Issue writing file to {file_location}")

    def add_path_to_yaml(current_yaml: dict, path: Path) -> dict:
        if current_yaml.get('path') is None:
            current_yaml['path'] = path.to_open_api_3()
        elif current_yaml.get('path'):
            current_yaml['path'].update(path.to_open_api_3())
        else:
            raise Exception(f"Error: Failed to add {path.endpoint.name} to yaml")


    def update_paths(self, current_yaml: dict, Endpoint: Endpoint):
        endpoint_yaml = Endpoint.to_open_api_3()
        if current_yaml.get('paths') is None:
            current_yaml['paths'] = endpoint_yaml
        else:
            for k,v in endpoint_yaml.items():
                current_yaml['paths'][k] = v 

class ToDoc:
    input_file: str
    output_file: str
    OADB: OpenApiDocBuilder
    current_yaml: dict

    def __init__(self, input_file: str, output_file: str) -> None:
        self.input_file = input_file
        self.output_file = output_file
        self.OADB = OpenApiDocBuilder(file_location=self.output_file, input_file_location=self.input_file)
        self.current_yaml = self.get_current_yaml(self.OADB)

    def set_current_yaml(self):
        self.OADB.write_to_file(self.current_yaml)
        return

    def get_current_yaml(self, oadb: OpenApiDocBuilder):
        return oadb.read_current_file()

    def _get_params(self, param_type: str, params: dict) -> list:
        param_list = list()
        for i, (param, param_value) in enumerate(params.items()):
            param_list.append(Parameter(name=str(param), IN=param_type, desc=f"{param_type} parameter {str(i)}", required=True, parameter_value=param_value))
        return param_list

    def _get_code(self, response: dict):
        if response.get('statusCode'):
            code = response['statusCode']
        else:
            raise Exception(f"Error response object should include key: 'statusCode' in order to be processed")

        if code == 200: msg = "Successful Operation"
        elif code == 400: msg = "Client Error"
        elif code == 404: msg = "Not Found Error"
        elif code == 500: msg = "Server Error"
        else: msg = "Some unspecified Error"
        return code, msg

    def add_response_to_method(self, response: Response, method: Method):
        pass

    def _add_response_to_endpoint_method(self, event: dict, response: dict):
        OADB = OpenApiDocBuilder(file_location=self.output_file, input_file_location=self.input_file)
        current_yaml = OADB.read_current_file()
        if current_yaml.get('paths'):
            paths = current_yaml['paths']
        else:
            raise Exception("paths are not yet defined")
        if paths.get(event["resource"]):
            E1 = Endpoint(endpoint_name=event["resource"])
        else:
            raise Exception("Endpoint is not yet defined")
        if paths[E1.name].get(event["httpMethod"].lower()):
            M1 = Method(verb=event["httpMethod"])
        else:
            raise Exception("Method is not yet defined")

        if paths[E1.name][M1.verb].get('responses'):
            schema_name = E1.name + M1.verb
            code, msg = self._get_code(response)
            r1 = Response(code=code, desc=msg, schema_name=schema_name)
            paths[E1.name][M1.verb]['responses'][str(r1.code)] =  r1.to_open_api_3()
            OADB.write_to_file(current_yaml)

    def add_params_to_endpoint_method(self, endpoint: Endpoint, method: Method, params: List[Parameter]):
        formatted_param_list = [p.to_open_api_3() for p in params]
        self.current_yaml["paths"][endpoint.name][method.verb]['parameters'] = formatted_param_list
        return

    def add_response_to_endpoint_method(self, endpoint: Endpoint, method: Method, response: Response):
        if self.current_yaml["paths"][endpoint.name][method.verb].get('responses'):
            self.current_yaml["paths"][endpoint.name][method.verb]['responses'].update(response.to_open_api_3())
        else:
            self.current_yaml["paths"][endpoint.name][method.verb]['responses'] = response.to_open_api_3()
        return

    def add_method_to_endpoint(self, endpoint: Endpoint, method: Method) -> None:
        if self.current_yaml["paths"][endpoint.name].get(method.verb):
            self.current_yaml["paths"][endpoint.name] = method.to_open_api_3()
        else:
            self.current_yaml["paths"][endpoint.name].update(method.to_open_api_3())
        return 

    def add_component(self, component: Component) -> None:
        if self.current_yaml.get("components"):
            self.current_yaml.update(component.to_open_api_3())
        else:
            self.current_yaml = component.to_open_api_3()
        return 

    def add_endpoint(self, endpoint: Endpoint) -> None:
        if self.current_yaml.get("paths"):
            self.current_yaml["paths"].update(endpoint.to_open_api_3())
        else:
            self.current_yaml["paths"] = endpoint.to_open_api_3()
        return 

    def add_schema_to_component(self, schema: Schema) -> None:
        if self.current_yaml.get("components") is None:
            self.current_yaml["components"] = {'schemas': {}}

        if self.current_yaml["components"].get('schemas'):
            self.current_yaml["components"]["schemas"].update(schema.to_open_api_3())
        else:
            self.current_yaml["components"]["schemas"] = schema.to_open_api_3()
        return         

    def build_endpoint(self, event: dict, response: dict):
        E1 = Endpoint(endpoint_name=event["resource"])
        M1 = Method(verb=event["httpMethod"])
            
        code, msg = self._get_code(response)
        if code == 200:
            schema_name = E1.name + M1.verb
        elif code == 400:
            schema_name = 'clientErrorResponse'
        elif code == 404:
            schema_name = 'notFoundErrorResponse'
        else: 
            schema_name = 'serverErrorResponse'
        R1 = Response(code=code, desc=msg, schema_name=schema_name)
        S1 = Schema(response=R1, example=json.loads(response['body']))

        if not E1.exists(self.current_yaml): self.add_endpoint(E1)

        if not M1.exists(E1.name, self.current_yaml): self.add_method_to_endpoint(E1, M1)

        if code == 200:
            q_param_list = self._get_params(param_type="query", params=event["queryStringParameters"]) if event.get("queryStringParameters") else None
            p_param_list = self._get_params(param_type="path", params=event["pathParameters"]) if event.get("pathParameters") else None
            if q_param_list: self.add_params_to_endpoint_method(E1, M1, q_param_list)
            if p_param_list: self.add_params_to_endpoint_method(E1, M1, p_param_list)

        if not R1.exists(E1.name, M1.verb, self.current_yaml): self.add_response_to_endpoint_method(E1, M1, R1)

        if not S1.exists(self.current_yaml): self.add_schema_to_component(S1)
        
        self.set_current_yaml()
        return 

if __name__ =="__main__":
    

    E1 = Endpoint(endpoint_name="/v1/poc/aurora/schema")
    M1 = Method(verb="POST")
    M2 = Method(verb="GET")
    

    schema_name = E1.name + M1.verb

    p1_1 = Parameter(name="queryparam1", IN="query", desc="query parameter 1", required=True, parameter_value="string_param_value")
    #print(p1_1.to_open_api_3())
    p1_2 = Parameter(name="queryparam2", IN="query", desc="query parameter 2", required=True, parameter_value=2)
    #print(p1_2.to_open_api_3())    
    p1_3 = Parameter(name="pathparam1", IN="path", desc="query parameter 2", required=True, parameter_value=3.0)
    #print(p1_3.to_open_api_3())  
    r1_1 = Response(code=200, desc="Successful Response", schema_name=schema_name)
    #print(r1_1.to_open_api_3())

    r1_2 = Response(code=400, desc="Bad Request", schema_name="ApiResponse")
    #print(r1_2.to_open_api_3())
    M1.set_parameters(parameters=[p1_1, p1_2])
    M1.set_responses(responses=[r1_1])

    M2.set_responses(responses=[r1_1, r1_2]) # no params on this
    #print(M1.to_open_api_3())
    E1.set_methods(methods=[M1])

    mixed_object_body = {
        "item1": "value1",
        "item2": 2,
        "item3": 3.0,
        "item4": None
    }
    print('\n')
    S1 = Schema(response=r1_1, example=mixed_object_body)
    S1.to_open_api_3()
    C1 = Component()
    C1.set_schemas([S1])



    # OADB = OpenApiDocBuilder(file_location=None)
    # current_yaml = OADB.read_current_file()
    # current_yaml["paths"] = E1.to_open_api_3()
    # current_yaml.update(C1.to_open_api_3())
    # OADB.write_to_file(current_yaml)

    
    