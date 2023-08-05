tornado-menumaker
=================

Inspired by tornroutes a simple menu api

Copyright license
=================

tornado-menumaker is licensed under the GNU Affero General Public License, for more information see the LICENSE.txt.

Usage
=====

Define Handler using decorator:

    import tornado.web
    from tornado_menumaker import page, index, subpage, routes

    @page('/news', 'News', icon='icon-news')
    class NewsHandler(tornado.web.RequestHandler):

        @index
        def get(self):
            pass

        @subpage('/show/(\d+)')
        def show(self, id):
            pass

        @subpage('/new', 'Neue News')
        def new(self):
            pass

        @new.post
        def new(self):
            pass

        @subpage('/archive', 'Archiv')
        def archive(self):
            pass

    a = tornado.web.Application(routes())

To get the menu structure you can then use:

    from tornado_menumaker import items

    for level, url, caption, sub_routes, kwargs in items():
       ...
       for level, url, caption, subsub_routes, kwargs in sub_routes:
          ...

    This will yield for the above example:
       0, '/news', 'News', <generator>, {icon: 'icon_news'}
         1, '/news/new', 'Neue News', <generator>, {}
         1, '/news/archive', 'Archiv', <generator>, {}







