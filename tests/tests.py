import unittest
import requests
import jenkins
from unittest.mock import Mock, patch
from nose.tools import assert_true, assert_is_not_none

#@patch('Main')
def test_request_response_GitHub():
	#mock_get.return_value.ok = True
	# Send a request to the API server and store the response.
	response = requests.get('https://api.github.com/search/repositories?q=language:java+topic:maven', auth = ("kshirsagarpratik", "Chinku95"))
	
	# Confirm that the request-response cycle completed successfully.
	assert_true(response.ok)

#@patch('Main')
def test_request_response_GitLab_Push():
	# mock_get.return_value.ok = True
	response = requests.post('http://localhost:30080/api/v4/projects', data = {'name':unittest}, headers = {'Private-Token':'9SsFv3LD6ijhGznMSjuK'})
	assert_is_not_none(response.ok)

#@patch('Main')
def test_request_response_jenkins():
	# mock_get.return_value.ok = True
	server = jenkins.Jenkins('http://localhost:8080/', username='pkshir2', password='jenkinsrocks') # Pass Jenkins host URL and credentials.
	user = server.get_whoami()
	assert_true(user)


#@patch('Main')
def test_request_response_GitLab_Pull():
	# mock_get.return_value.ok = True
	response = requests.get('http://localhost:30080/api/v4/projects?page=1&per_page=40', headers = {'Private-Token':'9SsFv3LD6ijhGznMSjuK'})
	assert_true(response.ok)
