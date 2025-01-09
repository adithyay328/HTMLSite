"""
This module contains common snippets,
like links to favicons, canonical
URLs, etc. These are pretty
specific to my website.

To allow these to change
over time, but not break
old pages, use version
numbers at the start
like V1
"""
from adihtml.core import *

def V1_headPreamble():
  """
  On basically every page
  on the site, we need the
  core stylesheet, icons,
  and a canonical url for
  indexing.

  :return: A string that can
    be inserted into Head
  """

  return "".join([
    Link(rel="stylesheet", href="/styles.css"),
    Link(rel="apple-touch-icon", sizes="180x180", href="/apple-touch-icon.png"),
    Link(rel="icon", type="image/png", sizes="32x32", href="/favicon-32x32.png"),
    Link(rel="icon", type="image/png", sizes="16x16", href="/favicon-16x16.png"),
    Link(rel="manifest", href="/site.webmanifest"),
    Meta(name="msapplication-TileColor", content="#da532c"),
    Meta(name="theme-color", content="#ffffff"),
    Link(rel="canonical", href="https://adiy.io/")])
