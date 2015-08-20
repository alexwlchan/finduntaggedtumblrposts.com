# untagged-tumblr-posts

This repo contains the source code for <http://finduntaggedtumblrposts.com>.

To build the site:

    pip install -r requirements.txt
    python make_pages.py

That will compile the templates and move all the appropriate files into the _output directory. I then push that directory to the gh-pages branch on GitHub, from which the site is served.

For the history of the site, see the <a href="http://finduntaggedtumblrposts.com/about/">about page</a>.