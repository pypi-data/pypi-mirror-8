# -*- coding: utf-8 -*-
"""
Message parser
"""
import re

POST_CLEANER_TAG_RE = '<(?P<tag>/?(?:b|i|s|u|tt|m|code))>'
POST_CLEANER_SCHEME_RE = '(?P<scheme>(?:http|ftp|https|chrome|gopher|git|git+ssh|svn|svn+ssh)://)'
POST_CLEANER_CLOCK_RE = u'(?<![0-9])(?P<clock>(?P<h>2[0-3]|[01][0-9])(?P<c>(?=[0-5][0-9][:0-9])|:)(?P<m>[0-5][0-9])(?:(?P=c)(?P<s>[0-5][0-9])(?:(?P<sel>[¹²³⁴⁵⁶⁷⁸⁹][⁰¹²³⁴⁵⁶⁷⁸⁹]?|[\^:][1-9][0-9]?))?)?)(?![0-9:@])'
POST_CLEANER_TOTOZ_RE = '(?P<totoz>\[\:[A-Za-z0-9-_ ]+\])'
POST_CLEANER_RE = re.compile('(' + POST_CLEANER_TOTOZ_RE + '|(?P<sep>[\(\)\[\]"])|' + POST_CLEANER_TAG_RE + '|' + POST_CLEANER_SCHEME_RE + '|' + POST_CLEANER_CLOCK_RE + ')')
POST_CLEANER_SEP_END = { '(': ')', '[': ']', '"': '"' }

# TODO: à migrer dans le settings "local" and use re.compile
URL_SUBSTITUTION = (
    (r".tar.gz", "tgz"),
    (r".tgz", "tgz"),
    (r".(zip|rpm|deb|tgz)$", r"\1"),
    (r".pdf", "pdf"),
    (r"http://localhost", "localhost"),
    (r"wikipedia.org/wiki/(.*)", r"\1@wikipedia"),
    (r"youtube.com", "youtube"),
    (r"dailymotion.com", "dailymotion"),
    (r"bashfr.org", "bashfr"),
    (r"imdb.com", "imdb"),
    (r"google.", "google"),
    (r"yahoo.", "yahoo"),
    (r"lemonde.fr", "lemonde"),
    (r"liberation.fr", "libe"),
    (r"lefigaro.fr", "lefigaro"),
    (r"journaldunet.", "jdn"),
    (r"01net.com", "01net"),
    (r"forum.hardware", "hfr"),
    (r"linuxfr.org", "Dlfp"),
    (r"goatse", "pas cliquer!"),
    (r"goat.cx", "pas cliquer!"),
    (r"glazman.org", "yerk pas cliquer!"),
    (r".ssz.fr", "pas cliquer non plus!"),
    (r"wiki", "wiki"),
    (r"wickedweasel", "WW"),
    (r"slashdot.org", "/."),
    (r"osnews.com", "osnews"),
    (r"zdnet.", "zdnet"),
    (r"ruby", "ruby"),
    (r"/goomi/unspeakable", "Fhtagn!"),
    (r"http://(.*).free.fr", r"\1@free"),
)

def XmlEntities(s):
    """
    TODO: utiliser les entités ``&XX;`` ou alors uniformiser sur la notation en hexa (
    mais les parser xml ont tendance à tous utiliser les entités ``&XX;``)
    """
    return s.replace('&', '&#38;').replace('<', '&#60;').replace('>', '&#62;').replace('"', '&#34;')

def PostMatchIterator(str):
    lastIndex = 0
    for match in re.finditer(POST_CLEANER_RE, str):
        if match.start() > lastIndex:
            yield ['txt', str[lastIndex:match.start()]]
        for category in ['sep', 'tag', 'scheme', 'clock', 'totoz']:
            if match.group(category):
                yield [category, match]
                break
        lastIndex = match.end()
    if len(str) > lastIndex:
        yield ['txt', str[lastIndex:]]

def ListPopIterator(list):
    while True:
        try:
            yield list.pop()
        except: break

class GenericPostCleaner(list):
    """
    G.I.P. 2 : "Glandium inspired parser" strikes back

    Original code is avalaible by GIT at : 
    git://git.glandium.org/bouchot-ng.git

    Original credits to :
    Mike Hommey mh AT glandium DOT org
    """
    def __init__(self):
        self._tags = []
        super(GenericPostCleaner, self).__init__()

    def pop_or_append(self, pop, append):
        if len(self) > 0 and self[len(self) - 1] == pop:
             self.pop()
        else:
             self.append(append)

    def append_tag(self, tag):
        """tag is given without <>"""
        if tag[0] == '/':
            if tag[1:] in self._tags:
                for t in ListPopIterator(self._tags):
                    self.pop_or_append('<%s>' % t, '</%s>' % t)
                    if t == tag[1:]:
                        break
        else:
            self._tags.append(tag)
            self.pop_or_append('</%s>' % tag, '<%s>' % tag)

    def append_escape(self, str):
        raise NotImplementedError

    def append_url(self, scheme, url):
        """scheme includes ://"""
        raise NotImplementedError

    def append_totoz(self, totoz):
        """totoz contains enclosing [: ]"""
        raise NotImplementedError

    def append_clock(self, format, h, m, s, sel):
        raise NotImplementedError

    def __str__(self):
        return ''.join(self)

    def __iter__(self):
        for t in ListPopIterator(self._tags):
            self.pop_or_append('<%s>' % t, '</%s>' % t)
        return super(GenericPostCleaner, self).__iter__()

    def append_batch(self, str):
        lastSep = ''
        code = 0
        iterator = iter(PostMatchIterator(str))
        for type, match in iterator:
            if type == 'txt':
                self.append_escape(match)
            elif code:
                if type == 'tag' and match.group('tag') == '/code':
                     self.append_tag(match.group('tag'))
                     code = 0
                else:
                    self.append_escape(match.group(0))
            elif type == 'sep':
                sep = match.group('sep')
                if sep in ['(', '[', '"']:
                    lastSep = sep
                self.append(sep)
            elif type == 'tag':
                if match.group('tag') == 'code':
                    code = 1
                self.append_tag(match.group('tag'))
            elif type == 'scheme':
                scheme = match.group('scheme')
                url = ''
                i = -1
                if lastSep:
                    end = POST_CLEANER_SEP_END[lastSep]
                else:
                    end = ' '
                url += scheme
                for type, match in iterator:
                    if type == 'tag' or (type == 'sep' and match.group('sep') == end):
                        break
                    if type == 'txt':
                        try:
                            i = match.index(' ')
                            url += match[:i]
                            break
                        except:
                            url += match
                    else:
                        url += match.group(0)
                self.append_url(scheme, url)
                if i != -1:
                    self.append_escape(match[i:])
                #if type == 'sep':
                if type == 'sep' and match.group('sep') == end:
                    self.append(match.group('sep'))
                elif type == 'tag':
                    self.append_tag(match.group('tag'))
            elif type == 'clock':
                if not match.group('s'):
                    format = '%H:%M'
                elif match.group('c'):
                    format = '%H:%M:%S'
                else:
                    format = '%H%M%S'
                self.append_clock(format, int(match.group('h')), int(match.group('m')),
                                                 int(match.group('s')) if match.group('s') else None, match.group('sel'))
            elif type == 'totoz':
                self.append_totoz(match.group('totoz'))

class PostCleaner(GenericPostCleaner):
    """
    ``GenericPostCleaner`` extension to implement needed methods and tribune behavior
    """
    def __init__(self, link_rel_escape):
        super(PostCleaner, self).__init__()
        self.matched_totozs = []
        self.matched_clocks = []
        self.matched_urls = []
        self.link_rel_escape = link_rel_escape

    def append_escape(self, s):
        self.append(XmlEntities(s))

    def append_url(self, scheme, url): # scheme includes ://
        self.append('<a href="')
        self.append_escape(url)
        self.append('"%s>' % self.link_rel_escape)
        self.append( self.link_formatter(scheme[0:-3], url) )
        self.append('</a>')
        self.matched_urls.append(url)

    def append_totoz(self, totoz): # totoz contains enclosing [: ]
        self.append('<totoz name="%s"/>' % totoz[2:])
        self.matched_totozs.append(totoz[2:])

    def append_clock(self, format, h, m, s, sel):
        time = ('%02d:%02d' if format[2] == ':' else '%02d%02d') % (h, m)
        if s != None:
            time += (':%02d' if format[2] == ':' else '%02d') % s
        if not sel:
            sel = ''
        self.append('<clock time="%s">' % (time.replace(':','')))
        self.append(time + sel)
        self.append('</clock>')
        self.matched_clocks.append(time + sel)

    def link_formatter(self, scheme, url):
        """
        Parse l'url pour en déterminer le titre
        """
        # Label par défaut des urls
        title = scheme
        if title == 'http':
            title = 'url'
        
        # Renommage du label du lien selon son url
        for k,v in URL_SUBSTITUTION:
            matched = re.search(k, url)
            # On a trouvé un motif de label
            if matched:
                # Motif avec substitution dynamique
                if len(matched.groups(0))>0:
                    title = matched.expand(v)
                # Motif avec substitution simple
                else:
                    title = v
                break
        
        return "[%s]" % title
