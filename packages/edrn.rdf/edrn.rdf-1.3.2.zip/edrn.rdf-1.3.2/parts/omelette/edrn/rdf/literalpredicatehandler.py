# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from five import grok
from interfaces import IAsserter
from predicatehandler import ISimplePredicateHandler
from Acquisition import aq_inner
import rdflib

class ILiteralPredicateHandler(ISimplePredicateHandler):
    '''A handler for DMCC web services that maps tokenized keys to literal RDF values.'''
    # No further fields are necessary.

class LiteralAsserter(grok.Adapter):
    '''Describes subjects using predicates with literal complementary objects.'''
    grok.context(ILiteralPredicateHandler)
    grok.provides(IAsserter)
    def characterize(self, obj):
        context = aq_inner(self.context)
        return [(rdflib.URIRef(context.predicateURI), rdflib.Literal(obj))]

    
