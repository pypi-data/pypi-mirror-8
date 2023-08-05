import collections
import inspect
import xml.etree.ElementTree as ElementTree

DUM_NONE = object()  # no parsed value


#
# ##  TARGET ATTRIBUTES
#
class _AbstractTarget(object):
    # constants
    ATOM = 0
    NODE = 1
    ARRAY = 2

    # defaults
    source = None
    attribname = None  # None:child or attr, False: only child, str: attr

    def fixSource(self, source):
        "split attribute and source path parts"
        items = source.rsplit("/@", 1)
        if len(items) == 2:
            self.source, self.attribname = items
        elif source == "dum_content":
            self.source = "."
            self.attribname = False
        else:
            self.source = source
            if "/" in source:
                self.attribname = False

    def register(self, bysources, defaults):
        "used for dum class initalization"
        bysources.append((self.source, self))
        if self.default is not DUM_NONE:
            defaults[self.target] = self

    def put(self, obj, value):
        "set value as obj attribute"
        setattr(obj, self.target, value)

    def set_default(self, obj):
        "set obj default attribute value"
        setattr(obj, self.target, self.default)


class Atom(_AbstractTarget):
    """convert to a single value (int,str...)"""
    kind = _AbstractTarget.ATOM

    def __init__(self, convert, source=None, target=None, default=DUM_NONE):
        self.parse = convert
        if source is not None:
            self.fixSource(source)
        self.target = target
        self.default = default


class Node(_AbstractTarget):
    """convert to a class"""
    kind = _AbstractTarget.NODE

    def __init__(self, cls, source=None, target=None, default=DUM_NONE):
        self.cls = cls
        if source is not None:
            self.fixSource(source)
        self.target = target
        self.default = default


class Array(_AbstractTarget):
    """convert to a list of objects"""
    kind = _AbstractTarget.ARRAY

    def __init__(self, sources=None, target=None):
        self.sources = sources
        self.target = target

    def register(self, bysources, defaults):
        "used for dum class initalization"
        for k in self.sources:
            bysources.append((k, self))
        defaults[self.target] = self

    def put(self, obj, value):
        "set value in obj list attribute"
        try:
            array = getattr(obj, self.target)
        except AttributeError:
            array = []
            setattr(obj, self.target, array)
        array.append(value)

    def set_default(self, obj):
        "default is alwaus an empty list"
        setattr(obj, self.target, [])


#
# ## CONVERTER DECORATORS
#
def converter(source=None, default=DUM_NONE):
    if isinstance(source, collections.Callable):
        # called without attributes
        return Atom(convert=source, default=default)

    def _converter(convert):
        return Atom(convert=convert, source=source, default=default)
    return _converter


def lister(source=None):
    if isinstance(source, collections.Callable):
        # called without attributes
        subfield = field(source, source=source.__name__)
        return Array(sources={source.__name__: subfield})

    def _lister(convert):
        subfield = field(convert, source=source)
        return Array(sources={source: subfield})
    return _lister


#
# ## FIELD FUNCTIONS
#
class group:
    "put several node types on the same list"
    def __init__(self, **kwds):
        self.kwds = kwds

    def toArrayField(self, source):
        source = source+"/" if source else ""
        kwds = {}
        for k, v in self.kwds.items():
            k = source+k
            kwds[k] = field(v, source=k)
        return Array(kwds)


def field(value, source, default=DUM_NONE):
    "low level field definition"
    # do we need to have it public ?
    if hasattr(value, "dum"):
        if inspect.isclass(value):
            return Node(value, source=source, default=default)
        else:
            if default is DUM_NONE:
                default = value
            return Node(type(value), source=source, default=default)

    if isinstance(value, collections.Callable):
        return Atom(value, source=source)
    if type(value) == list:
        subfield = field(value[0], source=source, default=default)
        return Array(sources={subfield.source: subfield})

    if default is DUM_NONE:
        default = value
    return Atom(type(value), source=source, default=default)


#
# ## PRIVATE FUNCTIONS
#
def _field_initialize(value, cls, name):
    "initializing one dum field"
    if type(value) == tuple:
        value, source = value
    else:
        source = None

    if isinstance(value, group):
        value = value.toArrayField(source)
    else:
        if source is None:
            source = name
        if isinstance(value, _AbstractTarget):
            if value.source is None:
                value.fixSource(source)
        else:
            value = field(value, source)
    if value.target is None:
        value.target = name
    return value


def _bysources(cls):
    "lazy dum class initialization, return source paths"
    dum = cls.dum
    try:
        return dum.__bysources__
    except AttributeError:
        pass
    # initialize dum declaration
    bysources = []
    defaults = {}
    for name in dir(dum):
        if name.startswith("__") and name.endswith("__"):
            continue  # special methods
        value = getattr(dum, name)
        field = _field_initialize(value, dum, name)
        field.register(bysources, defaults)

    # TODO check for duplicated target ?
    dum.__bysources__ = bysources
    dum.__defaults__ = defaults
    return bysources


def _fix_defaults(obj, cls, defined_targets):
    "finalize obj : default values and dum_projection() call"
    defaults = [v for (k, v) in cls.dum.__defaults__.items()
                if k not in defined_targets]
    for field in defaults:
        field.set_default(obj)
    try:
        dum_projection = obj.dum_projection
    except AttributeError:
        return obj
    return dum_projection()


#
# ##  CSV PARSING
#
def csv(cls, rows, headers=None):
    rows = iter(rows)
    # dum declaration
    bysources = dict(_bysources(cls))
    defined_targets = set()
    # column headers
    fields = []
    if headers is None:
        headers = next(rows)  # assume headers are in the first row
    for i, source in enumerate(headers):
        try:
            field = bysources[source]
        except KeyError:
            continue
        fields.append((i, field))
        defined_targets.add(field.target)
    # actual paring
    for row in rows:
        obj = cls()
        for i, field in fields:
            v = field.parse(row[i])
            field.put(obj, v)
        yield _fix_defaults(obj, cls, defined_targets)


#
# ##  JSON PARSING
#
def _jxpath(sp, idx, values):

    k = sp[idx]
    idx += 1
    if type(values) != list:
        values = (values,)
    for value in values:
        try:
            v = value[k]
        except KeyError:
            continue

        if idx >= 0:
            if type(v) == list:
                for a in v:
                    yield a
            else:
                yield v
        else:
            for i in _jxpath(sp, idx, v):
                yield i


def jxpath(path, values):
    sp = []
    for p in path.split('/'):
        if p == '.':
            continue
        if p in ('..', '', '*'):
            raise ValueError("NotImplemented")
        if p.startswith('['):
            # TODO attrs could be implemented by looking at dict values
            raise ValueError("attributes not supported in jxpath")

        sp.append(p)
    for i in _jxpath(sp, -len(sp), values):
        yield i


def json(cls, values):
    bysources = _bysources(cls)
    defined_targets = set()
    obj = cls()
    for key, field in bysources:
        putfield = field
        if field.kind == field.ARRAY:
            field = field.sources[key]
        for v in jxpath(key, values):
            if field.kind == field.ATOM:
                childobj = field.parse(v)
            elif field.kind == field.NODE:
                childobj = json(field.cls, v)
            else:
                raise TypeError("unknown field type")
            putfield.put(obj, childobj)
            defined_targets.add(putfield.target)
            if putfield.kind != putfield.ARRAY:
                break
    return _fix_defaults(obj, cls, defined_targets)


#
# ## XML PARSING
#

def _XmlParseAtom(field, putfield, obj, child):
    defined_target = None
    if field.attribname:
        values = [child.attrib.get(field.attribname, None)]
    else:
        values = [child.text]
        if putfield.kind == field.ARRAY:
            values += [gchild.tail for gchild in child]
    for value in values:
        if value is not None:
            childobj = field.parse(value)
            putfield.put(obj, childobj)
            defined_target = putfield.target
    return defined_target


def _XmlParseNode(field, putfield, obj, child):
    childobj = _XmlParseElement(field.cls, child)
    putfield.put(obj, childobj)
    return putfield.target

# not use singledispatch now for 3.3 compatibility
_XmlParsing = {_AbstractTarget.ATOM: _XmlParseAtom,
               _AbstractTarget.NODE: _XmlParseNode}


def _XmlParseElement(cls, elmt):
    bysources = _bysources(cls)
    defined_targets = set()
    obj = cls()

    # children
    attribs = []
    for match, field in bysources:
        putfield = field
        if field.kind == field.ARRAY:
            field = field.sources[match]
            children = elmt.findall(match)
        else:
            child = elmt.find(match)
            if child is None:
                if field.attribname is None:
                    attribs.append((match, field))
                continue
            children = (child,)

        parsing = _XmlParsing[field.kind]
        for child in children:
            defined_target = parsing(field, putfield, obj, child)
            defined_targets.add(defined_target)

    # curent node attributes
    for key, field in attribs:
        try:
            value = elmt.attrib[key]
        except KeyError:
            continue
        putfield = field
        if field.kind == field.ARRAY:
            field = field.sources[key]

        if field.kind == field.ATOM:
            childobj = field.parse(value)
        else:
            # TODO put value in node.dum_content ?
            raise ValueError("attr can't map to node "+putfield.target)
        putfield.put(obj, childobj)
        defined_targets.add(putfield.target)
    return _fix_defaults(obj, cls, defined_targets)


def xmls(cls, txt):
    root = ElementTree.fromstring(txt)
    return _XmlParseElement(cls, root)


def xml(cls, fd):
    tree = ElementTree.parse(fd)
    root = tree.getroot()
    return _XmlParseElement(cls, root)
