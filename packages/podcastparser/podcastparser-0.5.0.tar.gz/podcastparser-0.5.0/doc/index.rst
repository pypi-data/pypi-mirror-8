.. podcastparser documentation master file, created by
   sphinx-quickstart on Sat Apr 13 11:48:00 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

podcastparser
=============

*podcastparser* is a simple and fast podcast feed parser library in Python.
The two primary users of the library are the `gPodder Podcast Client`_ and
the `gpodder.net web service`_.

The following feed types are supported:

* Really Simple Syndication (`RSS 2.0`_)
* Atom Syndication Format (`RFC 4287`_)

The following specifications are supported:

* `Paged Feeds`_ (`RFC 5005`_)
* `Podlove Simple Chapters`_

These formats only specify the possible markup elements and attributes. We
recommend that you also read the `Podcast Feed Best Practice`_ guide if you
want to optimize your feeds for best display in podcast clients.

Where times and durations are used, the values are expected to be formatted
either as seconds or as `RFC 2326`_ Normal Play Time (NPT).

.. _gPodder Podcast Client: http://gpodder.org/
.. _gpodder.net web service: http://gpodder.net/
.. _RSS 2.0: http://www.rssboard.org/rss-specification
.. _RFC 4287: https://tools.ietf.org/html/rfc4287
.. _Podcast Feed Best Practice: https://github.com/gpodder/podcast-feed-best-practice/blob/master/podcast-feed-best-practice.md
.. _Paged Feeds: http://podlove.org/paged-feeds/
.. _RFC 5005: https://tools.ietf.org/html/rfc5005
.. _RFC 2326: https://tools.ietf.org/html/rfc2326
.. _Podlove Simple Chapters: http://podlove.org/simple-chapters/

Example
=======

.. code-block:: python

    import podcastparser
    import urllib

    feedurl = 'http://example.com/feed.xml'

    parsed = podcastparser.parse(feedurl, urllib.urlopen(feedurl))

    # parsed is a dict
    import pprint
    pprint.pprint(parsed)

.. TODO: Show example dict for a parsed feed with all fields

Supported XML Elements and Attributes
=====================================

For both RSS and Atom feeds, only a subset of elements (those that are relevant
to podcast client applications) is parsed. This section describes which elements
and attributes are parsed and how the contents are interpreted/used.

RSS
---

**rss@xml:base**
    Base URL for all relative links in the RSS file.

**rss/channel**
    Podcast.

**rss/channel/title**
    Podcast title (whitespace is squashed).

**rss/channel/link**
    Podcast website.

**rss/channel/description**
    Podcast description (whitespace is squashed).

**rss/channel/image/url**
    Podcast cover art.

**rss/channel/itunes:image**
    Podcast cover art (alternative).

**rss/channel/atom:link@rel=payment**
    Podcast payment URL (e.g. Flattr).

**rss/channel/item**
    Episode.

**rss/channel/item/guid**
    Episode unique identifier (GUID), mandatory.

**rss/channel/item/title**
    Episode title (whitespace is squashed).

**rss/channel/item/link**
    Episode website.

**rss/channel/item/description**
    Episode description (whitespace is squashed).

**rss/channel/item/itunes:subtitle**
    Episode subtitled / one-line description (whitespace is squashed).

**rss/channel/item/content:encoded**
    Episode description in HTML.

**rss/channel/item/itunes:duration**
    Episode duration.

**rss/channel/item/pubDate**
    Episode publication date.

**rss/channel/item/atom:link@rel=payment**
    Episode payment URL (e.g. Flattr).

**rss/channel/item/atom:link@rel=enclosure**
    File download URL (@href), size (@length) and mime type (@type).

**rss/channel/item/media:content**
    File download URL (@url), size (@fileSize) and mime type (@type).

**rss/channel/item/enclosure**
    File download URL (@url), size (@length) and mime type (@type).

**rss/channel/item/psc:chapters**
    Podlove Simple Chapters, version 1.1 and 1.2.

**rss/channel/item/psc:chapters/psc:chapter**
    Chapter entry (@start, @title, @href and @image).


Atom
----

For Atom feeds, *podcastparser* will handle the following elements and
attributes:

**atom:feed**
    Podcast.

**atom:feed/atom:title**
    Podcast title (whitespace is squashed).

**atom:feed/atom:subtitle**
    Podcast description (whitespace is squashed).

**atom:feed/atom:icon**
    Podcast cover art.

**atom:feed/atom:link@href**
    Podcast website.

**atom:feed/atom:entry**
    Episode.

**atom:feed/atom:entry/atom:id**
    Episode unique identifier (GUID), mandatory.

**atom:feed/atom:entry/atom:title**
    Episode title (whitespace is squashed).

**atom:feed/atom:entry/atom:link@rel=enclosure**
    File download URL (@href), size (@length) and mime type (@type).

**atom:feed/atom:entry/atom:link@rel=(self|alternate)**
    Episode website.

**atom:feed/atom:entry/atom:link@rel=payment**
    Episode payment URL (e.g. Flattr).

**atom:feed/atom:entry/atom:content**
    Episode description (in HTML or plaintext).

**atom:feed/atom:entry/atom:published**
    Episode publication date.

**atom:feed/atom:entry/psc:chapters**
    Podlove Simple Chapters, version 1.1 and 1.2.

**atom:feed/atom:entry/psc:chapters/psc:chapter**
    Chapter entry (@start, @title, @href and @image).

The ``podcastparser`` module
============================

.. automodule:: podcastparser
   :members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

