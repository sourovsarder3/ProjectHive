# ProjectHive
ProjectHive is a web-based chat application for teamwork inspired by most popular team communication platfrom 'Slack'. <br>

## Feature
<li> Multiple Workspace for different teams
<li> Real-time Messaging
<li> Channels
<li> Direct Messages
<li> File Sharing
<li> File Searching inside a certain Workspace  
<br>
<br>
If you want to learn more about <b>ProjctHive</b> you can read the tesis paper against this project. <a src='PjojectHive.pdf'>Click here.</a> <br> <br>

## Installation
First downlad code using git command or zip file.<br><br>
`git clone https://github.com/sourovsarder3/ProjectHive.git`<br><br>
I used Django channel and JavaScript websocket to establish real time message system. So we need Redis server. So you have to download and install Docker for installing redis server. So download Docker and install it then install redis server and run it using following command.<br><br>
`docker run -p 6379:6379 -d redis:5`<br><br>
Here 6379:6379 this option maps the host's port 6379 to the container's port 6379. This allows external applications to communicate with the Redis server running inside the container using the host's port 6379 and redis:5: This specifies the Redis image to use for creating the container. In this case, it refers to the Redis version 5 image. If the image is not available locally, Docker will automatically pull the image from the Docker Hub before creating the container.  
So you need to run this commmand everytime whenever you want to run the project.  
Now install the requirment package and dependencies in python virtual environment. If you don't have pipenv installed the install it and then run the following command. <br><br>
`pipenv install` <br><br>

It'll install all dependencies. Now create a .env file in root directory of yor project and add following varialbes. <br><br>

```python
SECRET_KEY = 'Give your django security code'
EMAIL = 'Give your email address'
EMAIL_PASSWORD = 'Give your email api access token'
```
<br>
To generate your own SECRET_KEY. Here's how you can do it: <br>
Use Django's function get_random_secret_key() to generate a new SECRET_KEY in their local environment. They can open a Python shell and execute the following commands: <br><br>

```python
from django.core.management.utils import get_random_secret_key

secret_key = get_random_secret_key()
print(secret_key)
``` 
<br>
This will generate a new random SECRET_KEY and print it to the console. Now assign this key with SECRET_KEY variable.<br>
Now it's ready to run the server.<br><br>

## Summary
This project hasn't been tested or qualified yet. So maybe there are some extra file or extra line or bug that might be found by you. So if you have found any issue you can let me know. I'll try to fix it. And I used some demo messages in this project that might be found in the db.sqlite3 file. You can delete them if you no longer need these. Thank you. 