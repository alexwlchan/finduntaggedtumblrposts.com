# finduntaggedtumblrposts.com

This repo contains the source code for [finduntaggedtumblrposts.com][root].
It's a static site built with [Jekyll][jekyll].

For the history of the site, see the site's [about page][about].

![](screenshot.png)

[root]: https://finduntaggedtumblrposts.com
[about]: https://finduntaggedtumblrposts.com/about/
[jekyll]: https://jekyllrb.com/

## Building the site

You need Git, make and Docker installed.

To build the site locally:

```console
$ git clone git@github.com:alexwlchan/finduntaggedtumblrposts.com.git
$ make serve
```

The site should be running on <http://localhost:6060>.
If you make changes to the source files, it will automatically update.

To build a one-off set of static HTML files:

```console
$ make build
```

## Deploying the site

The site can be deployed with Make:

```console
$ make deploy
```

You need to have SSH access to the Linode instance running the site.
