#!/usr/bin/env python

# flake8: noqa

import os
import shutil
import string

import csscompressor
import htmlmin
import slimit


ASSET_PATH = 'assets'
OUTPUT_PATH = '_output'
TEMPLATE_PATH = 'templates'
BASE_TEMPLATE_PATH = os.path.join(TEMPLATE_PATH, 'base.html')


class Template(object):

    def __init__(self, name):
        self.name = name
        self.path = os.path.join(TEMPLATE_PATH, '%s.html' % name)

    def render(self):
        """
        Returns the rendered version of a template.
        """
        # All templates inherit from a base template. First read the
        # contents of that template.
        with open(BASE_TEMPLATE_PATH) as fin:
            base = string.Template(fin.read())

        # The base template has a single parameter 'content', so we
        # fill it in with the unique contents of this template.
        with open(self.path) as content:
            return base.substitute(content=content.read())

    def minify(self):
        """
        Returns the minified version of a template.
        """
        return htmlmin.minify(self.render().decode('utf8'),
                              remove_comments=True,
                              remove_empty_space=True)

    def export(self, use_subdir=True):
        """
        Writes the minified version of a template to the output
        directory.  If use_subdir is True, then it is written to
        index.html in a subdirectory of OUTPUT_PATH with the same
        name as the template.
        """
        if use_subdir:
            os.makedirs(os.path.join(OUTPUT_PATH, self.name))
            path_to_write = os.path.join(OUTPUT_PATH, self.name, 'index.html')
        else:
            path_to_write = os.path.join(OUTPUT_PATH, 'index.html')

        with open(path_to_write, 'w') as outfile:
            outfile.write(self.minify().encode('utf8'))


def build_site():
    """
    Does all the work to build the production version of the site.
    This includes:
     * Rendering the HTML templates
     * Minifying and setting up the CSS/JS files
     * Copying the favicons into place
     * Setting the site up for pushing to GitHub

    Assumes that the site has not already been built.
    """
    # Create a directory for the output
    os.makedirs(OUTPUT_PATH)

    # The index template is the landing page, so we write it to index.html
    # in the top-level of the output directory.
    index_page = Template('index')
    index_page.export(use_subdir=False)

    # Create and export all the other pages
    for name in ['about', 'contact', 'privacy', 'results']:
        page = Template(name)
        page.export()

    # Copy the favicons into place
    os.makedirs(os.path.join(OUTPUT_PATH, 'images'))
    for filename in ['favicon.ico', 'favicon.png', 'apple-touch-icon.png']:
        shutil.copyfile(src=os.path.join(ASSET_PATH, filename),
                        dst=os.path.join(OUTPUT_PATH, 'images', filename))

    # Copy the CSS file into place, and minify appropriately
    os.makedirs(os.path.join(OUTPUT_PATH, 'css'))
    with open(os.path.join(ASSET_PATH, 'style.css')) as infile, \
         open(os.path.join(OUTPUT_PATH, 'css', 'style.min.css'), 'w') as outfile:
        outfile.write(csscompressor.compress(infile.read()))

    # Copy the JS file into place, and minify appropriately
    os.makedirs(os.path.join(OUTPUT_PATH, 'javascript'))
    with open(os.path.join(ASSET_PATH, 'main.js')) as infile, \
         open(os.path.join(OUTPUT_PATH, 'javascript', 'main.min.js'), 'w') as outfile:
        outfile.write(slimit.minify(infile.read()))

    # GitHub Pages requires a CNAME file for custom domains.  Create
    # this file in the output path.
    # https://help.github.com/articles/adding-a-cname-file-to-your-repository/
    with open(os.path.join(OUTPUT_PATH, 'CNAME'), 'w') as outfile:
        outfile.write('finduntaggedtumblrposts.com')


def main():
    if os.path.isdir(OUTPUT_PATH):
        shutil.rmtree(OUTPUT_PATH)
    build_site()


if __name__ == '__main__':
    main()
