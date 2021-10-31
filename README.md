# finduntaggedtumblrposts.com

This repo contains the source code for [finduntaggedtumblrposts.com][root], which helps you find untagged posts on Tumblr.

![A screenshot of the site](screenshot.png)

[root]: https://finduntaggedtumblrposts.com
[jekyll]: https://jekyllrb.com/

## Motivation

The idea for this site started in 2013, when a friend was trying to go back and retag her old Tumblr posts.
Without a way to easily see all her untagged posts, it was impossible for her to be sure that she was done.
I wrote her <a href="https://alexwlchan.net/2013/08/untagged-tumblr-posts/">a Python script</a> to get the job done, and that was that.

In 2014, I was getting a lot of hits to that post, but a Python script isn’t very user friendly.
I wrote this site to be an easier way to get a list of your untagged posts, because clearly it was something people wanted.

All the source code is [on GitHub](https://github.com/alexwlchan/untagged-tumblr-posts), and released under the [MIT license](https://opensource.org/licenses/MIT).

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
