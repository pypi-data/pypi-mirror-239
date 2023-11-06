#from urllib.parse import urldefrag, urljoin
#import urllib.parse
from collections.abc import Mapping
import abc
import typing as typ
from typing import Optional, Union, Iterable, Tuple, Callable, Any
from collections.abc import MutableMapping, Mapping

from rdflib import Graph, Namespace, RDF, URIRef, RDFS, Literal, BNode, IdentifiedNode
import rdflib

import logging
logger = logging.getLogger(__name__)

from xml.etree import ElementTree as ET
from urllib.parse import urlparse, urlunparse
from . import extensions

from .shared import _ns_wsdl, _ns_wsdlx, _ns_wsdlrdf, _ns_wsoap, _ns_whttp, _ns_wrpc, _ns_sawsdl, _ns_xs, WHTTP, WSDL, WSDLX, WSDL_RDF, WSOAP, SAWSDL
from .shared import name2qname, extract_namespaces, qname2rdfframes

from .wsdl_components import Binding, BindingFaultReference, BindingMessageReference, BindingOperation, Description, ElementDeclaration, Endpoint, Interface, InterfaceFault, InterfaceFaultReference, InterfaceMessageReference, InterfaceOperation, Service, TypeDefinition, Extension, BindingFault, MCM_ANY, MCM_NONE, MCM_OTHER, MCM_ELEMENT

#missing elementdeclaration, Extension

class UnexpectedNodetype(KeyError):
    """Is raised if an unexpected nodename is found in xmlfile"""



class _createnode_mixin:
    """This class specifies how transition between different levels
    are coordinated
    """
    _special_states: Mapping[str, type["_state_with_axioms"]]
    _default_state: Optional[type["_state"]] = None
    def transition(self, trans: Tuple[str, str],
                   attrs: typ.Mapping,
                   namespaces: Mapping[str, str],
                   default_namespace: str,
                   ) -> "_createnode_mixin":
        """
        :param trans: This is the name of the xml-element
        :raises: BadSyntax
        """
        #kwargs = {"parentnode":self, "attrs":attrs, "typeof":trans}
        state_gen = self._special_states.get(trans, self._default_state)
        if state_gen is None:
            raise Exception(self._default_state, self._special_states, trans, type(self))
            raise UnexpectedNodetype(trans, type(self), self._special_states)
        #if trans not in _RIF:
        #    raise BadSyntax("Found for Rif unsupported predicate %s" % trans)
        nextstate = state_gen(trans, parentnode=self, attrs=attrs,
                              namespaces=namespaces,
                              default_namespace=default_namespace,
                              )
        return nextstate


class _state(abc.ABC):
    """This class determines how the xmlhandler will interact with the current
    state.
    """
    axioms: Graph
    _buffer: list
    namespace_base: str
    namespaces: Mapping[str, str]
    default_namespace: Optional[str]
    def __init__(self, trans: Tuple[str, str],
                 parentnode: Union["_start", "_state"],
                 attrs: Mapping,
                 namespaces: Mapping[str, str] = {},
                 default_namespace: Optional[str] = None,
                 ) -> None:
        self._buffer = []
        self.parentnode = parentnode
        self.namespaces = {**self.parentnode.namespaces, **namespaces}
        if default_namespace is not None:
            self.default_namespace = default_namespace
        else:
            self.default_namespace = self.parentnode.default_namespace 
        self.attrs = {}
        for key, x in attrs.items():
            self.attrs[(None, key)] = x
            try:
                _q = name2qname(key, self.default_namespace, self.namespaces)
            except KeyError:
                pass
            else:
                self.attrs[_q] = x

    @property
    def content(self):
        """Returns all current plain text content"""
        return "".join(self._buffer)

    def add_characters(self, content):
        """Adds characters to the current plain text content"""
        self._buffer.append(content)

    @abc.abstractmethod
    def close(self) -> Optional["_state"]: ...

class _to_ElementTree(_createnode_mixin, _state):
    """This is used when an extension is used within the wsdl file.
    Extensions can be decievered via external mappings and are
    ignored if non is found.
    """
    element: ET.Element
    _special_states = {}
    #_default_state = self
    def __init__(self, trans: str,
                 parentnode: Union[_state, "_start", "_to_ElementTree"],
                 attrs: Mapping,
                 namespaces: Mapping[str, str] = {},
                 default_namespace: Optional[str] = None,
                 ) -> None:
        super().__init__(trans, parentnode, attrs,
                         namespaces, default_namespace)
        self.namespace_base = self.attrs.get("xmlns",
                                             self.parentnode.namespace_base)
        element_name = "{%s}%s" % trans
        if isinstance(self.parentnode, _to_ElementTree):
            self.element = ET.SubElement(self.parentnode.element, element_name)
        else:
            self.element = ET.Element(element_name)
        self.element.attrib.update(self.attrs)

    def close(self):
        """
        :TODO: Here external mappings should be called and tried to map given
            xml file
        """
        self.element.text = self.content
        return self.parentnode
_to_ElementTree._default_state = _to_ElementTree


class _start(_createnode_mixin, _state):
    """Startstate"""
    default_namespace = None
    namespaces = {}
    first_state: Optional["_wsdl_element"]
    def __init__(self) -> None:
        self.first_state = None
        self.axioms = rdflib.Graph()
        self._buffer = []
        self.namespace_base = "http://schemas.xmlsoap.org/wsdl/"

    def finalize(self):
        return self.axioms

    def transition(self, trans: Tuple[str, str],
                   attrs: typ.Mapping,
                   namespaces: Mapping[str, str],
                   default_namespace: str,
                   ) -> "_wsdl_element":
        nextstate = super().transition(trans, attrs, namespaces, default_namespace)
        self.first_state = nextstate
        return nextstate

    def close(self) -> None:
        raise Exception("base state can be closed")
        return self


class _state_with_axioms(_createnode_mixin, _state):
    """
    :TODO: change append_axiom because this doesnt work with how 
        properties of class 2 work.
    """
    parentnode: _state
    attrs: Mapping[Tuple[str, str], str]
    namespaces: Mapping[str, str]
    default_namespace: Optional[str]
    def __init__(self, trans, parentnode: _state, attrs: Mapping[str, str],
                 namespaces: Mapping[str, str] = {},
                 default_namespace: Optional[str] = None,
                 ):
        self.parentnode = parentnode
        self.axioms = rdflib.Graph()
        self._buffer = []
        self.namespaces = {**self.parentnode.namespaces, **namespaces}
        if default_namespace is not None:
            self.default_namespace = default_namespace
        else:
            self.default_namespace = self.parentnode.default_namespace 
        self.attrs = {}
        for key, x in attrs.items():
            self.attrs[(None, key)] = x
            try:
                _q = name2qname(key, self.default_namespace, self.namespaces)
            except KeyError:
                pass
            else:
                self.attrs[_q] = x
        try:
            self.namespace_base\
                    = self.attrs['http://www.w3.org/XML/1998/namespace',
                                 'base']
        except KeyError:
            self.namespace_base = parentnode.namespace_base

    def get_targetNamespace(self) -> str:
        return self.attrs.get((None, "targetNamespace"),
                              self.parentnode.get_targetNamespace)

    def close(self) -> None:
        for ax in self.axioms:
            self.parentnode.axioms.add(ax)

class _wsdl_element(_state_with_axioms):
    targetNamespace: str
    child_nodes: Iterable["_wsdl_element"]
    """Register child nodes"""
    def __init__(self, trans: str, parentnode: Union["_start", "_state"],
                 attrs: Mapping,
                 namespaces: Mapping[str, str] = {},
                 default_namespace: Optional[str] = None,
                 ) -> None:
        super().__init__(trans, parentnode, attrs,
                         namespaces, default_namespace)
        self.child_nodes = []

    @property
    def parent(self):
        return self.parentnode

    def transition(self, trans: Tuple[str, str],
                   attrs: typ.Mapping,
                   namespaces: Mapping[str, str],
                   default_namespace: str,
                   ) -> "_wsdl_element":
        next_element = super().transition(trans, attrs, namespaces,
                                          default_namespace)
        self.child_nodes.append(next_element)
        return next_element


class _wsdl_idelement(_wsdl_element):
    def __init__(self, trans: str, parentnode: Union["_start", "_state"],
                 attrs: Mapping,
                 namespaces: Mapping[str, str] = {},
                 default_namespace: Optional[str] = None,
                 ) -> None:
        super().__init__(trans, parentnode, attrs,
                         namespaces, default_namespace)
        myid = self.wsdlIRIReference
        for prop, obj in self._additional_frames():
            self.axioms.add((myid, prop, obj))

    def _additional_frames(self) -> Iterable[URIRef | Literal]:
        """Implements this if the class adds additional axioms"""
        return []

    @property
    @abc.abstractmethod
    def sharedReferences(self) -> MutableMapping[str, BNode]: ...

    def get_wsdlIRIReference(self, fragment_identifier=None,) -> URIRef:
        """Described in `http://www.w3.org/TR/wsdl20/#wsdl-iri-references`_
        :term:`Fragment Identifiers` can be viewed in `https://www.w3.org/TR/wsdl/#frag-ids`_
        """
        q = urlparse(self.targetNamespace)
        if fragment_identifier is None:
            fragment_identifier = self.fragment_identifier
        return URIRef(urlunparse(q._replace(fragment = fragment_identifier)))
    wsdlIRIReference = property(fget=get_wsdlIRIReference)

    @property
    @abc.abstractmethod
    def fragment_identifier(self) -> str: ...

    @property
    @abc.abstractmethod
    def targetNamespace(self) -> str: ...

class wsdl_description(_wsdl_idelement, Description):
    """`https://www.w3.org/TR/wsdl/#Description`_"""
    name = None
    def __init__(self, trans: str, parentnode: Union["_start", "_state"],
                 attrs: Mapping,
                 namespaces: Mapping[str, str] = {},
                 default_namespace: Optional[str] = None,
                 ) -> None:
        super().__init__(trans, parentnode, attrs,
                         namespaces, default_namespace)
        self.axioms.add((self.wsdlIRIReference,
                         RDF.type,
                         WSDL.Description))
        self._sharedReferences = {}

    @property
    def bindings(self) -> Iterable["wsdl_binding"]:
        return [x for x in self.child_nodes if isinstance(x, wsdl_binding)]

    @property
    def element_declarations(self) -> Iterable:
        REMOVE_EMPTY = str.maketrans({" ": None})
        types = next(x for x in self.child_nodes
                     if isinstance(x, wsdl_types))
        elem_decls = list(types.get_element_declarations())
        raise NotImplementedError(elem_decls)
        try:
            elems_str = self.attrs[(None, "element")]
        except KeyError:
            return []
        elems = elems_str.translate(REMOVE_EMPTY).split(",")
        raise Exception(elems)
        return [x for x in self.child_nodes
                if isinstance(x, wsdl_elementDeclaration)]

    @property
    def interfaces(self) -> Iterable["wsdl_interface"]:
        return [x for x in self.child_nodes if isinstance(x, wsdl_interface)]

    @property
    def services(self) -> Iterable["wsdl_service"]:
        return [x for x in self.child_nodes if isinstance(x, wsdl_service)]

    @property
    def type_definitions(self) -> Iterable["wsdl_types"]:
        types = next(x for x in self.child_nodes if isinstance(x, wsdl_types))
        return types.get_type_definitions()

    @property
    def sharedReferences(self) -> MutableMapping[str, BNode]:
        return self._sharedReferences

    @property
    def fragment_identifier(self) -> str:
        return "wsdl.description()"

    @property
    def targetNamespace(self) -> str:
        try:
            return self.attrs[(None, 'targetNamespace')]
        except KeyError:
            return self.attrs[(_ns_wsdl, 'targetNamespace')]

class _wsdl_with_QNameMapping(_wsdl_element):
    local_name: str
    """Either 'wsdl.description', 'wsdl.'interface', 'wsdl.binding',
    'wsdl.service', 'wsdl.interfaceMessageReference',
    'wsdl.interfaceFaultReference', 'wsdl.interfaceFault',
    'wsdl.bindingOperation', 'wsdl.bindingFault'
    """
    @property
    def QName(self):
        return "%s#%s" % (self.parentnode.targetNamespace,
                          self.local_name)

class wsdl_documentation(_wsdl_with_QNameMapping): ...

class wsdl_typeextension(_to_ElementTree):
    """
    is used in documentation.types as extension for every type
    """
    convert_function: Callable[[ET.ElementTree], Graph]
    TRANS2CONVERTFUNCTION = extensions.TYPES_EXTENSIONS
    xml_info: ET.ElementTree
    rdf_info: Graph
    def __init__(
            self, trans: [str, str], parentnode: Union["_start", "_state"],
            attrs: Mapping,
            namespaces: Mapping[str, str] = {},
            default_namespace: Optional[str] = None,
            ) -> None:
        self.convert_function = self.TRANS2CONVERTFUNCTION[trans]
        super().__init__(trans, parentnode, attrs,
                         namespaces, default_namespace)
        self.trans = trans

    def get_type_definitions(self) -> Iterable[TypeDefinition]:
        raise NotImplementedError()

    def get_element_declarations(self) -> Iterable[ElementDeclaration]:
        raise NotImplementedError(ET.tostring(self.xml_info.getroot()))

    def close(self):
        ret = super().close()
        self.xml_info = ET.ElementTree(self.element)
        self.rdf_info = self.convert_function(self.xml_info)
        return ret

class wsdl_types(_wsdl_element):
    """
    :TODO: xs:import is missing as expected transtype
    """
    _default_state = wsdl_typeextension
    child_nodes: Iterable["wsdl_typeextension"]

    def get_type_definitions(self) -> Iterable[TypeDefinition]:
        for x in self.child_nodes.get_type_definitions():
            yield x

    def get_element_declarations(self) -> Iterable[ElementDeclaration]:
        for x in self.child_nodes:
            for y in x.get_element_declarations():
                yield y


class _wsdl_properties(_wsdl_idelement):
    _fragment_base: str
    _property_URI: URIRef
    _type_URI: URIRef
    def __init__(self, trans: str, parentnode: Union["_start", "_state"],
                 attrs: Mapping,
                 namespaces: Mapping[str, str] = {},
                 default_namespace: Optional[str] = None,
                 ) -> None:
        super().__init__(trans, parentnode, attrs,
                         namespaces, default_namespace)
        myid = self.wsdlIRIReference
        newaxioms = [
                (myid, RDF.type, self._type_URI),
                (self.parentnode.wsdlIRIReference, self._property_URI, myid),
                ]
        for ax in newaxioms:
            self.axioms.add(ax)

    @property
    def sharedReferences(self) -> MutableMapping[str, BNode]:
        return self.parentnode.sharedReferences

    @property
    def fragment_identifier(self) -> str:
        """default"""
        return self._fragment_base % self.name

    @property
    def targetNamespace(self) -> str:
        return self.parentnode.targetNamespace

    @property
    @abc.abstractmethod
    def name(self) -> str: ...


class wsdl_interface(_wsdl_properties, Interface):
    _fragment_base = "wsdl.interface(%s)"
    _property_URI = WSDL.interface
    _type_URI = WSDL.Interface
    def _additional_frames(self) -> Iterable[URIRef | Literal]:
        yield RDFS.label, Literal(self.name)

    @property
    def name(self) -> str:
        return self.attrs[(None, "name")]

    @property
    def extended_interfaces(self) -> Iterable[Tuple[str, str]]:
        """
        :TODO: Implement according to `https://www.w3.org/TR/wsdl/#Interface`_
        """
        try:
            ext_int_str = self.attrs[(None, "extends")]
        except KeyError:
            return []
        else:
            raise NotImplementedError(ext_int_str)

    @property
    def interface_faults(self) -> Iterable["wsdl_interfaceFault"]:
        return [x for x in self.child_nodes
                if isinstance(x, wsdl_interfaceFault)]

    @property
    def interface_operations(self) -> Iterable["wsdl_interfaceOperation"]:
        return [x for x in self.child_nodes
                if isinstance(x, wsdl_interfaceOperation)]


class wsdl_binding(_wsdl_properties, Binding):
    _fragment_base = "wsdl.binding(%s)"
    _property_URI = WSDL.binding
    _type_URI = WSDL.Binding
    EXTENSIONS = extensions.BINDING_EXTENSIONS
    """This determines which extensions are used for the binding. Default is
    the same as extensions.BINDING_EXTENSIONS
    """
    def get(self, namespace: str, name: str, as_qname: bool=False,
            **kwargs: Any) -> str:
        if kwargs:
            raise TypeError("Unexpected keywords: %s" % kwargs)
        try:
            q = self.attrs[(namespace, name)]
        except KeyError:
            raise
            return None
        if as_qname:
            return name2qname(q, self.default_namespace, self.namespaces)
        return q

    @property
    def binding_faults(self) -> Iterable["wsdl_bindingFault"]:
        return (x for x in self.child_nodes
                if isinstance(x, wsdl_bindingFault))
    @property
    def binding_operations(self) -> Iterable["wsdl_bindingOperation"]:
        return (x for x in self.child_nodes
                if isinstance(x, wsdl_bindingOperation))

    def __init__(self, trans: str, parentnode: Union["_start", "_state"],
                 attrs: Mapping,
                 namespaces: Mapping[str, str] = {},
                 default_namespace: Optional[str] = None,
                 ) -> None:
        super().__init__(trans, parentnode, attrs,
                         namespaces, default_namespace)

        #yield WHTTP.defaultQueryParameterSeparator, Literal("&")
        myid = self.wsdlIRIReference
        namespace2annotation = get_namespaces_with_annotations(self.attrs)
        for ns, anno in namespace2annotation.items():
            try:
                ext = self.EXTENSIONS[ns]
            except KeyError:
                pass
            else:
                for ax in ext(myid, anno, self.namespaces, default_namespace):
                    self.axioms.add(ax)

    def _additional_frames(self) -> Iterable[URIRef | Literal]:
        for x in super()._additional_frames():
            yield x
        yield RDFS.label, Literal(self.name)
        yield RDF.type, URIRef(self.type)

        #interf_ns, interf_name = name2qname(self.interface,
        #                                    self.default_namespace,
        #                                    self.namespaces)
        #p = urlparse(interf_ns)._replace(fragment="wsdl.interface(%s)"
        #                                 % (interf_name))
        #yield WSDL.binds, URIRef(urlunparse(p))


    def get_extensionData(self) -> Mapping[(str, str), str]:
        return {key: x for key, x in self.attrs.items()
                if key[0] is not None}

    @property
    def type(self) -> str:
        return self.attrs[(None, "type")]

    @property
    def interface(self) -> wsdl_interface:
        inter_ns, inter_name = name2qname(self.attrs[(None, "interface")],
                                          self.default_namespace,
                                          self.namespaces)
        return next(x for x in self.parent.interfaces
                    if x.name == inter_name and x.targetNamespace == inter_ns)

    @property
    def name(self) -> str:
        return self.attrs[(None, "name")]


class wsdl_service(_wsdl_properties, Service):
    _fragment_base = "wsdl.service(%s)"
    _property_URI = WSDL.service
    _type_URI = WSDL.Service
    def _additional_frames(self) -> Iterable[URIRef | Literal]:
        return
        for x in super()._additional_frames():
            yield x
        yield RDFS.label, Literal(self.name)
        ns, name = self.interface
        p = urlparse(ns)._replace(fragment="wsdl.interface(%s)" % name)
        yield WSDL.implements, URIRef(urlunparse(p))

    @property
    def endpoints(self) -> Iterable["wsdl_endpoint"]:
        return (x for x in self.child_nodes
                if isinstance(x, wsdl_endpoint))

    @property
    def interface(self) -> "wsdl_interface":
        name = self.attrs[(None, "interface")]
        inter_ns, inter_name = name2qname(name, self.default_namespace,
                                          self.namespaces)
        return next(x for x in self.parent.interfaces
                    if x.name == inter_name and x.targetNamespace == inter_ns)

    @property
    def name(self) -> str:
        return self.attrs[(None, "name")]


class wsdl_bindingFault(_wsdl_properties, BindingFault):
    _fragment_base = "wsdl.bindingFault(%s)"
    _property_URI = WSDL.bindingFault
    _type_URI = WSDL.BindingFault
    EXTENSIONS = extensions.BINDING_FAULT_EXTENSIONS
    def get(self, namespace: str, name: str, as_qname: bool=False,
            **kwargs: Any) -> str:
        if kwargs:
            raise TypeError("Unexpected keywords: %s" % kwargs)
        try:
            q = self.attrs[(namespace, name)]
        except KeyError:
            raise
            return None
        if as_qname:
            return name2qname(q, self.default_namespace, self.namespaces)
        return q

    def __init__(self, trans: str, parentnode: Union["_start", "_state"],
                 attrs: Mapping,
                 namespaces: Mapping[str, str] = {},
                 default_namespace: Optional[str] = None,
                 ) -> None:
        super().__init__(trans, parentnode, attrs,
                         namespaces, default_namespace)
        myid = self.wsdlIRIReference
        namespace2annotation = get_namespaces_with_annotations(self.attrs)
        for ns, anno in namespace2annotation.items():
            try:
                ext = self.EXTENSIONS[ns]
            except KeyError:
                pass
            else:
                for ax in ext(myid, anno, self.namespaces, default_namespace):
                    self.axioms.add(ax)

    def _additional_frames(self) -> Iterable[URIRef | Literal]:
        return
        for x in super()._additional_frames():
            yield x
        interface_ns, interface_name = name2qname(self.interface, self.default_namespace, self.namespaces)
        fault_ns, fault_name = name2qname(self.ref, self.default_namespace, self.namespaces)
        #assert interface_ns == fault_ns
        p = urlparse(interface_ns)._replace(fragment="wsdl.interfaceFault(%s/%s)" % (interface_name, fault_name))
        yield WSDL.binds, URIRef(urlunparse(p))

    @property
    def interface_fault(self) -> "wsdl_interfaceFault":
        ref_ns, ref_name = name2qname(self.attrs[(None, "ref")],
                                      self.default_namespace,
                                      self.namespaces)
        return self.parent.parent.get_interfaceFault(ref_ns, ref_name)

    @property
    def ref(self) -> str:
        return self.attrs[(None, "ref")]

    @property
    def interface(self) -> str:
        return self.parentnode.interface

    @property
    def bindingName(self) -> str:
        return self.parentnode.name

    @property
    def faultName(self) -> str:
        return self.name

    @property
    def name(self) -> str:
        ns, name = name2qname(self.attrs[(None, "ref")],
                              self.default_namespace, self.namespaces)
        return name

    @property
    def fragment_identifier(self) -> str:
        return "wsdl.bindingFault(%s/%s)" % (self.bindingName, self.name)

class wsdl_bindingOperation(_wsdl_properties, BindingOperation):
    _fragment_base = "wsdl.bindingOperation(%s)"
    _property_URI = WSDL.bindingOperation
    _type_URI = WSDL.BindingOperation
    EXTENSIONS = extensions.BINDING_OPERATION_EXTENSIONS
    def get(self, namespace: str, name: str, as_qname: bool=False,
            **kwargs: Any) -> str:
        if kwargs:
            raise TypeError("Unexpected keywords: %s" % kwargs)
        try:
            q = self.attrs[(namespace, name)]
        except KeyError:
            raise
            return None
        if as_qname:
            return name2qname(q, self.default_namespace, self.namespaces)
        return q

    @property
    def binding_fault_references(self):
        return (x for x in self.child_nodes
                if isinstance(x, (wsdl_bindingFaultReferenceIn,
                                  wsdl_bindingFaultReferenceOut)))

    @property
    def binding_message_references(self) -> Iterable["BindingMessageReference"]:
        return (x for x in self.child_nodes
                if isinstance(x, wsdl_bindingMessageReference))

    @property
    def interface_operation(self) -> "wsdl_interfaceOperation":
        ref_ns, ref_name = name2qname(self.attrs[(None, "ref")],
                                      self.default_namespace,
                                      self.namespaces)
        return self.parent.parent.get_interfaceOperation(ref_ns, ref_name)

    def __init__(self, trans: str, parentnode: Union["_start", "_state"],
                 attrs: Mapping,
                 namespaces: Mapping[str, str] = {},
                 default_namespace: Optional[str] = None,
                 ) -> None:
        super().__init__(trans, parentnode, attrs,
                         namespaces, default_namespace)
        myid = self.wsdlIRIReference
        namespace2annotation = get_namespaces_with_annotations(self.attrs)
        for ns, anno in namespace2annotation.items():
            try:
                ext = self.EXTENSIONS[ns]
            except KeyError:
                pass
            else:
                for ax in ext(myid, anno, self.namespaces, default_namespace):
                    self.axioms.add(ax)

    def _additional_frames(self) -> Iterable[URIRef | Literal]:
        return
        for x in super()._additional_frames():
            yield x
        #yield RDFS.label, Literal(self.name)
        #elem = self.sharedReferences.setdefault(self.element, BNode())
        #yield WSDL.elementDeclaration, elem
        #yield WSDL.messageContentModel, WSDL.ElementContent
        interface_ns, interface_name = name2qname(self.interface, self.default_namespace, self.namespaces)
        fault_ns, fault_name = name2qname(self.ref, self.default_namespace, self.namespaces)
        #assert interface_ns == fault_ns
        p = urlparse(interface_ns)._replace(fragment="wsdl.interfaceOperation(%s/%s)" % (interface_name, fault_name))
        yield WSDL.binds, URIRef(urlunparse(p))

    @property
    def interface(self) -> str:
        return self.parentnode.interface

    @property
    def ref(self) -> str:
        return self.attrs[(None, "ref")]

    @property
    def bindingName(self) -> str:
        return self.parentnode.name

    @property
    def operationName(self) -> str:
        return self.name

    @property
    def name(self) -> str:
        ns, name = name2qname(self.attrs[(None, "ref")],
                              self.default_namespace, self.namespaces)
        return name

    @property
    def fragment_identifier(self) -> str:
        return "wsdl.bindingOperation(%s/%s)" % (self.bindingName, self.name)

class wsdl_bindingMessageReference(_wsdl_element, BindingMessageReference):
    def get(self, namespace: str, name: str, as_qname: bool=False,
            **kwargs: Any) -> str:
        if kwargs:
            raise TypeError("Unexpected keywords: %s" % kwargs)
        try:
            q = self.attrs[(namespace, name)]
        except KeyError:
            raise
            return None
        if as_qname:
            return name2qname(q, self.default_namespace, self.namespaces)
        return q

    def __init__(self, *args, **kwargs):
        raise NotImplementedError()

class wsdl_bindingFaultReference(_wsdl_element, BindingFaultReference):
    def get(self, namespace: str, name: str, as_qname: bool=False,
            **kwargs: Any) -> str:
        if kwargs:
            raise TypeError("Unexpected keywords: %s" % kwargs)
        try:
            q = self.attrs[(namespace, name)]
        except KeyError:
            raise
            return None
        if as_qname:
            return name2qname(q, self.default_namespace, self.namespaces)
        return q

class wsdl_messageReferenceIn(_wsdl_properties):
    """More information in `https://www.w3.org/TR/wsdl/#Binding_Message_Reference_XMLRep`_
    """
    EXTENSIONS = extensions.MESSAGE_REFERENCE_EXTENSIONS
    def __init__(self, *args, **kwargs):
        raise NotImplementedError()

class wsdl_messageReferenceOut(_wsdl_properties):
    """More information in `https://www.w3.org/TR/wsdl/#Binding_Message_Reference_XMLRep`_
    """
    EXTENSIONS = extensions.MESSAGE_REFERENCE_EXTENSIONS
    def __init__(self, *args, **kwargs):
        raise NotImplementedError()

class wsdl_bindingFaultReferenceIn(wsdl_bindingFaultReference):
    """More information in `https://www.w3.org/TR/wsdl/#Binding_Fault_Reference`_
    """
    EXTENSIONS = extensions.MESSAGE_FAULT_EXTENSIONS
    def __init__(self, *args, **kwargs):
        raise NotImplementedError()

class wsdl_bindingFaultReferenceOut(wsdl_bindingFaultReference):
    """More information in `https://www.w3.org/TR/wsdl/#Binding_Fault_Reference`_
    """
    EXTENSIONS = extensions.MESSAGE_FAULT_EXTENSIONS
    def __init__(self, *args, **kwargs):
        raise NotImplementedError()


class wsdl_interfaceFault(_wsdl_properties, InterfaceFault):
    _fragment_base = "wsdl.interfaceFault(%s)"
    _property_URI = WSDL.interfaceFault
    _type_URI = WSDL.InterfaceFault
    def __init__(self, *args, **kwargs):
        """
        :TODO: remove qname2rdffranes from here.
        """
        super().__init__(*args, **kwargs)
        elem = self.sharedReferences.setdefault(self.element, BNode())
        for pred, obj in qname2rdfframes(self.element, self.namespaces,
                                         self.default_namespace):
            self.axioms.add((elem, pred, obj))

    @property
    def message_content_model(self) -> str:
        try:
            elem = self.attrs[(None, "element")]
        except KeyError:
            return MCM_OTHER
        try:
            name2qname(elem, self.default_namespace, self.namespaces)
        except Exception:
            assert elem in (MCM_ANY, MCM_NONE, MCM_OTHER, MCM_ELEMENT)
            return elem
        else:
            return MCM_ELEMENT

    @property
    def element_declaration(self) -> Tuple[str, str]:
        """
        :raises AttributeError:
        """
        try:
            elem = self.attrs[(None, "element")]
        except KeyError as err:
            raise AttributeError("No element declaration") from err
        try:
            elem_ns, elem_name = name2qname(elem, self.default_namespace, self.namespaces)
        except Exception as err:
            raise AttributeError("No element declaration") from err
        return elem_ns, elem_name

    def _additional_frames(self) -> Iterable[URIRef | Literal]:
        for x in super()._additional_frames():
            yield x
        yield RDFS.label, Literal(self.name)
        elem = self.sharedReferences.setdefault(self.element, BNode())
        yield WSDL.elementDeclaration, elem
        yield WSDL.messageContentModel, WSDL.ElementContent

    @property
    def element(self) -> str:
        return self.attrs[(None, "element")]

    @property
    def interfaceName(self) -> str:
        return self.parentnode.name

    @property
    def faultName(self) -> str:
        return self.name

    @property
    def name(self) -> str:
        return self.attrs[(None, "name")]

    @property
    def fragment_identifier(self) -> str:
        return "wsdl.interfaceFault(%s/%s)" % (self.interfaceName, self.name)

class wsdl_interfaceOperation(_wsdl_properties, InterfaceOperation):
    _fragment_base = "wsdl.interfaceOperation(%s)"
    _property_URI = WSDL.interfaceOperation
    _type_URI = WSDL.InterfaceOperation
    input: Optional["wsdl_input"]
    output: Optional["wsdl_output"]
    def _additional_frames(self) -> Iterable[URIRef | Literal]:
        for x in super()._additional_frames():
            yield x
        yield RDFS.label, Literal(self.name)
        if self.attrs[(_ns_wsdlx, "safe")]:
            yield SAWSDL.modelReference, WSDLX.SafeInteraction
        else:
            raise NotImplementedError()
        yield WSDL.messageExchangePattern, URIRef(self.message_exchange_pattern)
        for style in self.style:
            yield WSDL_RDF.operationStyle, URIRef(style)

    def get(self, namespace: str, name: str, as_qname: bool=False,
            **kwargs: Any) -> str:
        if kwargs:
            raise TypeError("Unexpected keywords: %s" % kwargs)
        try:
            q = self.attrs[(namespace, name)]
        except KeyError:
            raise
            return None
        if as_qname:
            return name2qname(q, self.default_namespace, self.namespaces)
        return q

    @property
    def interface_fault_references(
            self) -> Iterable["InterfaceFaultReference"]:
        return [x for x in self.child_nodes
                if isinstance(x, (wsdl_infault, wsdl_outfault))]

    @property
    def interface_message_references(
            self) -> Iterable["wsdl_interfaceMessageReference"]:
        return [x for x in self.child_nodes
                if isinstance(x, (wsdl_input, wsdl_output))]


    @property
    def style(self) -> Iterable[str]:
        _remove_emptyspace = str.maketrans({" ": None})
        style_list_str = self.attrs[(None, "style")]
        styles = style_list_str.translate(_remove_emptyspace).split(",")
        return styles

    @property
    def safe(self) -> str:
        """Implements acces to if operation is safe.
        See `https://www.w3.org/TR/wsdl20-adjuncts/#safety`_
        """
        return self.attrs.get((_ns_wsdlx, "safe"), "xs:false")

    @property
    def message_exchange_pattern(self) -> str:
        return self.attrs.get((None, "pattern"),
                              "http://www.w3.org/ns/wsdl/in-out")

    @property
    def interfaceName(self) -> str:
        return self.parentnode.name

    @property
    def operationName(self) -> str:
        return self.name

    @property
    def name(self) -> str:
        return self.attrs[(None, "name")]

    @property
    def fragment_identifier(self) -> str:
        return "wsdl.interfaceOperation(%s/%s)" % (self.interfaceName, self.name)

class wsdl_endpoint(_wsdl_properties, Endpoint):
    """:term:`wsdl endpoint`
    For more information see `https://www.w3.org/TR/wsdl/#Endpoint`_
    """
    _fragment_base = "wsdl.endpoint(%s)"
    _property_URI = WSDL.endpoint
    _type_URI = WSDL.Endpoint
    EXTENSIONS = extensions.ENDPOINT_EXTENSIONS
    def __init__(self, trans: str, parentnode: Union["_start", "_state"],
                 attrs: Mapping,
                 namespaces: Mapping[str, str] = {},
                 default_namespace: Optional[str] = None,
                 ) -> None:
        super().__init__(trans, parentnode, attrs,
                         namespaces, default_namespace)

        #yield WHTTP.defaultQueryParameterSeparator, Literal("&")
        myid = self.wsdlIRIReference
        namespace2annotation = get_namespaces_with_annotations(self.attrs)
        for ns, anno in namespace2annotation.items():
            try:
                ext = self.EXTENSIONS[ns]
            except KeyError:
                logger.debug("Found data for '%s' but no corresponding "
                             "extension was found for %s" % (ns, type(self)))
            else:
                for ax in ext(myid, anno, self.namespaces, default_namespace):
                    self.axioms.add(ax)

    def get(self, namespace: str, name: str, as_qname: bool=False,
            **kwargs: Any) -> str:
        if kwargs:
            raise TypeError("Unexpected keywords: %s" % kwargs)
        try:
            q = self.attrs[(namespace, name)]
        except KeyError:
            raise
            return None
        if as_qname:
            return name2qname(q, self.default_namespace, self.namespaces)
        return q

    def _additional_frames(self) -> Iterable[URIRef | Literal]:
        for x in super()._additional_frames():
            yield x
        yield RDFS.label, Literal(self.name)
        yield WSDL.address, URIRef(self.address)
        fake_fragment = "wsdl.binding(%s)" % (self.binding)
        fake_reference = self.get_wsdlIRIReference(
                fragment_identifier=fake_fragment,
                )
        yield WSDL.usesBinding, fake_reference

    @property
    def binding(self) -> str:
        ns, name = name2qname(self.attrs[(None, "binding")],
                              self.default_namespace, self.namespaces)
        return next(x for x in self.parent.parent.bindings
                    if x.name == name and x.targetNamespace == ns)

    @property
    def address(self) -> str:
        return self.attrs[(None, "address")]

    @property
    def service(self) -> str:
        return self.parentnode

    @property
    def name(self) -> str:
        return self.attrs[(None, "name")]

    @property
    def fragment_identifier(self) -> str:
        return "wsdl.endpoint(%s/%s)" % (self.service.name, self.name)

class _wsdl_interfaceReference(_wsdl_properties):
    contentmodel: str
    def __init__(self, trans: Tuple[str, str],
                 parentnode: Union["_start", "_state"],
                 attrs: Mapping,
                 namespaces: Mapping[str, str] = {},
                 default_namespace: Optional[str] = None,
                 ) -> None:
        super().__init__(trans, parentnode, attrs, namespaces,
                         default_namespace)

    def _additional_frames(self) -> Iterable[URIRef | Literal]:
        for x in super()._additional_frames():
            yield x
        yield WSDL.messageContentModel, self.contentModel

    @property
    def contentModel(self) -> URIRef:
        if (None, "any") in self.attrs:
            return WSDL.AnyContent
        elif (None, "none") in self.attrs:
            return WSDL.NoContent
        elif (None, "other") in self.attrs:
            return WSDL.OtherContent
        elif (None, "element") in self.attrs:
            return WSDL.ElementContent
        else:
            logger.critical(self.attrs)
            raise SyntaxError("Didnt contain valid content description")



class _wsdl_interfaceMessageReference(_wsdl_interfaceReference, InterfaceMessageReference):
    _fragment_base = "wsdl.interfaceMessageReference(%s)"
    _property_URI = WSDL.interfaceMessageReference
    _type_URI = WSDL.InterfaceMessageReference

    @property
    def element_declaration(self) -> Tuple[str, str]:
        """
        :raises AttributeError:
        """
        try:
            elem = self.attrs[(None, "element")]
        except KeyError as err:
            raise AttributeError("No element declaration") from err
        try:
            elem_ns, elem_name = name2qname(elem, self.default_namespace, self.namespaces)
        except Exception as err:
            raise AttributeError("No element declaration") from err
        return elem_ns, elem_name
        q = self._get_all_element_declarations()

        raise Exception(q)
        q = [x for x in self.child_nodes
                if isinstance(x, wsdl_elementDeclaration)]
        raise Exception(elem_ns, elem_name, q)

    @property
    def message_content_model(self) -> str:
        try:
            elem = self.attrs[(None, "element")]
        except KeyError:
            return MCM_OTHER
        try:
            name2qname(elem, self.default_namespace, self.namespaces)
        except Exception:
            assert elem in (MCM_ANY, MCM_NONE, MCM_OTHER, MCM_ELEMENT)
            return elem
        else:
            return MCM_ELEMENT

    @property
    def message_label(self) -> str:
        return self.attrs[(None, "messageLabel")]

    @property
    def interface(self) -> str:
        return self.parentnode.parentnode

    @property
    def operation(self) -> str:
        return self.parentnode

    @property
    def name(self) -> str:
        return self.attrs[(None, "messageLabel")]

    @property
    def fragment_identifier(self) -> str:
        return "wsdl.interfaceMessageReference(%s/%s/%s)"\
                % (self.interface.name, self.operation.name, self.name)

class wsdl_input(_wsdl_interfaceMessageReference):
    @property
    def direction(self) -> str: return "in"
    def __init__(self, trans: str, parentnode: Union["_start", "_state"],
                 attrs: Mapping,
                 namespaces: Mapping[str, str] = {},
                 default_namespace: Optional[str] = None,
                 ) -> None:
        super().__init__(trans, parentnode, attrs,
                         namespaces, default_namespace)
        self.parentnode.input = self
        elem = self.sharedReferences.setdefault(self.element, BNode())
        for pred, obj in qname2rdfframes(self.element, self.namespaces,
                                         self.default_namespace):
            self.axioms.add((elem, pred, obj))

    def _additional_frames(self) -> Iterable[URIRef | Literal]:
        for x in super()._additional_frames():
            yield x
        yield RDF.type, WSDL.InputMessage
        p = urlparse(self.parentnode.message_exchange_pattern)._replace(fragment=self.name)
        yield WSDL.messageLabel, URIRef(urlunparse(p))
        elem = self.sharedReferences.setdefault(self.element, BNode())
        yield WSDL.elementDeclaration, elem

    @property
    def element(self) -> str:
        return self.attrs[(None, "element")]

class wsdl_output(_wsdl_interfaceMessageReference):
    @property
    def direction(self) -> str: return "out"
    def __init__(self, trans: str, parentnode: Union["_start", "_state"],
                 attrs: Mapping,
                 namespaces: Mapping[str, str] = {},
                 default_namespace: Optional[str] = None,
                 ) -> None:
        super().__init__(trans, parentnode, attrs,
                         namespaces, default_namespace)
        self.parentnode.output = self
        elem = self.sharedReferences.setdefault(self.element, BNode())
        for pred, obj in qname2rdfframes(self.element, self.namespaces,
                                         self.default_namespace):
            self.axioms.add((elem, pred, obj))

    def _additional_frames(self) -> Iterable[URIRef | Literal]:
        for x in super()._additional_frames():
            yield x
        yield RDF.type, WSDL.OutputMessage
        p = urlparse(self.parentnode.message_exchange_pattern)._replace(fragment=self.name)
        yield WSDL.messageLabel, URIRef(urlunparse(p))
        elem = self.sharedReferences.setdefault(self.element, BNode())
        yield WSDL.elementDeclaration, elem

    @property
    def element(self) -> str:
        return self.attrs[(None, "element")]

#class _wsdl_interfaceFaultReference(_wsdl_interfaceReference):
class _wsdl_interfaceFaultReference(_wsdl_properties, InterfaceFaultReference):
    _fragment_base = "wsdl.interfaceFaultReference(%s)"
    _property_URI = WSDL.interfaceFaultReference
    _type_URI = WSDL.InterfaceFaultReference

    @property
    def interface(self) -> str:
        return self.parentnode.parentnode

    @property
    def operation(self) -> str:
        return self.parentnode

    @property
    def name(self) -> str:
        ns, name = name2qname(self.attrs[(None, "ref")],
                              self.default_namespace, self.namespaces)
        return name

    @property
    def message_label(self) -> str:
        return self.attrs[(None, "messageLabel")]

    @property
    def fragment_identifier(self) -> str:
        return "wsdl.interfaceFaultReference(%s/%s/%s/%s)"\
                % (self.interface.name, self.operation.name,
                   self.message_label, self.name)

class wsdl_infault(_wsdl_interfaceFaultReference):
    @property
    def interface_fault(self):
        raise NotImplementedError()
        return next(x for x in self.parent.parent.interface_faults
                    if True)

    @property
    def direction(self) -> str:
        return "in"

    def _additional_frames(self) -> Iterable[URIRef | Literal]:
        for x in super()._additional_frames():
            yield x
        yield RDF.type, WSDL.OutputMessage
        messageLabel = self.attrs[(None, "messageLabel")]
        p = urlparse(self.parentnode.message_exchange_pattern)._replace(fragment=messageLabel)
        yield WSDL.messageLabel, URIRef(urlunparse(p))
        fake_fragment = "wsdl.interfaceFault(%s/%s)" % (self.interface.name, self.name)
        fake_reference = self.get_wsdlIRIReference(fake_fragment)
        yield WSDL.interfaceFault, fake_reference

    @property
    def message(self) -> Optional[wsdl_output]:
        return self.operation.output

class wsdl_outfault(_wsdl_interfaceFaultReference):
    @property
    def interface_fault(self) -> wsdl_interfaceFault:
        ref_ns, ref_name = name2qname(self.attrs[(None, "ref")],
                                      self.default_namespace,
                                      self.namespaces)
        return next(x for x in self.interface.interface_faults
                    if x.name == ref_name and x.targetNamespace == ref_ns)

    @property
    def direction(self) -> str:
        return "out"

    def _additional_frames(self) -> Iterable[URIRef | Literal]:
        for x in super()._additional_frames():
            yield x
        yield RDF.type, WSDL.OutputMessage
        messageLabel = self.attrs[(None, "messageLabel")]
        p = urlparse(self.parentnode.message_exchange_pattern)._replace(fragment=messageLabel)
        yield WSDL.messageLabel, URIRef(urlunparse(p))
        fake_fragment = "wsdl.interfaceFault(%s/%s)" % (self.interface.name, self.name)
        fake_reference = self.get_wsdlIRIReference(fake_fragment)
        yield WSDL.interfaceFault, fake_reference

    @property
    def message(self) -> Optional[wsdl_output]:
        return self.operation.output

class wsdl_fault(_wsdl_element): ...

class wsdl_operation(_wsdl_element): ...

_start._special_states = {
        (_ns_wsdl, "description"): wsdl_description,
        #_ns_wsdl + "": ,
        }
#_createnode_mixin._default_state = _state_with_axioms
wsdl_description._special_states = {
        (_ns_wsdl, "documentation"): wsdl_documentation,
        (_ns_wsdl, "binding"): wsdl_binding,
        (_ns_wsdl, "interface"): wsdl_interface,
        (_ns_wsdl, "service"): wsdl_service,
        (_ns_wsdl, "types"): wsdl_types,
        }
wsdl_types._special_states = {
        }
#wsdl_types._default_state = _to_ElementTree
wsdl_binding._special_states = {
        (_ns_wsdl, "operation"): wsdl_bindingOperation,
        (_ns_wsdl, "fault"): wsdl_bindingFault,
        }

wsdl_interface._special_states = {
        (_ns_wsdl, "operation"): wsdl_interfaceOperation,
        (_ns_wsdl, "fault"): wsdl_interfaceFault,
        }

wsdl_service._special_states = {
        (_ns_wsdl, "endpoint"): wsdl_endpoint,
        }

wsdl_bindingOperation._special_states = {
        (_ns_wsdl, "input"): wsdl_messageReferenceIn,
        (_ns_wsdl, "output"): wsdl_messageReferenceOut,
        (_ns_wsdl, "infault"): wsdl_bindingFaultReferenceIn,
        (_ns_wsdl, "outfault"): wsdl_bindingFaultReferenceOut,
        }

wsdl_interfaceOperation._special_states = {
        (_ns_wsdl, "input"): wsdl_input,
        (_ns_wsdl, "output"): wsdl_output,
        (_ns_wsdl, "infault"): wsdl_infault,
        (_ns_wsdl, "outfault"): wsdl_outfault,
        }

wsdl_service._special_states = {
        (_ns_wsdl, "endpoint"): wsdl_endpoint,
        }

def get_namespaces_with_annotations(attrs: Mapping[Tuple[str, str], str],
                                    ) -> Mapping[str, Mapping[str, str]]:
    ns2anno = {}
    for key, x in attrs.items():
        ns, attr = key
        if ns is not None and ns is not _ns_wsdl:
            ns2anno.setdefault(ns, {})[attr] = x
    return ns2anno
