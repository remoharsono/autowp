# AutoWP

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

Make sure you have python 3.7.x and pip installed on your system.

```python
pip install autowp
```

# Usages

Manage profiles

```
autowp profile:register myname mypass // register profiles
autowp profile:delete myname // delete profile
autowp profile:list // list of registered profiles
```

