import jsonschema
from jsonschema import validate

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hello {name}!')  # Press Ctrl+F8 to toggle the breakpoint.

def validate_json_schema():
    schema = {
        "type": "object",
        "properties": {
            "merchantID": {"type": "string"},
            "siteNickNameId": {"type": "string"},
            "countryCode": {"type": "string"},
            "currencyCode": {"type": "string"}
        },
        "required": ["merchantID"]
    }
    
    try:
        validate(instance={"merchantID":"GED","siteNickNameId":"shopee-3","countryCode":"PH","currencyCode":"PHP"}, schema=schema)
        validate(instance={"merchantID": "","siteNickNameId":"shopee-3","countryCode":"PH","currencyCode":"PHP"}, schema=schema)
        # validate(instance={"siteNickNameId":"shopee-3","countryCode":"PH","currencyCode":"PHP"}, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        print(err.path, err.message)
        return False
    return True


# Initiate app
# if __name__ == '__main__':
#     print_hi('World')
#     validateJsonSchema()
