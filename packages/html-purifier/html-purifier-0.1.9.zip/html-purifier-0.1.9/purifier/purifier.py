# -*- coding: utf-8 -*-
"""
Based on native Python module HTMLParser purifier of HTML
"""

import logging
try:
    from HTMLParser import HTMLParser
except ImportError:
    from html.parser import HTMLParser


class HTMLPurifier(HTMLParser):
    """
    Cuts the tags and attributes are not in the whitelist. Their content is leaves.
    Signature of whitelist:
    {
        'enabled tag name' : ['list of enabled tag's attributes']
    }
    You can use the symbol '*' to allow all tags and/or attributes 
    """
    
    DEBUG = False
    level = 0
    isNotPurify = False
    removeEntity = False
    unclosedTags = ['br', 'hr']
    isStrictHtml = False
    log = None
        
    def feed(self, data):
        """
        Main method for purifying HTML (overrided)
        """
        self.reset_purified()
        HTMLParser.feed(self, data)
        return self.html()
    
    def reset_purified(self):
        """
        Reset of inner purifying data
        """
        self.data = []
    
    def html(self):
        """
        Current representation of purifying data as unicode
        """
        return u''.join(self.data)
    
    def handle_starttag(self, tag, attrs):
        """
        Handler of starting tag processing (overrided, private)
        """
        self.log.debug( u'Encountered a start tag: {0} {1}'.format(tag, attrs) )
        if tag in self.sanitizelist:
            self.level += 1
            return
        if self.isNotPurify or tag in self.whitelist_keys:
            attrs = self.__attrs_str(tag, attrs)
            attrs = ' ' + attrs if attrs else ''
            tmpl = u'<%s%s />' if tag in self.unclosedTags and self.isStrictHtml else u'<%s%s>'
            self.data.append( tmpl % (tag, attrs,) )
        
    def handle_endtag(self, tag):
        """
        Handler of ending tag processing (overrided, private)
        """
        self.log.debug( u'Encountered an end tag : {0}'.format(tag) )
        if tag in self.sanitizelist:
            self.level -= 1
            return
        if tag in self.unclosedTags:
            return
        if self.isNotPurify or tag in self.whitelist_keys:
            self.data.append(u'</%s>' % tag)
        
    def handle_data(self, data):
        """
        Handler of processing data inside tag (overrided, private)
        """
        self.log.debug( u'Encountered some data  : {0}'.format(data) )
        if not self.level:
            self.data.append(data)
    
    def handle_entityref(self, name):
        """
        Handler of processing entity (overrided, private)
        """
        self.log.debug( u'Encountered entity  : {0}'.format(name) )
        if not self.removeEntity:
            self.data.append('&%s;' % name)
        
    def __init__(self, whitelist=None, remove_entity=False):
        """
        Build white list of tags and their attributes and reset purifying data
        """
        if not self.log:
            self.__set_log()
        self.removeEntity = remove_entity
        HTMLParser.__init__(self)
        self.__set_whitelist(whitelist)
        self.reset_purified()
    
    def __set_whitelist(self, whitelist=None):
        """
        Update default white list by customer white list
        """
        # add tag's names as key and list of enabled attributes as value for defaults
        self.whitelist = {}
        # tags that removed with contents
        self.sanitizelist = ['script', 'style']
        if isinstance(whitelist, dict) and '*' in whitelist.keys():
            self.isNotPurify = True
            self.whitelist_keys = []
            return
        else:
            self.isNotPurify = False
        self.whitelist.update(whitelist or {})
        self.whitelist_keys = self.whitelist.keys()
    
    def __attrs_str(self, tag, attrs):
        """
        Build string of attributes list for tag
        """
        enabled = self.whitelist.get(tag, ['*'])
        all_attrs = '*' in enabled
        items = []
        for attr in attrs:
            key = attr[0]
            value = attr[1] or ''
            if all_attrs or key in enabled:
                items.append( u'%s="%s"' % (key, value,) )
        return u' '.join(items)

    def __set_log(self):
        level = logging.DEBUG if self.DEBUG else logging.INFO
        self.log = logging.getLogger('purifier.HTMLPurifier')
        self.log.setLevel(level)
        handler = logging.StreamHandler()
        handler.setLevel(level)
        self.log.addHandler(handler)
