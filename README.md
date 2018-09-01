# DevOps I - Jenkins and GitLab CI/CD Service

> **Consume and adapt, adapt and evolve.**

## Problem Statement

Our task was to *simulate* a DevOps pipeline with multiple components such as Jenkins CI, our own GitLab server and SciTools Understand, a static code analyzer.

### Breaking down the problem

1. We installed Docker(Community Edition) so as to run a GitLab server as a container on our own local machines.
2. We installed and configured Jenkins on our system, locally.
3. We set up a GitLab server and then connected our Jenkins instance to our GitLab server.
4. The next step was importing open source repositories from GitHub and pushing them onto our GitLab server.
5. Once we cloned the repositories onto our GitLab server, we create Jenkins jobs that trigger a CI pipeline when there is a push event in any of the GitLab repositories.
6. For this we needed to set up Web-hooks between GitLab repositories and respective Jenkins jobs.
7. We then used a static code analysis tool called Understand to generate Dependency graphs and other Analysis reports.
8. We also used the “git diff” command to find out certain files that may required to be retested due to their newly modified state.

### Detailed Explanation of steps

[!Jenkins](Jenkins.png)

#### Installing Docker

*For Mac:* Install the stable version of Docker Community Edition for Mac from [here.](https://docs.docker.com/docker-for-mac/install/)

*For Windows:* Install the stable version of Docker Community Edition for Windows from [here.](https://docs.docker.com/docker-for-windows/install/#download-docker-for-windows) If your system does not meet the requirements for Docker CE for Windows, you can use [Docker Toolbox](https://docs.docker.com/toolbox/overview/)

#### Installing Gitlab

To launch GitLab, run the following Docker command in the docker command line interface: 
```
sudo docker run --detach --name gitlab \
 --hostname gitlab.example.com \
 --restart always \ 
 --volume <Your_location_for_gitlab>/gitlab/config:/ etc/gitlab \    
 --volume <Your_location_for_gitlab>/gitlab/logs:/var/ log/gitlab \    
 --volume <Your_location_for_gitlab>/gitlab/data:/var/ opt/gitlab \ 
 --publish 30080:30080 \     
 --publish 20080:80 \ 
 --publish 30022:22 \ 
 --publish 32768:443 \ 
 --env GITLAB_OMNIBUS_CONFIG="external_url 'http:// gitlab.example.com:30080'; gitlab_rails['gitlab_shell_ssh_port']=30022;" \ 
 gitlab/gitlab-ce:latest

```

Wait a few minutes to let GitLab start inside the container. (You can view progress with docker logs -f gitlab.) Then, access GitLab via http://127.0.0.1:30080 (or, use your $DOCKER_HOST IP if you are not using localhost) and sign up. 

#### Installing Jenkins

Download the latest package for your system from [here.](https://jenkins.io/download/) Open the package and follow the instructions. Install the recommended plugins while setting up.

Once you have jenkins up and running, install the following plugins:

1. GitLab
2. Job DSL
3. Job DSL to XML
4. Jacoco
5. GitLab Auth
6. Git
7. Maven integration
8. Build with Parameters
9. SSH
10. Git Server
11. Git Client
12. SSH Credentials
13. SSH Agent
14. Violation Commit to GitLab
15. GitLab Hook

Configure the maven installation as per the documentation (HW1 Documentation.pdf)

#### Installing Python

Download the latest version of Python from https://www.python.org/downloads/. Make sure you download Python 3.x. as that is what we need for the [Understand API](https://scitools.com/support/python-api/)

#### Installing pip

Download the latest version of pip from https://pip.pypa.io/en/stable/installing/

#### Installing Understand

You can download the tool and apply for a non-commercial licence at https://scitools.com/non-commercial-license/. During the installation, check the box that lets you add Understand to the `PATH` variable(You can do this later too if you miss it). Once you have successfully installed the tool, you'll need to follow the steps given below to be able to use the [Python API](https://scitools.com/support/python-api/) for Understand

1. If you did not add Understand to the Path variable during installation, you will need to add the `SciTools/bin/<System>` directory to PATH.
On non-Windows systems, you may need to create an `STIHOME` environment variable that points to the <SciTools> directory.
2. Modify/Add the `PYTHONPATH` environment variable to include the module location, which is `SciTools/bin/<System>/Python`. For Mac users, the python module is in `Understand.app/Contents/MacOS/Python`. All that is necessary to load the module on Mac is to set `PYTHONPATH` to point to that directory and run python3. For example: `PYTHONPATH=/Applications/Understand.app/Contents/MacOS/Python python3`


## Description of the implementation

#### How to compile and run it

* In Main.py and Clone.py files, replace the Personal Access Token and URL of GitLab according to your setup. 
* Also you might have to change your network interface as a parameter in Main.py. (The default interface is the eth0 for WiFi on a Mac.)
* By that, we mean 'ipconfig getifaddr en0'

* run the following commands.

`sudo pip3 install -r requirements.txt`

`python3 Main.py`

* The repositories will be cloned into the root of the project and the Dependency graphs and other metrics generated by Understand will reside within these project folders.
    Developers can see their recommendations in the text file - RetestTheseFiles.txt, located in the root directory of the project.

* To run the acceptance tests run the following command

`nosetests --verbosity=2 <homework_repo_name>`

After running Main.py, your GitLab instance will have cloned all the repos from GitHub that meet the criteria of Language = Java.
You will also see all the Jenkins jobs have been generated and these jobs will trigger builds and Jacoco coverage reports on any push event in GitLab.   

#### Limitations of the implementation.
The repositories have to be cloned onto your local machine to generate the reports using the Understand API; This could have been done using a python/shell script in the jenkins build step, thus avoiding cloning the repositories locally.