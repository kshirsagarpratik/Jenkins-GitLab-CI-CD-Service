import jenkins
import requests
import gitlab
import xml.etree.ElementTree as ET
import os
import clone # our own file


r = requests.get('https://api.github.com/search/repositories?q=language:java+topic:maven', auth = ("kshirsagarpratik", "Chinku95"))
#r.json()
for item in r.json()['items']:
	print('Cloning into GitLab...')
	repo_url = item['clone_url']
	repo_name = item['name']
	print(repo_name)
	print(repo_url)

	g = requests.post('http://localhost:30080/api/v4/projects', data = {'name':repo_name,'import_url':repo_url}, headers = {'Private-Token':'9SsFv3LD6ijhGznMSjuK'})


os.system('ipconfig getifaddr en0') # assuming you are using en0 interface for wifi
input = input("Please type in the above IP address. If this gives an error please enter your local IP. You can find your local IP here: https://www.whatismyip.com/\n\n")
local_ip = str(input)

server = jenkins.Jenkins('http://localhost:8080/', username='pkshir2', password='jenkinsrocks') # Pass Jenkins host URL and credentials.
user = server.get_whoami()
#version = server.get_version()     # this method is bugged.
print('Hello %s from Jenkins' % (user['fullName']))

gl = gitlab.Gitlab('http://localhost:30080', private_token='9SsFv3LD6ijhGznMSjuK') # Pass the gitlab host URL and generated private API token (from gitlab.)
gl.auth()

r = requests.get('http://localhost:30080/api/v4/projects?page=1&per_page=40', headers = {'Private-Token':'9SsFv3LD6ijhGznMSjuK'})
for item in r.json():
	repo_name = item['name']
	repo_url = item['ssh_url_to_repo']
	# print(repo_name, repo_url)

# repo_name = 'versions-maven-plugin'
# repo_url = 'ssh://git@gitlab.example.com:30022/root/versions-maven-plugin.git'
	print('Creating Jenkins job and GitLab webhook for: ' + repo_name + ' located at ' + repo_url)
	tree = ET.parse('config.xml')
	root = tree.getroot()
	root[3][1][0].text = repo_name
	root[4][1][0][2].text = repo_url
	tree.write('output.xml')

	xmlstr = ET.tostring(root).decode()
	server.create_job(repo_name, xmlstr)

	project = gl.projects.get('root/' + repo_name)
	hooks = project.hooks.create({'url': 'http://' + local_ip + ':8080/project/' + repo_name, 'push_events': 1})

print('All Jenkins jobs have been created as well as GitLab webhooks have been set.\nAny push updates to any of these repositories will trigger the build step and publish the JaCoCo code coverage report.\nThank you.')

clone.diffnund() # invokes diffnund method from clone.py
