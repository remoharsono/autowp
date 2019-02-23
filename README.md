# AutoWP [IN DEVELOPMENT]

```
WARNING!

This tools still under active developments, please do not try to install it from pypi.
```

---

AutoWP is a command line interface application built to helping people managing
their wordpress applications.

Scopes:

- Auto installation on targeted server
- Mass installation on separated servers
- Resource managements (hosts, domains) 
- Setup Nginx as proxy and balancers for each site
- Secure usages, you can create a password to running this app

Note:

- This application need a ssh access to your servers, make sure you have configured
your ssh files with your servers.

# Requirements

- Python 3.7.x
- MongoDB

Just for recommendations:

- Install and manage your python versions using [pyenv](https://github.com/pyenv/pyenv)
- You can use docker to install [MongoDB](https://hub.docker.com/_/mongo)
- For OS environment, we are not test this application running using Windows, our recommendation is Linux (Ubuntu).
But as long as, python (and pip) installed on your machine, this app should works.

# Installations

Make sure you have python 3.7.x and [pipenv](https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv) installed on your system.

- Clone this repo
- run: `pipenv install '-e .'`
- run: `python setup.py develop` 

Configurations:

You need to set environment variables, following this way:

```
export AUTOWP_MONGO_HOST="<your_mongodb_uri>"
export AUTOWP_MONGO_DBNAME="<your_db_name">
export AUTOWP_SALT="<your_random_key_of_strings>"
```

Optional variables:

```
export AUTOWP_MONGO_CONNECT_TIMEOUT=<int> // default: 5000 (ms)
export AUTOWP_MONGO_SOCKET_TIMEOUT=<int> // default: 1000 (ms) 
export AUTOWP_MONGO_SERVER_SELECTION_TIMEOUT=<int> // default: 15000 (ms)
```

Place all of these variables in your `~/.bashrc` or `~/.zshrc` and dont forget
to activate them using `source`, example: `source ~/.bashrc` or `source ~/.zshrc`

# Usages

After clone this repo, "cd" to `autowp` folder, and run this available commands:

Manage profiles

```
python main.py profile:register myname mypass // register profiles
python main.py profile:delete myname // delete profile
python main.py profile:list // list of registered profiles
```

Manage security

```
python main.py security:login myname // will promp a question to input your password
python main.py security:logout // logged out from current session
python main.py security:current // show your current logged in profile
```
