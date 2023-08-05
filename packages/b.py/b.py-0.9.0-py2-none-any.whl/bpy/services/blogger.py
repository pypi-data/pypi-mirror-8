# Copyright (C) 2013-2014 by Yu-Jie Lin
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

"""
Blogger service recognizes the following options in :ref:`brc.py`:

.. code:: python

  service = 'blogger'
  service_options = {
    'blog': <blog id>,
  }

You can use ``blogs`` command to quickly get the blog ID.


.. _Authorization:

Authorization
=============

You need to authorize *b.py* to access your Blogger account. Simply using
``blogs`` command (see *Commands* section) to start the authorization process:

.. code:: sh

  b.py blogs

Once you follow the prompted steps, there should be a b.dat_ created under the
current working directory, you should keep it safe.


.. _b.dat:

``b.dat``
=========

``b.dat`` is a credential file for Blogger service, it's read by *b.py* from
the current directory.

To create the file, please follow Authorization_.
"""

from __future__ import print_function

import os
import sys

import httplib2

from bpy.services.base import Service as BaseService

if sys.version_info.major == 2:
  from apiclient.discovery import build
  from oauth2client.client import OAuth2WebServerFlow
  from oauth2client.file import Storage as BaseStorage
  from oauth2client.tools import run

  API_STORAGE = 'b.dat'

  class Storage(BaseStorage):
    """Inherit the API Storage to suppress CredentialsFileSymbolicLinkError
    """

    def __init__(self, filename):

      super(Storage, self).__init__(filename)
      self._filename_link_warned = False

    def _validate_file(self):

      if os.path.islink(self._filename) and not self._filename_link_warned:
        print('File: %s is a symbolic link.' % self._filename)
        self._filename_link_warned = True


class Service(BaseService):

  service_name = 'blogger'

  def __init__(self, *args, **kwargs):

    super(Service, self).__init__(*args, **kwargs)

    self.http = None
    self.service = None

  def auth(self):

    if sys.version_info.major != 2:
      msg = ('This command requires google-api-python-client, '
             'which only support Python 2')
      raise RuntimeError(msg)

    if self.http and self.service:
      return

    FLOW = OAuth2WebServerFlow(
      '56045325640.apps.googleusercontent.com',
      'xCzmIv2FUWxeQzA5yJvm4w9U',
      'https://www.googleapis.com/auth/blogger',
      auth_uri='https://accounts.google.com/o/oauth2/auth',
      token_uri='https://accounts.google.com/o/oauth2/token',
    )

    storage = Storage(API_STORAGE)
    credentials = storage.get()
    if credentials is None or credentials.invalid:
      credentials = run(FLOW, storage)

    http = httplib2.Http()
    self.http = credentials.authorize(http)
    self.service = build("blogger", "v3", http=self.http)

  def list_blogs(self):

    self.auth()
    blogs = self.service.blogs()
    req = blogs.listByUser(userId='self')
    resp = req.execute(http=self.http)
    print('%-20s: %s' % ('Blog ID', 'Blog name'))
    for blog in resp['items']:
      print('%-20s: %s' % (blog['id'], blog['name']))

  def post(self):

    handler, post = self.make_handler_post()

    if 'blog' not in post:
      print('You need to specify which blog to post on '
            'in either brc.py or header of %s.' % handler.filename)
      sys.exit(1)

    self.auth()

    kind = post['kind'].replace('blogger#', '')
    title = post['title']

    if kind == 'post':
      posts = self.service.posts()
    elif kind == 'page':
      posts = self.service.pages()
    else:
      raise ValueError('Unsupported kind: %s' % kind)

    data = {
      'blogId': post['blog']['id'],
      'body': post,
    }
    if 'id' in post:
      data['%sId' % kind] = post['id']
      action = 'revert' if post['draft'] else 'publish'
      data[action] = True
      print('Updating a %s: %s' % (kind, title))
      req = posts.update(**data)
    else:
      data['isDraft'] = post['draft']
      print('Posting a new %s: %s' % (kind, title))
      req = posts.insert(**data)

    resp = req.execute(http=self.http)

    resp['draft'] = resp['status'] == 'DRAFT'

    handler.merge_header(resp)
    handler.write()

  def search(self, q):

    if self.options['blog'] is None:
      raise ValueError('no blog ID to search')

    self.auth()

    fields = 'items(labels,published,title,url)'
    posts = self.service.posts()
    req = posts.search(blogId=self.options['blog'], q=q, fields=fields)
    resp = req.execute(http=self.http)
    items = resp.get('items', [])
    print('Found %d posts on Blog %s' % (len(items), self.options['blog']))
    print()
    for post in items:
      print(post['title'])
      labels = post.get('labels', [])
      if labels:
        print('Labels:', ', '.join(labels))
      print('Published:', post['published'])
      print(post['url'])
      print()
