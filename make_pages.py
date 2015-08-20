#!/usr/bin/env python

import os
import shutil
from string import Template

OUTPUT_PATH = '_output'
TEMPLATE_PATH = 'templates'


def template(name):
    return os.path.join(TEMPLATE_PATH, '%s.html' % name)

def outfile(name):
    if name == 'index':
        return os.path.join(OUTPUT_PATH, '%s.html' % name)
    else:
        return os.path.join(OUTPUT_PATH, name, 'index.html')

def render_template(base, name):
    with open(template(name)) as content, open(outfile(name), 'w') as idx:
        idx.write(base.substitute(content=content.read()))



def main():

    # Create an output directory for the rendered files
    # if os.path.isdir(OUTPUT_PATH):
    #     shutil.rmtree(OUTPUT_PATH)
    # os.mkdir(OUTPUT_PATH)

    # Get the contents of the base template, and render the pages
    with open(template('base')) as f:
        base = Template(f.read())

    render_template(base=base, name='index')

    for name in ['about', 'results', 'privacy', 'contact']:
        # os.mkdir(os.path.join(OUTPUT_PATH, name))
        render_template(base=base, name=name)


    # Move the static assets directories
    # for staticdir in ['css', 'javascript']:
        # shutil.copytree(staticdir, os.path.join(OUTPUT_PATH, staticdir))



if __name__ == '__main__':
    main()