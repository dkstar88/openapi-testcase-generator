import datetime
import jsonref as json
import os
from pathlib import Path

import click
import requests
from jinja2 import Template

from schema_default import get_format_default, sanitize_name


class Endpoint:

    JSON_CONTENT_TYPES = ["application/json", "text/json"]

    def __init__(self, path, method, data, swagger):
        self.path = path
        self.original_path = path
        self.method = method
        self.query_parameters = []
        self.json_request = []
        self.default_query = {}
        self.default_post_body = None
        self._swagger = swagger
        self.load_from_dict(data)

    def load_from_dict(self, data):
        if "tags" in data:
            self.tag = data["tags"][0]
        self.summary = data.get("summary")
        self.description = data.get("description")
        self.name = data.get("operationId", self.method + "-" + sanitize_name(self.path))
        self.responses = data["responses"]
        if "parameters" in data:
            for param in data["parameters"]:
                param["default"] = default_value(param, self._swagger)
                if param["in"] == "query":
                    self.query_parameters.append(param)
                    self.default_query[param.get("name")] = param["default"]
                elif param["in"] == "path":
                    self.path = self.path.replace("{" + param.get("name") + "}", str(param["default"]))
                    self.default_query[param.get("name")] = param["default"]       

        # # Get JSON request data
        # for json_type in self.JSON_CONTENT_TYPES:
        #     if isinstance(data.requestBody, RequestBody):
        #         if json_type in data.requestBody.content:
        #             self.json_request = default_value(data.requestBody.content[json_type], self._swagger)
        #             break


def fetch_swagger(url):
    r = requests.get(url)
    return json.loads(r.content)


def ensure_dir(filename):
    directory = os.path.dirname(filename)
    Path(directory).mkdir(parents=True, exist_ok=True)
    pass


def get_reference_default(ref, swagger):
    pass


def default_value(prop, swagger):
    result = {}
    return get_format_default(prop, swagger)


HTTP_METHODS = ["get", "post", "put", "delete", "patch", "trace", "head", "options"]


@click.command()
@click.option("--url", help="Swagger url")
@click.option("--file", help="Swagger json file")
def import_swagger(url, file):
    # Load feature template
    feature_template = None
    with open('templates/testcase.feature.jinja') as file_:
        feature_template = Template(file_.read())

    data = None
    if url:
        data = fetch_swagger(url)
    elif file:
        with open(file) as swagger_file:
            data = json.loads(swagger_file.read())

    if data is None:
        exit(1)


    tag_endpoints = {}
    for path, path_data in data["paths"].items():
        for method in HTTP_METHODS:
            if method in path_data:
                method_data = path_data[method]
                if method_data:
                    endpoint = Endpoint(path, method, method_data, data)
                    # print("%s - %s" % (endpoint.method, endpoint.path))
                    if endpoint.tag in tag_endpoints:
                        tag_endpoints[endpoint.tag].append(endpoint)
                    else:
                        tag_endpoints[endpoint.tag] = [endpoint]


    for tag, endpoints in tag_endpoints.items():
        print("----- %s ------" % tag)
        for endpoint in endpoints:
            output = feature_template.render({
                "endpoint": endpoint
            })
            filename = "features/%s/%s.feature" % (tag, endpoint.name)
            ensure_dir(filename)
            with open(filename, "w") as w:
                w.write(output)                    
            print("%s - %s" % (endpoint.method, endpoint.path))
            if endpoint.default_query:
                print("Query: ", endpoint.default_query)
            if endpoint.json_request:
                print("Request: ", endpoint.json_request)


if __name__ == '__main__':
    import_swagger()
