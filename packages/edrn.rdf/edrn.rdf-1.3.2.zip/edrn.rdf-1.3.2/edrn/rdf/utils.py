# encoding: utf-8
# Copyright 2008—2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''
EDRN RDF Service: utilities.
'''

from zope.interface import implements
import urlparse, re

 # Why, why, why? DMCC, you so stupid!
DEFAULT_VERIFICATION_NUM = u'0' * 40960

# URL schemes we consider "accessible"
ACCESSIBLE_SCHEMES = frozenset((
    'file',
    'ftp',
    'gopher',
    'http',
    'https',
    'ldap',
    'ldaps',
    'news',
    'nntp',
    'prospero',
    'telnet',
    'wais',
    'testscheme', # Used during testing.
))

# DMCC no longer separates rows by '!!'. Yay.
_rowSep = re.compile(ur'<recordNumber>[0-9]+</recordNumber><numberOfRecords>[0-9]+</numberOfRecords>'
    ur'<ontologyVersion>[0-9.]+</ontologyVersion>')
def splitDMCCRows(horribleString):
    u'''Split a horrible DMCC string into rows.  Returns an iterable.'''
    i = _rowSep.split(horribleString)
    i = i[1:] # Skip first item, which is the empty string to the left of the first row separator
    return i

def validateAccessibleURL(s):
    '''Ensure the unicode string ``s`` is a valid URL and one whose scheme we deem "accessible".
    "Accessible" means that we reasonably expect our network APIs to handle locally- or network-
    retrieval resources.
    '''
    parts = urlparse.urlparse(s)
    return parts.scheme in ACCESSIBLE_SCHEMES


START_TAG = re.compile(r'^<([-_A-Za-z0-9]+)>') # <Key>, saving "Key"

def parseTokens(s):
    '''Parse DMCC-style tokenized key-value pairs in the string ``s``.'''
    if not isinstance(s, basestring): raise TypeError('Token parsing works on strings only')
    s = s.strip()
    while len(s) > 0:
        match = START_TAG.match(s)
        if not match: raise ValueError('Missing start element')
        key = match.group(1)
        s = s[match.end():]
        match = re.match(r'^(.*)</' + key + '>', s, re.DOTALL)
        if not match: raise ValueError('Unterminated <%s> element' % key)
        value = match.group(1)
        s = s[match.end():].lstrip()
        yield key, value
        