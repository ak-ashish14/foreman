########
# Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.


# ctx is imported and used in operations
from cloudify import ctx

# put the operation decorator on any function that is a task
from cloudify.decorators import operation
import requests
import foreman
from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings()


@operation
def create_host(hostname, port, username, password, **kwargs):
    # setting node instance runtime property
    ctx.instance.runtime_properties['hostname'] = hostname
    #ctx.instance.runtime_properties['username'] = username
    #str=some_property1+some_property2
    ctx.logger.info("Trying to connect FICO Foreman server.")


    data="couchbase_v2"
    result=foreman.Foreman(hostname,port,username,password,False).search_environment(data)


    env_id=result['id']
    # TODO data should have the requirements regarding the instance 
    data={
    		'name':'ash-host-test01', 
    		'enviroment_id':1, 				# couchbase_v2
    		'architecture_id':1,					# x86_64
    		'domain_id':1,							# sdlab.fairisaac.com
    		'compute_resource_id':1,				# SDLAB(VMware)
    		'hostgroup_id': 23,						# VMware/couchbase
    		'compute_profile_id':2,					# 2 - medium	
    		'root_pass':'#ash14',
    		'location_id':1,						# SDLAB
    		'organization_id': 4,					# data center technology
    		'comment':'testing plugin.',
    		'compute_attributes':{'start':1}
    	  }
    print foreman.Foreman(hostname,port,username,password,False).create_host(data)

"""
    url=hostname+"/api/v2/locations"
    headers={'Content-Type':'application/json','Accept':'application/json'}
    r=requests.get(url,auth=HTTPBasicAuth(username,password),headers=headers, verify=False)
    print r.json()
"""



@operation
def delete_host(hostname, port, username, password, **kwargs):
    # setting node instance runtime property
    ctx.instance.runtime_properties['hostname'] = hostname
    #ctx.instance.runtime_properties['username'] = username
    #str=some_property1+some_property2
    ctx.logger.info("Trying to connect FICO Foreman server.")

    #host id needs to be fetched from the FOREMAN SERVER

    """
	HOST ID is not visible on the FOREMAN UI 
	Getting the HOST ID 
	1. make a GET request to /hosts?search=""
	2. result["id"]
    """


    host_id="2583"
    print foreman.Foreman(hostname,port,username,password,False).delete_host(host_id)



@operation
def get_environments(hostname, port, username, password, **kwargs):
    # setting node instance runtime property
    ctx.instance.runtime_properties['hostname'] = hostname
    #ctx.instance.runtime_properties['username'] = username
    #str=some_property1+some_property2
    ctx.logger.info("Trying to connect FICO Foreman server.")
    ctx.logger.info("Fetching enviroment details.")

    print foreman.Foreman(hostname,port,username,password,False).get_environments()
 

@operation
def search_environment(hostname, port, username, password, **kwargs):
    # setting node instance runtime property
    ctx.instance.runtime_properties['hostname'] = hostname
    #ctx.instance.runtime_properties['username'] = username
    #str=some_property1+some_property2
    ctx.logger.info("Trying to connect FICO Foreman server.")
    ctx.logger.info("Fetching enviroment details.")

    data="FFM_ORT"

    result=foreman.Foreman(hostname,port,username,password,False).search_environment(data)
    print result

@operation
def power_host(hostname, port, username, password, power_action, host_id, **kwargs):
	# setting node instance runtime property
    ctx.instance.runtime_properties['hostname'] = hostname
    #ctx.instance.runtime_properties['username'] = username
    #str=some_property1+some_property2
    ctx.logger.info("Trying to connect FICO Foreman server.")
    print foreman.Foreman(hostname,port,username,password,False).power_host(power_action,host_id)