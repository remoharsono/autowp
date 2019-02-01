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

Setup database:

```python
autowp setup --mongo-host=myhost --mongo-port=myport --mongo-user=myuser --mongo-pass=mypass
```

Secure your works:

```python
autowp security --profile=myprofilename
```

Login to your profile:

```python
autowp security login --profile=myprofilename
```

Change profile:

```python
autowp security profile --switch=myotherprofile
```

Detail profile:

```python
autowp security profile --name=myprofilename

// or 

autowp security profile --current // means current logged in profile
```

List profiles:

```
autowp security profiles
```

Logout from current session profile:

```python
autowp security --logout
```

Please take a note, that each time you are login using your profile, all your activities
will refer to your profile. This means, you can manage your wordpress sites based on your
profile.

---

Setup your resource hosts:

```python
autowp resource host --register=myhost --credentials=myuser,myip,mypass
```

Manage your wordpress site:

```python
autowp resource site --register=mydomain.com
```

Please take a note, that this cli app DO NOT register your domain site and pointing
to your servers.  Registering site means to helping us to manage your apps.

---

Simple wordpress installation:

```python
autowp wordpress app --install=mydomain.com --host=myhost --db-host=mydbhost --db-port=mydbport --db-user=mydbuser --db-pass=mydbpass
```

Mass installation:

```python
autowp wordpress app --mass-install=/path/to/mycsvfile
```
