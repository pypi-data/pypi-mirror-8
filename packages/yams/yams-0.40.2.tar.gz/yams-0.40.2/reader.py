# copyright 2004-2014 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of yams.
#
# yams is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# yams is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with yams. If not, see <http://www.gnu.org/licenses/>.
"""ER schema loader.

Use either a sql derivated language for entities and relation definitions
files or a direct python definition file.
"""

__docformat__ = "restructuredtext en"

import sys
import types
from os import listdir
from os.path import exists, join, splitext, basename, abspath
from warnings import warn

from logilab.common import tempattr
from logilab.common.modutils import modpath_from_file, cleanup_sys_modules

from yams import UnknownType, BadSchemaDefinition, BASE_TYPES
from yams import constraints, schema as schemamod
from yams import buildobjs


CONSTRAINTS = {}
# add constraint classes to the context
for objname in dir(constraints):
    if objname[0] == '_':
        continue
    obj = getattr(constraints, objname)
    try:
        if issubclass(obj, constraints.BaseConstraint) and (
            not obj is constraints.BaseConstraint):
            CONSTRAINTS[objname] = obj
    except TypeError:
        continue


def obsolete(cls):
    def wrapped(*args, **kwargs):
        reason = '%s should be explictly imported from %s' % (
            cls.__name__, cls.__module__)
        warn(reason, DeprecationWarning, stacklevel=2)
        return cls(*args, **kwargs)
    return wrapped

def fill_schema(schema, erdefs, register_base_types=True,
                remove_unused_rtypes=False, post_build_callbacks=[]):
    if register_base_types:
        buildobjs.register_base_types(schema)
    # relation definitions may appear multiple times
    erdefs_vals = set(erdefs.values())
    # register relation types and non final entity types
    for definition in erdefs_vals:
        if isinstance(definition, type):
            definition = definition()
        if isinstance(definition, buildobjs.RelationType):
            schema.add_relation_type(definition)
        elif isinstance(definition, buildobjs.EntityType):
            schema.add_entity_type(definition)
    # register relation definitions
    for definition in erdefs_vals:
        if isinstance(definition, type):
            definition = definition()
        definition.expand_relation_definitions(erdefs, schema)
    # call 'post_build_callback' functions found in schema modules
    for cb in post_build_callbacks:
        cb(schema)
    # finalize schema
    schema.finalize()
    # check permissions are valid on entities and relations
    for erschema in schema.entities() + schema.relations():
        erschema.check_permission_definitions()
    # check unique together consistency
    for eschema in schema.entities():
        eschema.check_unique_together()
    # optionaly remove relation types without definitions
    if remove_unused_rtypes:
        for rschema in schema.relations():
            if not rschema.rdefs:
                schema.del_relation_type(rschema)
    return schema


class SchemaLoader(object):
    """the schema loader is responsible to build a schema object from a
    set of files
    """
    schemacls = schemamod.Schema
    extrapath = None
    context = dict([(attr, getattr(buildobjs, attr))
                    for attr in buildobjs.__all__])
    context.update(CONSTRAINTS)

    def load(self, directories, name=None,
             register_base_types=True, construction_mode='strict',
             remove_unused_rtypes=True):
        """return a schema from the schema definition read from <directory>
        """
        self.defined = {}
        self.loaded_files = []
        self.post_build_callbacks = []
        sys.modules[__name__].context = self
        # ensure we don't have an iterator
        directories = tuple(directories)
        try:
            self._load_definition_files(directories)
            schema = self.schemacls(name or 'NoName', construction_mode=construction_mode)
            try:
                fill_schema(schema, self.defined, register_base_types,
                            remove_unused_rtypes=remove_unused_rtypes,
                            post_build_callbacks=self.post_build_callbacks)
            except Exception as ex:
                if not hasattr(ex, 'schema_files'):
                    ex.schema_files = self.loaded_files
                raise
        finally:
            # cleanup sys.modules from schema modules
            # ensure we're only cleaning schema [sub]modules
            directories = [(not directory.endswith(self.main_schema_directory)
                            and join(directory, self.main_schema_directory)
                            or directory)
                           for directory in directories]
            cleanup_sys_modules(directories)
        schema.loaded_files = self.loaded_files
        return schema

    def _load_definition_files(self, directories):
        for directory in directories:
            package = basename(directory)
            for filepath in self.get_schema_files(directory):
                with tempattr(buildobjs, 'PACKAGE', package):
                    self.handle_file(filepath)

    # has to be overridable sometimes (usually for test purpose)
    main_schema_directory = 'schema'
    def get_schema_files(self, directory):
        """return an ordered list of files defining a schema

        look for a schema.py file and or a schema sub-directory in the given
        directory
        """
        result = []
        if exists(join(directory, self.main_schema_directory + '.py')):
            result = [join(directory, self.main_schema_directory + '.py')]
        if exists(join(directory, self.main_schema_directory)):
            directory = join(directory, self.main_schema_directory)
            for filename in listdir(directory):
                if filename[0] == '_':
                    if filename == '__init__.py':
                        result.insert(0, join(directory, filename))
                    continue
                ext = splitext(filename)[1]
                if ext == '.py':
                    result.append(join(directory, filename))
                else:
                    self.unhandled_file(join(directory, filename))
        return result

    def handle_file(self, filepath):
        """handle a partial schema definition file according to its extension
        """
        assert filepath.endswith('.py'), 'not a python file'
        if filepath not in self.loaded_files:
            modname, module = self.exec_file(filepath)
            objects_to_add = set()
            for name, obj in vars(module).items():
                if (isinstance(obj, type)
                    and issubclass(obj, buildobjs.Definition)
                    and obj.__module__ == modname
                    and not name.startswith('_')):
                    objects_to_add.add(obj)
            for obj in objects_to_add:
                self.add_definition(obj, filepath)
            self.loaded_files.append(filepath)

    def unhandled_file(self, filepath):
        """called when a file without handler associated has been found,
        does nothing by default.
        """
        pass

    def add_definition(self, defobject, filepath=None):
        """file handler callback to add a definition object

        wildcard capability force to load schema in two steps : first register
        all definition objects (here), then create actual schema objects (done in
        `_build_schema`)
        """
        if not issubclass(defobject, buildobjs.Definition):
            raise BadSchemaDefinition(filepath, 'invalid definition object')
        defobject.expand_type_definitions(self.defined)

    def import_erschema(self, ertype, schemamod=None, instantiate=True):
        warn('import_erschema is deprecated, use explicit import once schema '
             'is turned into a proper python module (eg not expecting '
             'predefined context in globals)', DeprecationWarning, stacklevel=3)
        try:
            erdef = self.defined[ertype]
            name = getattr(erdef, 'name', erdef.__name__)
            if name == ertype:
                assert instantiate, 'can\'t get class of an already registered type'
                return erdef
        except KeyError:
            pass
        assert False, 'ooups'

    def exec_file(self, filepath):
        try:
            modname = '.'.join(modpath_from_file(filepath, self.extrapath))
            doimport = True
        except ImportError:
            warn('module for %s can\'t be found, add necessary __init__.py '
                 'files to make it importable' % filepath, DeprecationWarning)
            modname = splitext(basename(filepath))[0]
            doimport = False
        # XXX can't rely on __import__ until bw compat (eg implicit import) needed
        #if doimport:
        #    module = __import__(modname, fglobals)
        #    for part in modname.split('.')[1:]:
        #        module = getattr(module, part)
        #else:
        if modname in sys.modules:
            module = sys.modules[modname]
            # NOTE: don't test raw equality to avoid .pyc / .py comparisons
            assert abspath(module.__file__).startswith(abspath(filepath)), (
                modname, filepath, module.__file__)
        else:
            # XXX until bw compat is gone, put context into builtins to allow proper
            # control of deprecation warning
            from six.moves import builtins
            fglobals = {} # self.context.copy()
            # wrap callable that should be imported
            for key, val in self.context.items():
                if key in BASE_TYPES or key == 'RichString' or key in CONSTRAINTS or \
                       key in ('SubjectRelation', 'ObjectRelation'):
                    val = obsolete(val)
                setattr(builtins, key, val)
            builtins.import_erschema = self.import_erschema
            fglobals['__file__'] = filepath
            fglobals['__name__'] = modname
            package = '.'.join(modname.split('.')[:-1])
            if package and not package in sys.modules:
                __import__(package)
            with open(filepath) as f:
                exec(f.read(), fglobals)
            # check for use of classes that should be imported, without
            # importing them
            for name, obj in fglobals.items():
                if isinstance(obj, type) and \
                       issubclass(obj, buildobjs.Definition) and \
                       obj.__module__ == modname:
                    for parent in obj.__bases__:
                        pname = parent.__name__
                        if pname in fglobals or not pname in self.context:
                            # imported
                            continue
                        warn('%s: please explicitly import %s (%s)'
                             % (filepath, pname, name), DeprecationWarning)
            #for key in self.context:
            #    fglobals.pop(key, None)
            fglobals['__file__'] = filepath
            module = types.ModuleType(str(modname))
            module.__dict__.update(fglobals)
            sys.modules[modname] = module
            if package:
                setattr(sys.modules[package], modname.split('.')[-1], module)
        if hasattr(module, 'post_build_callback'):
            self.post_build_callbacks.append(module.post_build_callback)
        return (modname, module)

# XXX backward compatibility to prevent changing cw.schema and cw.test.unittest_schema (3.12.+)
PyFileReader = SchemaLoader
PyFileReader.__init__ = lambda *x: None

def fill_schema_from_namespace(schema, items, **kwargs):
    erdefs = {}
    for name, obj in items:
        if (isinstance(obj, type) and issubclass(obj, buildobjs.Definition)
            and obj not in (buildobjs.Definition, buildobjs.RelationDefinition, buildobjs.EntityType)):
            obj.expand_type_definitions(erdefs)
    fill_schema(schema, erdefs, **kwargs)

def build_schema_from_namespace(items):
    schema = schemamod.Schema('noname')
    fill_schema_from_namespace(schema, items)
    return schema

class _Context(object):
    def __init__(self):
        self.defined = {}

context = _Context()
