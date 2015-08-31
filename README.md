# untagged-tumblr-posts

This repo contains the source code for <http://finduntaggedtumblrposts.com>.

For the history of the site, see the
<a href="http://finduntaggedtumblrposts.com/about/">about page</a>.

## Building the site

To work on the site, you need to create a Python virtualenv, and then
install the requirements:

    virtualenv -p python3 venv
    source venv/bin/activate
    pip install -r requirements.txt

I use Python 2.7 to develop the site.  Moving to Python 3 is blocked
on [an issue with slimit](https://github.com/rspivak/slimit/issues/64),
the Python library I use for JavaScript minification.

All the key tasks are handled by the Makefile.  Help message with
`make help`:

    $ make help
    Makefile for "Find Untagged Tumblr Posts

    Usage:
       make html                           (re)generate the web site
       make clean                          remove the generated files
       make serve                          serve site at http://localhost:8000
       make github                         upload the web site via gh-pages
