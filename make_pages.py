#!/usr/bin/env python

import os
import shutil
from string import Template

import csscompressor
from htmlmin.decorator import htmlmin


OUTPUT_PATH = '_output'
TEMPLATE_PATH = 'templates'


def template(name):
    return os.path.join(TEMPLATE_PATH, '%s.html' % name)

def outfile(name):
    if name == 'index':
        return os.path.join(OUTPUT_PATH, '%s.html' % name)
    else:
        return os.path.join(OUTPUT_PATH, name, 'index.html')

@htmlmin(remove_comments=True,
         remove_empty_space=True)
def render_template(base, name):
    with open(template(name)) as content:
        return base.substitute(content=content.read())


# Create an output directory for the rendered files
if os.path.isdir(OUTPUT_PATH):
    shutil.rmtree(OUTPUT_PATH)
os.mkdir(OUTPUT_PATH)

# Get the contents of the base template, and render the pages
with open(template('base')) as f:
    base = Template(f.read())

# Write the templates
outfile
with open(outfile('index'), 'w') as g:
    g.write(render_template(base=base, name='index'))

for name in ['about', 'results', 'privacy', 'contact']:
    os.mkdir(os.path.join(OUTPUT_PATH, name))
    with open(outfile(name), 'w') as g:
        g.write(render_template(base=base, name=name))

# Install the CSS file, making sure we minify it first
os.mkdir(os.path.join(OUTPUT_PATH, 'css'))
with open('style.css') as cssfile, open(os.path.join(OUTPUT_PATH, 'css', 'style.css'), 'w') as outfile:
    data = cssfile.read()
    outfile.write(csscompressor.compress(data))

# Install the JS file.  I haven't found a good way to do the minification
# in Python, so I just do it by hand.
os.mkdir(os.path.join(OUTPUT_PATH, 'javascript'))
print("Don't forget to minify the JS file!")
with open('main.js') as jsfile, open(os.path.join(OUTPUT_PATH, 'javascript', 'main.min.js'), 'w') as outfile:
    data = jsfile.read()
    outfile.write(data)


# Create the CNAME file that GitHub Pages requires
with open(os.path.join(OUTPUT_PATH, 'CNAME'), 'w') as f:
    f.write('finduntaggedtumblrposts.com')