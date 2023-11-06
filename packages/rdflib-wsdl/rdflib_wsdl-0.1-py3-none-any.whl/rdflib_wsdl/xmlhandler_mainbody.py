from typing import Optional, Tuple
from collections.abc import Mapping
import xml.sax
import xml.sax.handler
from .xmlhandler import _start, _state, name2qname, extract_namespaces
from .wsdl2rdf import generateRDF

class WSDLXMLHandler(xml.sax.handler.ContentHandler):
    startingstate: type[_state] = _start
    locator: Optional
    def __init__(self, store):
        self.store = store
        self.preserve_bnode_ids = False
        self.reset()
        self.states = []

    def _get_currentState(self):
        return self.states[-1]

    def _set_currentState(self, newstate):
        if newstate not in self.states:
            self.states.append(newstate)
        elif self.states[-2] == newstate:
            self.states.pop()
        else:
            raise Exception("Cant set state only to an old state, if that "
                            "state is the previous state.")

    currentState = property(fset=_set_currentState, fget=_get_currentState)

    def reset(self):
        pass

    def setDocumentLocator(self, locator):
        self.locator = locator

    def startDocument(self):
        self.currentState = self.startingstate()
        
    def parse(self, *args):
        raise Exception()

    #def feed(self, buffer):
    #    raise Exception(buffer)
    #    super().feed()

    def endDocument(self):
        """
        :TODO: Change endstate.close to return the graph.
        """
        assert isinstance(self.currentState, _start)
        #cant close basestate so use finalize instead of close
        for ax in generateRDF(self.currentState.first_state):
            self.store.add(ax)
        #endinfograph = self.currentState.finalize()
        #for ax in endinfograph:
        #    self.store.add(ax)

    def startElement(self, name, attrs):
        other_attrs, namespaces, defaultNS = extract_namespaces(attrs._attrs)
        namespaces = {**self.currentState.namespaces, **namespaces}
        if defaultNS == None:
            defaultNS = self.currentState.default_namespace
        qname = name2qname(name, defaultNS, namespaces)
        self.currentState = self.currentState.transition(qname, attrs,
                                                         namespaces, defaultNS)

    def endElement(self, name):
        self.currentState.close()
        self.states.pop()

    def startElementNS(self, name, qname, attrs):
        """Cant implement this with feature Namespaces enabled because
        i need access to namespaces within binding.
        """
        raise NotImplementedError()

    def endElementNS(self, name, qname):
        raise NotImplementedError()

    def characters(self, content):
        self.currentState.add_characters(content)

    def ignorableWhitespace(self, content):
        pass
