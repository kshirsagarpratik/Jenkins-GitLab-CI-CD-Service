import unittest
import requests
from nose.tools import assert_true

def test_request_response():
	# Send a request to the API server and store the response.
	response = requests.get('http://jsonplaceholder.typicode.com/todos')
	
	# Confirm that the request-response cycle completed successfully.
	assert_true(response.ok)
