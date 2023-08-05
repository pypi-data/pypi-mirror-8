# This application is derived from Dan Mackinlay's sphinxcontrib.feed package.
# The original can be found at http://bitbucket.org/birkenfeld/sphinx-contrib/src/tip/feed/

import os.path
import subprocess
import time

from feedformatter import Feed

from sphinx.application import ENV_PICKLE_FILENAME
from sphinx.util.console import bold


def setup(app):
    """ see: http://sphinx.pocoo.org/ext/appapi.html
        this is the primary extension point for Sphinx
    """
    from sphinx.application import Sphinx
    if not isinstance(app, Sphinx): return
    app.add_config_value('feed_base_url', '', '')
    app.add_config_value('feed_description', '', '')
    app.add_config_value('feed_author', '', '')
    app.add_config_value('feed_filename', 'rss.xml', 'html')

    app.connect('html-page-context', create_feed_item)
    app.connect('build-finished', emit_feed)
    app.connect('builder-inited', create_feed_container)

    #env.process_metadata deletes most of the docinfo, and dates
    #in particular.

def create_feed_container(app):
    feed = Feed()
    feed.feed['title'] = app.config.project
    feed.feed['link'] = app.config.feed_base_url
    feed.feed['author'] = app.config.feed_author
    feed.feed['description'] = app.config.feed_description

    if app.config.language:
        feed.feed['language'] = app.config.language
    if app.config.copyright:
        feed.feed['copyright'] = app.config.copyright
    app.builder.env.feed_feed = feed
    if not hasattr(app.builder.env, 'feed_items'):
        app.builder.env.feed_items = {}

def _parse_pubdate(pubdate):
    try:
        date = time.strptime(pubdate, '%Y-%m-%d %H:%M')
    except ValueError:
        date = time.strptime(pubdate, '%Y-%m-%d')
    return date

def _get_last_updated(app, pagename):
    # Defaulting to None means the item will not go into the feed.
    last_updated = None

    # Look for an explicit publish date in the metadata for the file.
    # Use the metadata syntax in order to specify the publish data:
    #   :Publish Date: 2010-01-01
    metadata = app.builder.env.metadata.get(pagename, {})
    if 'Publish Date' in metadata:
        last_updated = _parse_pubdate(metadata['Publish Date'])
    else:
        # Use the last modified date from git instead of applying a single
        # value to the entire site.
        src_file = app.builder.env.doc2path(pagename)
        if os.path.exists(src_file):
            try:
                last_updated_t = subprocess.check_output(
                    [
                        'git', 'log', '-n1', '--format=%ad', '--date=short',
                        '--', src_file,
                    ]
                ).decode('utf-8').strip()
                last_updated = _parse_pubdate(last_updated_t)
            except (ValueError, subprocess.CalledProcessError) as e:
                pass
    return last_updated

def create_feed_item(app, pagename, templatename, ctx, doctree):
    """ Here we have access to nice HTML fragments to use in, say, an RSS feed.
    """
    env = app.builder.env
    metadata = app.builder.env.metadata.get(pagename, {})

    pubdate = _get_last_updated(app, pagename)

    if not pubdate:
        # This file hasn't been checked in or is being generated from
        # a template rather than a real page. Ignore it.
        return

    item = {
        'title': ctx.get('title'),
        'link': app.config.feed_base_url + '/' + ctx['current_page_name'] + ctx['file_suffix'],
        # FIXME(dhellmann): Need to remove the anchor links in the
        # headers. See tinkerer code for how to do this with pyquery.
        # FIXME(dhellmann): Should also remove the h1 title from the
        # body, since it is the title of the feed item.
        'description': ctx.get('body'),
        'pubDate': pubdate,
    }
    if 'author' in metadata:
        item['author'] = metadata['author']
    env.feed_items[pagename] = item
    #Additionally, we might like to provide our templates with a way to link to the rss output file
    ctx['rss_link'] = app.config.feed_base_url + '/' + app.config.feed_filename

def emit_feed(app, exc):
    ordered_items = app.builder.env.feed_items.values()
    feed = app.builder.env.feed_feed
    ordered_items.sort(
      cmp=lambda x,y: cmp(x['pubDate'],y['pubDate']),
      reverse=True)
    for item in ordered_items:
        feed.items.append(item)

    path = os.path.join(app.builder.outdir,
                        app.config.feed_filename)
    feed.format_rss2_file(path)

    # save the environment
    builder = app.builder
    builder.info(bold('pickling environment... '), nonl=True)
    builder.env.topickle(os.path.join(builder.doctreedir, ENV_PICKLE_FILENAME))
    builder.info('done')

    # global actions
    builder.info(bold('checking consistency... '), nonl=True)
    builder.env.check_consistency()
    builder.info('done')
