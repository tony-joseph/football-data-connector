import re
import requests


def fetch_data_from_api(endpoint, api_key='', options=None):
    """Fetches data from the endpoint and returns it

    :param endpoint: api endpoint to connect
    :param api_key: optional api key
    :param options: data to sent with api call
    :return: 
    """

    # Build headers
    headers = {}
    if api_key:
        headers['X-Auth-Token'] = api_key

    # Build data
    params = options if options else {}

    r = requests.get(endpoint, headers=headers, params=params)

    # Return the json data if request is successful
    if r.status_code == 200:
        return r.json()

    return []


def camel_to_snake(name):
    """Takes a string in camel case and converts it to snake case
    
    :param name: String to convert to snake case 
    :return: String in snake case
    """

    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def clean_object(data):
    """Takes data from api and build data dictionary with proper keys
    
    :param data: Dict data from api
    :return: Dict with proper keys and meta data removed
    """

    data_dict = {}
    for key in data.keys():
        new_key = key
        if key.startswith('_'):
            # Remove _ to prevent misinterpretation as private date
            new_key = key.replace('_', '', 1)

        data_dict[camel_to_snake(new_key)] = data[key]

    return data_dict
