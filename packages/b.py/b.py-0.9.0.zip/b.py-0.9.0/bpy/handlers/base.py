# Copyright (C) 2013, 2014 Yu-Jie Lin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


from __future__ import print_function, unicode_literals

import codecs
import re
import warnings
from abc import ABCMeta, abstractmethod
from base64 import b64encode
from hashlib import md5
from os.path import basename, exists, splitext

HAS_SMARTYPANTS = False
try:
  import smartypants
  HAS_SMARTYPANTS = True
except ImportError:
  pass


class BaseHandler():
  """The base clase of markup handler"""
  __metaclass__ = ABCMeta

  # default handler options
  OPTIONS = {
    'markup_prefix': '',
    'markup_suffix': '',
    'smartypants': False,
    'id_affix': None,
  }

  MERGE_HEADERS = ('service', 'kind', 'blog', 'id', 'url', 'draft')
  HEADER_FMT = '%s: %s'
  PREFIX_HEAD = ''
  PREFIX_END = ''

  RE_SPLIT = re.compile(r'^(?:([^\n]*?!b.*?)\n\n)?(.*)',
                        re.DOTALL | re.MULTILINE)
  RE_HEADER = re.compile(r'.*?([a-zA-Z0-9_-]+)\s*[=:]\s*(.*)\s*')

  SUPPORT_EMBED_IMAGES = True
  RE_IMG = re.compile(
    r'''
    (?P<prefix><img.*?)
    src="(?!data:image/|https?://)(?P<src>[^"]*)"
    (?P<suffix>.*?>)
    ''',
    re.VERBOSE
  )

  def __init__(self, filename, options=None):

    self.filename = filename
    self.title = ''
    self.options = self.OPTIONS.copy()
    self.options.update(options or {})
    if filename:
      with codecs.open(filename, 'r', 'utf8') as f:
        self.source = f.read()
      header, markup = self.split_header_markup()
      self.title = splitext(basename(filename))[0]
    else:
      header = {}
      markup = ''
    self.header = header
    self.markup = markup
    self.modified = False

  def set_header(self, k, v):
    """Set header

    >>> class Handler(BaseHandler):
    ...   def _generate(self, source=None): return source
    >>> handler = Handler(None)
    >>> print(handler.header)
    {}
    >>> handler.modified
    False
    >>> handler.set_header('foo', 'bar')
    >>> print(handler.header['foo'])
    bar
    >>> handler.modified
    True
    """
    if k in self.header and self.header[k] == v:
      return

    self.header[k] = v
    self.modified = True

  def merge_header(self, header):
    """Merge header

    >>> class Handler(BaseHandler):
    ...   def _generate(self, source=None): return source
    >>> handler = Handler(None)
    >>> handler.merge_header({'id': 12345, 'bogus': 'blah'})
    >>> print(handler.header['id'])
    12345
    >>> handler.modified
    True
    """
    for k, v in header.items():
      if k not in self.MERGE_HEADERS:
        continue
      if k == 'blog':
        v = v['id']
      elif k == 'kind':
        v = v.replace('blogger#', '')
      self.set_header(k, v)

  @property
  def markup(self):
    """Return markup with markup_prefix and markup_suffix

    >>> class Handler(BaseHandler):
    ...   def _generate(self, source=None): return source
    >>> options = {
    ...   'markup_prefix': 'the prefix\\n',
    ...   'markup_suffix': '\\nthe suffix',
    ...   }
    >>> handler = Handler(None, options)
    >>> handler.markup = 'content'
    >>> print(handler.markup)
    the prefix
    content
    the suffix
    """
    return '%s%s%s' % (
      self.options['markup_prefix'],
      self._markup,
      self.options['markup_suffix'],
    )

  @markup.setter
  def markup(self, markup):
    """Set the markup"""
    self._markup = markup

  @property
  def id_affix(self):
    """Return id_affix

    The initial value is from self.options, and can be overriden by
    self.header.

    Returns

    * None if it's None.
    * value if value is not ''
    * first 4 digits of md5 of value if value is '', and assign back to
      self.options. _generate method of Handler should write back to
      self.header.

    >>> class Handler(BaseHandler):
    ...   def _generate(self, source=None): return source
    >>> options = {
    ...   'id_affix': None,
    ...   }
    >>> handler = Handler(None, options)
    >>> print(repr(handler.id_affix))
    None
    >>> handler.options['id_affix'] = 'foobar'
    >>> print(handler.id_affix)
    foobar
    >>> # auto generate an id affix from title
    >>> handler.options['id_affix'] = ''
    >>> handler.title = 'abc'
    >>> print(handler.id_affix)
    9001
    >>> handler.header['id_affix'] = 'override-affix'
    >>> print(handler.id_affix)
    override-affix
    """
    id_affix = self.options['id_affix']
    # override?
    if 'id_affix' in self.header:
      id_affix = self.header['id_affix']
      if self.header['id_affix'] and id_affix != 'None':
        return self.header['id_affix']

    # second case is from header of post, has to use string 'None'
    if id_affix is None or id_affix == 'None':
      return None

    if id_affix:
      return id_affix

    m = md5()
    m.update(self.title.encode('utf8'))
    return m.hexdigest()[:4]

  @abstractmethod
  def _generate(self, markup=None):
    """Generate HTML of markup source"""
    raise NotImplementedError

  def generate(self, markup=None):
    """Generate HTML

    >>> class Handler(BaseHandler):
    ...   def _generate(self, markup=None): return markup
    >>> handler = Handler(None)
    >>> print(handler.generate('foo "bar"'))
    foo "bar"
    >>> handler.options['smartypants'] = True
    >>> print(handler.generate('foo "bar"'))
    foo &#8220;bar&#8221;
    """

    if markup is None:
      markup = self.markup

    html = self._generate(markup)

    if self.options.get('smartypants', False):
      if not HAS_SMARTYPANTS:
        warnings.warn("smartypants option is set, "
                      "but the library isn't installed.", RuntimeWarning)
        return html
      Attr = smartypants.Attr
      html = smartypants.smartypants(html, Attr.set1 | Attr.w)

    if self.SUPPORT_EMBED_IMAGES and self.options.get('embed_images', False):
      html = self.embed_images(html)

    return html

  def generate_header(self, header=None):
    """Generate header in text for writing back to the file

    >>> class Handler(BaseHandler):
    ...   PREFIX_HEAD = 'foo '
    ...   PREFIX_END = 'bar'
    ...   HEADER_FMT = '--- %s: %s'
    ...   def _generate(self, source=None): pass
    >>> handler = Handler(None)
    >>> print(handler.generate_header({'title': 'foobar'}))
    foo !b
    --- title: foobar
    bar
    <BLANKLINE>
    >>> print(handler.generate_header({'labels': ['foo', 'bar']}))
    foo !b
    --- labels: foo, bar
    bar
    <BLANKLINE>
    """
    if header is None:
      header = self.header

    lines = [self.PREFIX_HEAD + '!b']
    for k, v in header.items():
      if k in ('labels', 'categories'):
        v = ', '.join(v)
      elif k == 'draft':
        v = repr(v)
      lines.append(self.HEADER_FMT % (k, v))
    lines.append(self.PREFIX_END)
    return '\n'.join([_f for _f in lines if _f]) + '\n'

  def generate_title(self, title=None):
    """Generate title for posting

    >>> class Handler(BaseHandler):
    ...   def _generate(self, source=None): return source
    >>> handler = Handler(None)
    >>> print(handler.generate_title('foo "bar"'))
    foo "bar"
    >>> print(handler.generate_title('foo\\nbar\\n\\n'))
    foo bar
    >>> handler.options['smartypants'] = True
    >>> print(handler.generate_title('foo "bar"'))
    foo &#8220;bar&#8221;
    """
    if title is None:
      title = self.header.get('title', self.title)

    title = self.generate(title)
    title = title.replace('<p>', '').replace('</p>', '')
    # no trailing newlines
    title = re.sub(r'\n+', ' ', title).rstrip()
    return title

  def generate_post(self):
    """Generate dict for merging to post object of API"""
    post = {'title': self.generate_title(), 'draft': False}
    for k in ('blog', 'id', 'labels', 'categories', 'draft'):
      if k not in self.header:
        continue
      if k == 'blog':
        post[k] = {'id': self.header[k]}
      else:
        post[k] = self.header[k]
    return post

  def split_header_markup(self, source=None):
    """Split source into header and markup parts

    It also parses header into a dict."""
    if source is None:
      source = self.source

    header, markup = self.RE_SPLIT.match(source).groups()

    _header = {}
    if header:
      for item in header.split('\n'):
        m = self.RE_HEADER.match(item)
        if not m:
          continue
        k, v = list(map(type('').strip, m.groups()))
        if k in ('labels', 'categories'):
          v = [_f for _f in [label.strip() for label in v.split(',')] if _f]
        elif k == 'draft':
          v = v.lower() in ('true', 'yes', '1')
        _header[k] = v
    header = _header

    return header, markup

  def update_source(self, header=None, markup=None, only_returned=False):

    if header is None:
      header = self.header
    if markup is None:
      markup = self._markup

    source = self.generate_header(header) + '\n' + markup
    if not only_returned:
      self.source = source
    return source

  def write(self, forced=False):
    """Write source back to file"""
    if not self.modified:
      if not forced:
        return
    else:
      self.update_source()

    with codecs.open(self.filename, 'w', 'utf8') as f:
      f.write(self.source)
    self.modified = False

  def embed_images(self, html):
    """Embed images on local filesystem as data URI

    >>> class Handler(BaseHandler):
    ...   def _generate(self, source=None): return source
    >>> handler = Handler(None)
    >>> html = '<img src="http://example.com/example.png"/>'
    >>> print(handler.embed_images(html))
    <img src="http://example.com/example.png"/>
    >>> html = '<img src="tests/test.png"/>'
    >>> print(handler.embed_images(html))  #doctest: +ELLIPSIS
    <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAAB...QmCC"/>
    """
    if not self.SUPPORT_EMBED_IMAGES:
      raise RuntimeError('%r does not support embed_images' % type(self))

    return self.RE_IMG.sub(self._embed_image, html)

  @staticmethod
  def _embed_image(match):

    src = match.group('src')
    if not exists(src):
      print('%s is not found.' % src)
      return match.group(0)

    with open(src, 'rb') as f:
      data = b64encode(f.read()).decode('ascii')

    return '%ssrc="%s"%s' % (
      match.group('prefix'),
      'data:image/%s;base64,%s' % (splitext(src)[1].lstrip('.'), data),
      match.group('suffix'),
    )
