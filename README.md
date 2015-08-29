#Groupdynamics


##General Idea
An analytics tool to visualize and understand how you and your friends interact in your Whatsapp groups.

##Toolset

The following tools are proposed for the different parts.

 - Backend: Python with [Flask](http://flask.pocoo.org/) and [uWSGI](https://uwsgi-docs.readthedocs.org/en/latest/)
 - Frontend: [AngularJS](https://angularjs.org/) with [Highcharts.js](http://www.highcharts.com/) for visualization.
 - [Docker](https://www.docker.com/) for containerization
 - [AWS ECS](https://aws.amazon.com/ecs/) for hosting.

##Development

###Clone repository

First, clone into repository via

```bash
git clone git@github.com:BowTieProject/groupdynamics.git
cd groupdynamics
```

Next, checkout fetch all existing branches and checkout the desired one.
```bash
git fetch
git checkout <branch-name>
```

###Backend: Setting up the Virtual Environment

We use virtualenv to isolate the Python distribution and packages from the host's own Python distribution. 

Check if there is a venv folder
```bash
ls
<list-of-folders>
```
If there is no virtualenv, do:

if your system has a python2.7 distribution as default:
```bash
virtualenv venv
```

if your system has any other python distribution as default (and assuming you've installed python 2.7):
```bash
virtualenv -p /usr/local/bin/python2.7 --no-site-packages venv
```

Now, activate the virtual environment

```bash
source venv/bin/activate
```

install the required packages
```bash
pip install -r requirements.txt
```

and to run the app
```bash
python run_backend.py
```

###Frontend: Setting up the Yeoman Toolset

GroupStats is scaffolded using [yo:angular](https://github.com/yeoman/generator-angular) which in turn requires [Node](https://nodejs.org/).

To install Node, it is highly recommended that you use nvm. Follow the instructions in https://github.com/creationix/nvm to install it in your computer. Basically you just need to run:

```bash
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.25.4/install.sh | bash
```
Once you've installed nvm, you need to install the proper Node version:

```bash
nvm install v0.12
```

Now use that version:
```bash
nvm use v0.12
```

Ok, install the required libraries using npm:

```bash
npm install -g grunt-cli bower yo generator-karma generator-angular
```

we should now install the required dependencies using bower and npm:
```bash
npm install
bower install
```

###Frontend: Serving the GUI

You probably want to serve your GUI so you can see changes as you make them. Grunt allows you to serve a live GUI that will update whenever it detects a change in the code:

```bash
grunt serve
```
This, however, will not boot up the backend. If you want to test the entire application do

```bash
grunt build
```
and then after it is built run the ```run_backend.py``` command as seen above.

##Deployment

GroupStats uses Docker and AWS for it's deployment. The deployment process consists of the following:


- On commit to the **master** branch, there is a commit-hook that calls Docker Hub to build the image. The steps needed to build the image are explicitly described in the **Dockerfile**. 
- Once the image is built, the admin manually goes to AWS's EC2 Container Service (**ECS**) and updates the service, pulling the latest Docker image (This piece could, and should, automated in the future deploying every time the docker image has been updated). 