License
=======
See the attached LICENSE.txt file to see the license under which GraphLab Service Client is distributed.

Getting Started
===============
To install:
>>> pip install GraphLab-Service-Client

To import:
>>> from graphlab_service_client import PredictiveServiceClient

Using a config file (.ini file generated from Predictive Service):
>>> client = PredictiveServiceClient(config_file='/path/to/file.ini')

Using endpoint and api_key directly:
>>> client = PredictiveServiceClient(endpoint='', api_key='')
>>> results = client.query('uri', {'users':[111,222,333]})
>>> client.feedback('uri', {'requestid':'abcde-abcde'})

References
==========
A lot more documentation regarding the GraphLab Create is available here: http://graphlab.com and on our Forum at http://forum.graphlab.com

Contributors
============
GraphLab Team, http://graphlab.com (@graphlabteam)
