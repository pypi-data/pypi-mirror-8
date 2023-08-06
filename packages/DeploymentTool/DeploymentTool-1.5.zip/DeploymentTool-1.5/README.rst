How to use:

1. easy_install DeploymentTool
2. after all dependency installed download the project at here https://pypi.python.org/pypi?:action=display&name=DeploymentTool&version=1.4
3. extract the downloaded file
4. go to the directory of extracted file or with cmd if using windows
5. go to Deployment directory and make sure manage.py file is there
6. run manage.py createsuperadmin
7. create database with name deploymentdb and back to the Deployment directory
8. run manage.py syncdb
9. run manage.py runserver
10. go to localhost:8000/admin and login with your newly created superadmin account
11. create new host and users
12. go to localhost:8000 and login with your superadmin account or newly added user