# ProjectHive
ProjectHive is a web-based chat application for teamwork inspired by most popular team communication platfrom <b>Slack</b>.

## Feature
<li> Multiple Workspace for different teams
<li> Real-time Messaging
<li> Channels (Private and Open)
<li> Direct Messagging
<li> File Sharing
<li> File Searching inside a certain Workspace  

If you want to learn more about <b>ProjctHive</b> you can read the tesis paper against this project. [Click Here](PjojectHive.pdf)  

## Used Tools  
<li> Django
<li> JavaScript
<li> Django Channel & WebSocket
<li> Redis Server
<li> Docker

## Installation
First downlad the code from this Github repo using git command or zip file.  
```bash
git clone https://github.com/sourovsarder3/ProjectHive.git
```
I used Django channel and JavaScript websocket to establish real time message system using <b>Redis</b> server. So you have to download and install <b>Docker</b> for installing Redis server. So download Docker and install it. Now to install and run Redis server run the following command.  

```docker
docker run -p 6379:6379 -d redis:5
```
Here <b>6379:6379</b> this option maps the host's port 6379 to the container's port 6379. This allows external applications to communicate with the Redis server running inside the container using the host's port 6379. This <b>redis:5</b> specifies the Redis image to use for creating the container. In this case, it refers to the Redis version 5 image. If the image is not available locally, Docker will automatically pull the image from the Docker Hub before creating the container.  
So you need to run this commmand everytime whenever you want to run the project.  
Now install the requirment package and dependencies in python virtual environment. If you don't have pipenv installed then install it and run the following command to install all dependencies for this project.  

```python
pipenv install
```

It'll install all dependencies that used in this project. Now create a `.env` file in root directory of yor project and add following varialbes.  

```python
SECRET_KEY = 'Give your django security code'
EMAIL = 'Give your email address'
EMAIL_PASSWORD = 'Give your email api access token'
```  
To generate your own `SECRET_KEY` Here's how you can do it:  

Use django's function `get_random_secret_key()` to generate a new `SECRET_KEY` in your local environment. They can open a Python shell and execute the following commands:  


```python
from django.core.management.utils import get_random_secret_key

secret_key = get_random_secret_key()
print(secret_key)
```  
This will generate a new random SECRET_KEY and print it to the console. Now assign this key with  `SECRET_KEY`  variable.<br>
Now it's ready to run the server.  

## Summary
This project hasn't been tested or qualified yet. So maybe there are some extra file or extra line or bug that might be found. So if you have found any issue you can let me know. I'll try to fix it. And I used some demo messages in this project that might be found in the db.sqlite3 file. You can delete them if you no longer need these. Thank you. 
