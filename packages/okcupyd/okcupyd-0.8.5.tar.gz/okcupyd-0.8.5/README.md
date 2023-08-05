<!--THIS FILE IS AUTO GENERATED; DO NOT EDIT IT MANUALLY.
[EDIT README.rst insted.-->
[![Build Status](https://travis-ci.org/IvanMalison/okcupyd.svg?branch=master)](https://travis-ci.org/IvanMalison/okcupyd)[![Documentation Status](https://readthedocs.org/projects/okcupyd/badge/?version=latest)](http://okcupyd.readthedocs.org/en/latest/)

Getting Started
===============

Installation/Setup
------------------

### pip/PyPI

okcupyd is available for install from PyPI. If you have pip you can
simply run:

``` {.sourceCode .bash}
pip install okcupyd
```

to make okcupyd available from import in python.

### From Source

You can install from source by running the setup.py script included as
part of this repository as follows:

``` {.sourceCode .bash}
python setup.py install
```

This can be useful if you want to install a version that has not yet
been released on PyPI.

### From Docker

okcupyd is available on docker (see
<https://registry.hub.docker.com/u/imalison/okcupyd/>)

If you have docker installed on your machine, you can run

``` {.sourceCode .bash}
docker run -t -i imalison/okcupyd okcupyd
```

to get an interactive okcupyd shell.

Use
---

### Interactive

Installing the okcupyd package should add an executable script to a
directory in your \$PATH that will allow you to type okcupyd to enter an
interactive ipython shell that has been prepared for use with okcupyd.
Before the shell starts, you will be prompted for your username and
password.

### Credentials

If you wish to avoid entering your password each time you start a new
session you can do one of the following things:

1.  Create a python module (.py file) with your username and password
    set to the variables USERNAME and PASSWORD respectively. You can
    start an interactive session with the USERNAME and PASSWORD stored
    in my\_credentials.py in the current working directory of the
    project by running:

``` {.sourceCode .bash}
PYTHONPATH=. okcupyd --credentials my_credentials
```

The PYTHONPATH=. at the front of this command is necessary to ensure
that the current directory is searched for modules.

2.  Set the shell environment variables OKC\_USERNAME and OKC\_PASSWORD
    to your username and password respectively. Make sure to export the
    variables so they are visible in processes started from the shell.
    You can make a credentials.sh file to do this using the following
    template:

``` {.sourceCode .bash}
export OKC_USERNAME='your_username'
export OKC_PASSWORD='your_password'
```

Simply run source credentials.sh to set the environment variables and
your shell should be properly configured. Note that this approach
requires that the relevant environment variables be set before
okcupyd.settings is imported.

3\. Manually override the values in okcupyd/settings.py. This method is
not recommended because it requires you to find the installation
location of the package. Also, If you are working with a source
controlled version, you could accidentally commit your credentials.

### Using `--credentials` in a custom script

The \~okcupyd.util.misc.add\_command\_line\_options and
\~okcupyd.util.misc.handle\_command\_line\_options can be used to make a
custom script support the `--credentials` and `--enable-loggers` command
line flags. The interface to these functions is admittedly a little bit
strange. Refer to the example below for details concerning how to use
them:

``` {.sourceCode .python}
import argparse
parser = argparse.ArgumentParser()
util.add_command_line_options(parser.add_argument)
args = parser.parse_args()
util.handle_command_line_options(args)
```

Basic Examples
--------------

All examples in this section assume that the variable u has been
initialized as follows:

``` {.sourceCode .python}
import okcupyd
u = okcupyd.User()
```

### Searching profiles

To search through the user:

``` {.sourceCode .python}
profiles = u.search(age_min=26, age_max=32)
for profile in profiles[:10]:
    profile.message("Pumpkins are just okay.")
```

To search for users that have answer a particular question in a way that
is consistent with the user's preferences for that question:

``` {.sourceCode .python}
user_question = user.questions.very_important[0]
profiles = u.search(question=user_question)
for profile in profiles[:10]:
    their_question = profile.find_question(user_question.id)
    profile.message("I'm really glad that you answered {0} to {1}".format(
        their_question.their_answer, their_question.question.text
    ))
```

The search functionality can be accessed without a \~.okcupyd.user.User
instance:

``` {.sourceCode .python}
from okcupyd.search import SearchFetchable

for profile in SearchFetchable(attractiveness_min=8000)[:5]:
    profile.message("hawt...")
```

For more details about what filter arguments can be used with these
search functions, see the doucmentation for
\~.okcupyd.search.SearchFetchable

### Messaging another user

``` {.sourceCode .python}
u.message('foxylady899', 'Do you have a map?')
# This has slightly different semantics; it will not look through the user's
# inbox for an existing thread.
u.get_profile('foxylady889').message('Do you have a map?')
```

### Rating a profile

``` {.sourceCode .python}
u.get_profile('foxylady899').rate(5)
```

### Mailbox

``` {.sourceCode .python}
first_thread = u.inbox[0]
print(first_thread.messages)
```

### Quickmatch, Essays, Looking For, Details

You can access the essays, looking for attributes and detail attributes
of a profile very easily

``` {.sourceCode .python}
profile = u.quickmatch()
print(profile.essays.self_summary)
print(profile.looking_for.ages)
print(profile.details.orientation)
```

The data for these attributes is loaded from the profile page, but it
should be noted that this page is only loaded on demand, so the first of
these attribute access calls will make an http request.

A logged in user can update their own details using these objects:

``` {.sourceCode .python}
user.profile.essays.self_summary = "I'm pretty boring."
user.profile.looking_for.ages = 18, 19
user.profile.details.ethnicities = ['asian', 'black', 'hispanic']
```

These assignments will result in updates to the okcupid website. When
these updates happen, subsequent access to any profile attribute will
result in a new http request to reload the profile page.

Development
-----------

### tox

If you wish to contribute to this project, it is recommended that you
use tox to run tests and enter the interactive environment. You can get
tox by running

``` {.sourceCode .bash}
pip install tox
```

if you do not already have it.

Once you have cloned the project and installed tox, run:

``` {.sourceCode .bash}
tox -e py27
```

This will create a virtualenv that has all dependencies as well as the
useful ipython and ipdb libraries installed, and run all okcupyds test
suite.

If you want to run a command with access to a virtualenv that was
created by tox you can run

``` {.sourceCode .bash}
tox -e venv -- your_command
```

To use the development version of the interactive shell (and avoid any
conflicts with versions installed in site-packages) you would run the
following command:

``` {.sourceCode .bash}
tox -e venv -- okcupyd
```

### git hooks

It is recommended that you install the git hooks that are included in
this repository by running

``` {.sourceCode .bash}
bin/create-githook-symlinks.sh
```

from the root directory of the repository.

This is only important (at the moment) if you plan to edit README.rst.

