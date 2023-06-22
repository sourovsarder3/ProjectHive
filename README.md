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
First downlad code using git command or zip file.  
`git clone https://github.com/sourovsarder3/ProjectHive.git`  
I used Django channel and JavaScript websocket to establish real time message system. So we need Redis server. So you have to download and install Docker for installing redis server. So download Docker and install it then install redis server and run it using following command.  
`docker run -p 6379:6379 -d redis:5`  
Here 6379:6379 this option maps the host's port 6379 to the container's port 6379. This allows external applications to communicate with the Redis server running inside the container using the host's port 6379 and redis:5: This specifies the Redis image to use for creating the container. In this case, it refers to the Redis version 5 image. If the image is not available locally, Docker will automatically pull the image from the Docker Hub before creating the container.  
So you need to run this commmand everytime whenever you want to run the project.  
