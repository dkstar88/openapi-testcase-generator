def _default_string():
    return "string"


def _default_string_date():
    return "2017-07-21"


def _default_string_date_time():
    return "2017-07-21T17:32:28Z"


def _default_string_password():
    return "password"


def _default_string_byte():
    return "U3dhZ2dlciByb2Nrcw=="


def _default_string_uuid():
    return "00000000-0000-0000-0000-000000000000"


def _default_string_email():
    return "example@iherb.com"


def _default_string_uri():
    return "https://www.iherb.com/"


def _default_string_hostname():
    return "www.iherb.com"


def _default_string_ipv4():
    return "66.116.126.193"


def _default_string_ipv6():
    return "2001:0db8:0000:0000:0000:ff00:0042:8329"


string_format_dict = {
    None: _default_string,
    "date": _default_string_date,
    "date-time": _default_string_date_time,
    "password": _default_string_password,
    "byte": _default_string_byte,
    "uuid": _default_string_uuid,
    "email": _default_string_email,
    "uri": _default_string_uri,
    "hostname": _default_string_hostname,
    "ipv4": _default_string_ipv4,
    "ipv6": _default_string_ipv6,
}


def get_format_default(schema, swagger):
    if "schema" in schema:
        return get_format_default(schema["schema"], swagger)
    if schema:
        if schema.get("default"):
            return schema["default"]
        schema_type = schema["type"]
        if schema_type == "string":
            return string_format_dict[schema.get("format")]()
        elif schema_type == "integer":
            return 1
        elif schema_type == "number":
            return 2.5
        elif schema_type == "boolean":
            return True
        elif schema_type == "null":
            return None
        elif schema_type == "array":
            return [get_format_default(schema["items"], swagger)]
        elif schema_type == "object":
            obj = {}
            if schema.get("properties"):
                for k, prop in schema["properties"].items():
                    obj[k] = get_format_default(prop, swagger)
            return obj

    return None


def sanitize_name(name):
    result = name.replace("/", "-").replace("\\", "-").replace("{", "").replace("}", "")
    result = result.strip().strip("-").strip("_")
    return result
    
