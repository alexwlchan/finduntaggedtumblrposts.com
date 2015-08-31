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

I use Python 3.4 to develop the site.  Last time I checked, the scripts
weren't working with Python 2.x

To build the site:
 
    python make_pages.py

Then push the output directory to the gh-pages branch on GitHub:

    ghp-import -p _output
