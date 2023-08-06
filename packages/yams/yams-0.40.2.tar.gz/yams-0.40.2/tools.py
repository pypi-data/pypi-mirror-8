"""some yams command line tools"""

import sys
from os.path import exists, join, dirname
from tempfile import NamedTemporaryFile
from subprocess import Popen
from traceback import extract_tb

from logilab.common.configuration import Configuration

from yams.__pkginfo__ import version
from yams import schema2dot
from yams.reader import SchemaLoader
from yams._exceptions import *

def _error(file=None, line=None, msg=''):
    if file is None:
        file = sys.argv[1]
    if line is None:
        line=''
    else:
        line = str(line)
    print >> sys.stderr, ':'.join(('E', file, line, msg))

def check_schema():
    config = Configuration(
        usage="yams-check [[[...] deps] deps] apps",
        doc="Check the schema of an application.",
        version=version)
    dirnames = config.load_command_line_configuration()
    if not dirnames:
        print >> sys.stderr, config.help()
        return 2
    for dir in dirnames:
        assert exists(dir), dir
    try:
        SchemaLoader().load(dirnames)
        return 0
    except Exception, ex:
        tb_offset = getattr(ex, 'tb_offset', 0)
        filename, lineno, func, text = extract_tb(sys.exc_traceback)[-1-tb_offset]
        if hasattr(ex, "schema_files"):
            filename = ', '.join(ex.schema_files)
        _error(filename, lineno,"%s -> %s" % (ex.__class__.__name__, ex))
        return 2

def schema_image():
    options = [('output-file', {'type':'file', 'default': None,
                 'metavar': '<file>', 'short':'o', 'help':'output image file'}),
               ('viewer', {'type': 'string', 'default':"rsvg-view", 'short': "w", 'metavar':'<cmd>',
                 'help':'command use to view the generated file (empty for none)'}),
               ('lib-dir', {'type': 'string', 'short': "L", 'metavar':'<dir>',
                 'help':'directory to look for schema dependancies'}),
              ]

    config = Configuration(options=options,
        usage="yams-view [-L <lib_dir> | [[[...] deps] deps]] apps",
        version=version)
    dirnames = config.load_command_line_configuration()

    lib_dir = config['lib-dir']
    assert lib_dir is not None
    if lib_dir is not None:
        app_dir = dirnames[-1]
        from cubicweb.cwconfig import CubicWebConfiguration as cwcfg
        packages = cwcfg.expand_cubes(dirnames)
        packages = cwcfg.reorder_cubes(packages)
        packages = [pkg for pkg in packages if pkg != app_dir]
    elif False:
        glob = globals().copy()
        execfile(join(app_dir,"__pkginfo__.py"), glob)
        #dirnames = [ join(lib_dir,dep) for dep in glob['__use__']]+dirnames
        packages = [ dep for dep in glob['__use__']]


    for dir in dirnames:
        assert exists(dir), dir

    import cubicweb
    cubicweb_dir = dirname(cubicweb.__file__)

    schm_ldr = SchemaLoader()

    class MockConfig(object):
        def packages(self):
            return packages
        def packages_path(self):
            return packages
        def schemas_lib_dir(self):
            return join(cubicweb_dir,"schemas")
        #def apphome(self):
        #    return lib_dir
        apphome = dirnames[0]
        def appid(self):
            "bob"

    print MockConfig().packages()

    schema = schm_ldr.load(MockConfig())


    out, viewer = config['output-file'], config['viewer']
    if out is None:
        tmp_file = NamedTemporaryFile(suffix=".svg")
        out = tmp_file.name
    schema2dot.schema2dot(schema, out, #size=size,
        skiprels=("identity",), skipentities=("Person","AbstractPerson","Card","AbstractCompany","Company","Division"))
    if viewer:
        p = Popen((viewer, out))
        p.wait()

    return 0
