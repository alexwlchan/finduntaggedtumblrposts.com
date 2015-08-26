# untagged-tumblr-posts

This repo contains the source code for <http://finduntaggedtumblrposts.com>.

For the history of the site, see the <a href="http://finduntaggedtumblrposts.com/about/">about page</a>.

## Building the site

To build the site:

    pip install -r requirements.txt
    python make_pages.py

Then push the output directory to the gh-pages branch on GitHub:

    ghp-import -p _output
