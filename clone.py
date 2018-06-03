import requests
import gitlab
import sys
import os
import understand_report # our own file

def diffnund():
	parent_directory = os.getcwd()

	r = requests.get('http://localhost:30080/api/v4/projects?page=1&per_page=40', headers = {'Private-Token':'9SsFv3LD6ijhGznMSjuK'})
	for item in r.json():
		repo_name = item['name']
		repo_url = item['ssh_url_to_repo']
		os.system('git clone ' + repo_url)
		os.chdir(repo_name)
		os.system('git diff --stat HEAD HEAD~3 >> RetestTheseFiles.txt')
		os.chdir(parent_directory)
		print('Generating Understand Reports for '+ repo_name)
		udbPath = parent_directory +'/'+repo_name+'/test.udb'
		understand_report.create_udb(udbPath, 'Java', parent_directory + '/'+repo_name)
		understand_report.getUnderstandReport(udbPath, parent_directory + '/'+repo_name)
	print('Understand reports have been generated in their respective project roots.')

