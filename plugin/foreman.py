import json

import requests

# from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings()

FOREMAN_REQUEST_HEADERS = {
    'content-type': 'application/json',
    'accept': 'application/json'
}
FOREMAN_API_VERSION = 'v2'


ARCHITECTURES = 'architectures'
ARCHITECTURE = 'architecture'
COMPUTE_ATTRIBUTES = 'compute_attributes'
COMPUTE_ATTRIBUTE = 'compute_attribute'
COMPUTE_PROFILES = 'compute_profiles'
COMPUTE_PROFILE = 'compute_profile'
COMPUTE_RESOURCES = 'compute_resources'
COMPUTE_RESOURCE = 'compute_resource'
ENVIRONMENTS = 'environments'
ENVIRONMENT = 'environment'
HOSTS = 'hosts'
HOST = 'host'
HOSTGROUPS = 'hostgroups'
HOSTGROUP = 'hostgroup'
IMAGES = 'images'
IMAGE = 'image'
LOCATIONS = 'locations'
LOCATION = 'location'
MEDIA = 'media'
MEDIUM = 'medium'
OPERATINGSYSTEMS = 'operatingsystems'
OPERATINGSYSTEM = 'operatingsystem'
ORGANIZATIONS = 'organizations'
ORGANIZATION = 'organization'
OS_DEFAULT_TEMPLATES = 'os_default_templates'
OS_DEFAULT_TEMPLATE = 'os_default_template'
PARAMETERS = 'parameters'
PARAMETER = 'parameter'
PARTITION_TABLES = 'ptables'
PARTITION_TABLE = 'ptable'
PERMISSIONS = 'permissions'
PERMISSION = 'permission'
POWER = 'power'
ROLES = 'roles'
ROLE = 'role'
SUBNETS = 'subnets'
SUBNET = 'subnet'

"""
    def _get_request_error_message(self, data):
        request_json = data.json()
        if 'error' in request_json:
            request_error = data.json().get('error')
        elif 'errors' in request_json:
            request_error = data.json().get('errors')

        if 'message' in request_error:
            error_message = request_error.get('message')
        elif 'full_messages' in request_error:
            error_message = ', '.join(request_error.get('full_messages'))
        else:
            error_message = str(request_error)

        return error_message


COMMON_PARAMETERS = 'common_parameters'
COMMON_PARAMETER = 'common_parameter'
FILTERS = 'filters'
FILTER = 'filter'
AUTH_SOURCE_LDAPS = 'auth_source_ldaps'
AUTH_SOURCE_LDAP = 'auth_source_ldap'
REALMS = 'realms'
REALM = 'realm'
SMART_PROXIES = 'smart_proxies'
SMART_PROXY = 'smart_proxy'
TEMPLATE_KINDS = 'template_kinds'
USERS = 'users'
USER = 'user'
DOMAINS = 'domains'
DOMAIN = 'domain'
CONFIG_TEMPLATES = 'config_templates'
CONFIG_TEMPLATE = 'config_template'
SETTING = 'setting'
SETTINGS = 'settings'

"""

class ForemanError(Exception):
    """ForemanError Class
    Simple class to handle exceptions while communicating to Foreman API
    """

    def __init__(self, url, status_code, message):
        self.url = url
        self.status_code = status_code
        self.message = message
        super(ForemanError, self).__init__()

class Foreman:

    def __init__(self, hostname, port, username, password, ssl=True):
        """Init
        """
        self.__auth = (username, password)
        self.hostname = hostname
        self.port = port
        #self.url_scheme = ("http", "https")[ssl]
        self.url_scheme="http"

        self.url = "{0}://{1}:{2}/api/{3}".format(
            self.url_scheme,
            self.hostname,
            self.port,
            FOREMAN_API_VERSION,
        )
        """

        self.url = "{0}:{1}/api/{2}".format(
            self.hostname,
            self.port,
            FOREMAN_API_VERSION,
        )
        """

        print hostname+"  :::::::::: initializing url :::::::::::::: "+self.url


    def _get_resource_url(self, resource_type, resource_id=None, component=None, component_id=None):
        url = self.url + '/' + resource_type
        if resource_id:
            url = url + '/' + str(resource_id)
            if component:
                url = url + '/' + component
                if component_id:
                    url = url + '/' + str(component_id)

        print "setting url :::::::::::::: "+url
        return url

    def _handle_request(self, req):
        if req.status_code in [200, 201]:
            return json.loads(req.text)
        elif req.status_code == 404:
            error_message = 'Not found'
        else:
            print "Error with Handle_REQ"+str(req)
#error_message = self._get_request_error_message(data=req)

#raise ForemanError(url=req.url,status_code=req.status_code,message=error_message)

    def _get_request(self, url, data=None):
        """Execute a GET request agains Foreman API
        Args:
          resource_type (str): Name of resource to get
          component (str): Name of resource components to get
          component_id (str): Name of resource component to get
          data (dict): Dictionary to specify detailed data
        Returns:
          Dict
        """
        req = requests.get(url=url,
                           data=data,
                           auth=self.__auth,
                           verify=False)
        return self._handle_request(req)


    def _post_request(self, url, data):
            """Execute a POST request against Foreman API
            Args:
              resource_type (str): Name of resource type to post
              component (str): Name of resource to post
              data (dict): Dictionary containing component details
            Returns:
              Dict
            """
            req = requests.post(url=url,
                                data=json.dumps(data),
                                headers=FOREMAN_REQUEST_HEADERS,
                                auth=self.__auth,
                                verify=False)
            return self._handle_request(req)
    
    def _delete_request(self, url):
        """Execute a DELETE request against Foreman API
        Args:
          resource_type (str): Name of resource type to post
          resource_id (str): Resource identified
        Returns:
          Dict
        """
        req = requests.delete(url=url,
                              headers=FOREMAN_REQUEST_HEADERS,
                              auth=self.__auth,
                              verify=False)
        return self._handle_request(req)

    def _put_request(self, url, data):
        """Execute a PUT request against Foreman API
        Args:
          resource_type (str): Name of resource type to post
          resource_id (str): Resource identified
          data (dict): Dictionary of details
        Returns:
          Dict
        """
        req = requests.put(url=url,
                           data=json.dumps(data),
                           headers=FOREMAN_REQUEST_HEADERS,
                           auth=self.__auth,
                           verify=False)
        return self._handle_request(req)




    def get_resources(self, resource_type, resource_id=None, component=None):
        """ Return a list of all resources of the defined resource type
        Args:
           resource_type: Type of resources to get
           resource_id (str): Resource identified
           component (str): Component name to request
           component_id (int): Component id to request
        Returns:
           list of dict
        """
        url = self._get_resource_url(resource_type=resource_type,
                                     resource_id=resource_id,
                                     component=component)
        request_result = self._get_request(url=url,
                                           data={'page': '1', 'per_page': 99999})
        return request_result.get('results')


    def get_resource(self, resource_type, resource_id, component=None, component_id=None):
        """ Get information about a resource
        If data contains id the resource will be get directly from the API.
        If id is not specified but name the resource will be searched within
        the database.
        If found the id of the research will be used. If not found None will
        be returned.
        :rtype : object
        Args:
           resource_type (str): Resource type
           resource_id (str): Resource identified
           component (str): Component name to request
           component_id (int): Component id to request
        Returns:
           dict
        """
        url = self._get_resource_url(resource_type=resource_type,
                                     resource_id=resource_id,
                                     component=component,
                                     component_id=component_id)
        return self._get_request(url=url)

    def update_resource(self, resource_type, resource_id, data, component=None, component_id=None):
        url = self._get_resource_url(resource_type=resource_type, resource_id=resource_id,
                                     component=component, component_id=component_id)
        return self._put_request(url=url, data=data)


    def create_resource(self, resource_type, resource, data,resource_id=None, component=None, additional_data=None):
        """ 
        Create a resource by executing a post request to Foreman
            Execute a post request to create one <resource> of a <resource type>.
            Foreman expects usually the following content:
            {
              "<resource>": {
                "param1": "value", 
                "param2": "value",
                ...
                "paramN": "value"
              }
            }
            <data> has to contain all parameters and values of the resource to be
            created. They are passed as {<resource>: data}.
            As not all resource types can be handled in this way <additional_data>
            can be used to pass more data in. All key/values pairs will be passed
            directly and not passed inside '{<resource>: data}.
            Args:
               data(dict): Hash containing parameter/value pairs
        """
        url = self._get_resource_url(resource_type=resource_type, resource_id=resource_id,component=component)
        resource_data = {}

        resource_data[resource] = data
        return self._post_request(url=url, data=resource_data)

    '''
        def search_resource(self, resource_type, data):
            search_data = {'search': '', 'per_page': 1000 }

            for key, value in data.items():
                if search_data['search']:
                    search_data['search'] += ' AND '
                search_data['search'] += (key + ' == ')

                if isinstance(value, int):
                    search_data['search'] += str(value)
                elif isinstance(value, str):
                    search_data['search'] += ('"' + value + '"')
                else:
                    TypeError("Type {0} of search key {1} not supported".format(type(value), key))

            url = self._get_resource_url(resource_type=resource_type)
            results = self._get_request(url=url, data=search_data)
            result = results.get('results')

            if len(result) == 1:
                return result[0]

            return result
    '''


    def delete_resource(self, resource_type, resource_id, component=None, component_id=None):
        url = self._get_resource_url(resource_type=resource_type, resource_id=resource_id,
                                     component=component, component_id=component_id)
        return self._delete_request(url=url)    

    # USE "VALUE"
    def search_resource(self,resource_type, value):
        search_data = {'search': ''}
        if isinstance(value, int):
            search_data['search'] += str(value)
        elif isinstance(value, str):
            search_data['search'] += ('"' + value + '"')
        else:
            #TypeError("Type {0} of search key {1} not supported".format(type(value), key))
            print "Error with GET data."

        url = self._get_resource_url(resource_type=resource_type)
        results = self._get_request(url=url, data=search_data)
        result = results.get('results')
        


        if len(result) == 1:
            return result[0]
        return result

    def power_host(self,power_action, host_id):
        data={
                'id':host_id,
                'power_action':power_action
            }
        return self.update_resource(resource_type=HOSTS,resource_id=host_id,data=data,component=POWER)

# VALUE is a STRING OR INTEGER
    def search_architecture(self, data):
        return self.search_resource(resource_type=ARCHITECTURES, value=data)

    def search_environment(self,data):
        return self.search_resource(resource_type=ENVIRONMENTS, value=data)

    def create_host(self, data):
        return self.create_resource(resource_type=HOSTS, resource=HOST, data=data)

    def delete_host(self, id):
        return self.delete_resource(resource_type=HOSTS, resource_id=id)
    
    def get_environments(self):
        return self.get_resources(resource_type=ENVIRONMENTS)
