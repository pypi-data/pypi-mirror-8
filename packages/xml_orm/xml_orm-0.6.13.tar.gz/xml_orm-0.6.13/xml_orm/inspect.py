#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
if sys.version_info >= (3,):
    basestring = str
    unicode = str
    bytes = bytes
else:
    basestring = basestring
    unicode = unicode
    bytes = str

from io import BytesIO

from .core import Schema, XML_ORM_Error
from .fields import *


class ConversionError(XML_ORM_Error):
    pass

try:
    from lxml import etree
except ImportError:
    from xml.etree import ElementTree as etree

xs = "http://www.w3.org/2001/XMLSchema"
_nsmap = {
    'xs': xs
}

_QN = etree.QName


_xsd_to_field_cls = {
    'xs:integer': IntegerField,
    'xs:float': FloatField,
    'xs:decimal': DecimalField,
    'xs:date': DateTimeField,
    'xs:boolean': BooleanField,
}


def _parse_complex(root, level=0, ctypes={}, stypes={}):
    fieldnum = 1
    fields = {}
    is_choice = False
    doc = root.find('xs:annotation', namespaces=_nsmap)
    if doc is not None:
        fields['doc'] = doc.findtext('xs:documentation', namespaces=_nsmap).strip()
    contents = root.find('xs:sequence', namespaces=_nsmap)
    if contents is None:
        contents = root.find('xs:choice', namespaces=_nsmap)
        is_choice = contents is not None
    if contents is not None:
        if (contents.get('minOccurs', "1") != "1" or
                contents.get('maxOccurs', "1") != "1"):
            raise ConversionError('Sequences/Choices with non-default minOccurs or '
                                  'maxOccurs are not supported')
        for sub in contents:
            if sub.tag == _QN(xs, 'element'):
                name = 'field_{0}'.format(fieldnum)
                fieldnum += 1
                fields[name] = _parse_elt(sub, name, None, level + 1, ctypes,
                                          stypes)
            elif sub.tag == _QN(xs, 'sequence') or sub.tag == _QN(xs, 'choice'):
                raise ConversionError('Nested sequences/choices are not supported')

    for sub in root.findall('xs:attribute', namespaces=_nsmap):
        props = dict(tag=sub.get('name'), cls=SimpleField)
        st = sub.find('xs:simpleType', namespaces=_nsmap)
        elt_type = sub.get('type')
        if st is not None:
            props.update(_parse_simple(st))
        elif elt_type in stypes:
            props.update(stypes[elt_type])
        elif elt_type:
            props['cls'] = _xsd_to_field_cls.get(elt_type, SimpleField)
        props['default'] = sub.get('default')
        if sub.get('use') == 'optional':
            props['minOccurs'] = 0
        cls = props.pop('cls')
        fields['field_{0}'.format(fieldnum)] = cls.A(**props)
        fieldnum += 1
    fields['__is_choice'] = is_choice
    return fields


def _parse_elt(root, name, target_ns, level=0, ctypes={}, stypes={}):
    ct = root.find('xs:complexType', namespaces=_nsmap)
    st = root.find('xs:simpleType', namespaces=_nsmap)
    elt_type = root.get('type')
    minOccurs = int(root.get('minOccurs', 1))
    try:
        maxOccurs = int(root.get('maxOccurs', 1))
    except ValueError:
        maxOccurs = 'unbounded'
    props = dict(
        tag=root.get('name'), minOccurs=minOccurs, maxOccurs=maxOccurs)
    doc = root.find('xs:annotation', namespaces=_nsmap)
    if doc is not None:
        props['doc'] = doc.findtext('xs:documentation', namespaces=_nsmap).strip()
    cls = None
    if ct is not None:
        props.update(_parse_complex(ct, level, ctypes, stypes))
        cls = Schema
    elif st is not None:
        props.update(_parse_simple(st))
        cls = props.pop('cls')
    elif elt_type in ctypes:
        cls = ctypes[elt_type]
    elif elt_type in stypes:
        props.update(stypes[elt_type])
        cls = props.pop('cls')
    elif elt_type:
        cls = _xsd_to_field_cls.get(elt_type, SimpleField)

    if not cls:
        raise ConversionError('Unable to determine element class for element {0} {1}'
                              .format(root.tag, root.get('name')))

    if isinstance(cls, basestring):
        props['ref'] = cls
        return ComplexField(**props)
    elif isinstance(cls, type) and issubclass(cls, Schema):
        if level == 0:
            meta_props = dict(root=props.pop('tag'))
            if target_ns is not None:
                meta_props['namespace'] = target_ns
            props['Meta'] = type('Meta', (object,), meta_props)
            doc = props.pop('doc', None)
            res = type(name, (cls, ), props)
            if doc is not None:
                res.__doc__ = doc
            return res
        else:
            return ComplexField(cls, **props)
    else:
        return cls(**props)


def _parse_simple(root):
    args = {}
    restr = root.find('xs:restriction', namespaces=_nsmap)
    if restr is not None:
        base = restr.get('base')
        args['cls'] = _xsd_to_field_cls.get(base, SimpleField)
        for facet in restr:
            if facet.tag == _QN(xs, 'enumeration'):
                args['restrict'] = args.get('restrict', [])
                args['restrict'].append(facet.get('value'))
            elif facet.tag == _QN(xs, 'minLength'):
                args['min_length'] = int(facet.get('value'))
                args['cls'] = CharField
            elif facet.tag == _QN(xs, 'maxLength'):
                args['max_length'] = int(facet.get('value'))
                args['cls'] = CharField
            elif facet.tag == _QN(xs, 'pattern'):
                args['pattern'] = facet.get('value')
    return args


def _parse_xsd(root):
    result = []
    ctypes = {}
    stypes = {}
    clsnum = 1
    target_ns = root.get('targetNamespace', None)
    for st in root.findall('xs:simpleType', namespaces=_nsmap):
        name = st.get('name')
        stypes[name] = _parse_simple(st)
    for ct in root.findall('xs:complexType', namespaces=_nsmap):
        name = ct.get('name')
        ctypes[name] = 'Class_{0}'.format(clsnum)
        clsnum += 1
    clsnum = 1
    for ct in root.findall('xs:complexType', namespaces=_nsmap):
        name = ct.get('name')
        fields = _parse_complex(ct, ctypes=ctypes, stypes=stypes)
        newcls = type('Class_{0}'.format(clsnum), (Schema, ), fields)
        ctypes[name] = newcls
        clsnum += 1
    for elt in root.findall('xs:element', namespaces=_nsmap):
        name = 'Class_{0}'.format(clsnum)
        clsnum += 1
        newcls = _parse_elt(elt, name, target_ns, ctypes=ctypes, stypes=stypes)
        if newcls:
            result.append(newcls)
    return result


def inspect_xsd(root):
    ''' Автоматическое преобразование XSD-схемы в класс `Schema`. Возвращает
        все найденные в схеме глобальные типы данных в виде
        списка классов.

        :root: Может принимать значения:
            * Строка Unicode с XSD, либо с именем файла.
            * Байтовая строка с XSD.
            * Файло-подобный объект.

        :returns: список классов.

    '''
    if isinstance(root, unicode):
        try:
            root = etree.fromstring(root.encode('utf-8'))
        except:
            root = etree.parse(root).getroot()
    elif isinstance(root, bytes):
        cont = BytesIO(root)
        root = etree.parse(cont).getroot()
    elif hasattr(root, 'read'):
        root = etree.parse(root).getroot()
    return _parse_xsd(root)


def main():
    if len(sys.argv) < 3:
        print('''Usage: inspect.py schema1.xsd [schema2.xsd ...] result.py
or: inspect.py schema1.xsd [schema2.xsd ...] - ''')
        sys.exit(1)
    resfile = sys.argv[-1]
    if resfile != '-' and not resfile.endswith('.py'):
        print('''Target file extension must be .py''')
        sys.exit(2)
    result = codecs.open(resfile, 'wb', encoding='utf-8') if resfile != '-' else sys.stdout
    result.write('# coding: utf-8\n')
    for xsd in sys.argv[1:-1]:
        for res in inspect_xsd(unicode(xsd)):
            s = res.reverse()
            result.write(s)
