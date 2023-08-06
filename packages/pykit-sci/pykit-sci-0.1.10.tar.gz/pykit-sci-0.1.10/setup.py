# -*- coding: utf-8 -*-
"""pykit-sci: collection of python modules for science.

*pykit-sci* is a collection of python modules for science.

For documentation, please see
`pykit-sci documentation <http://projects.geekspin.net/pykit-sci/doc>`_

"""

DOCLINES = __doc__.split("\n")

import os
import sys
import subprocess

from setuptools import setup, find_packages

#from numpy.distutils.core import setup

if sys.version_info[:2] < (2, 7):
    raise RuntimeError("Python version 2.7 required.")

CLASSIFIERS = """\
Development Status :: 4 - Beta
Intended Audience :: Science/Research
License :: OSI Approved :: BSD License
Operating System :: MacOS :: MacOS X
Operating System :: Microsoft :: Windows
Operating System :: POSIX
Operating System :: Unix
Programming Language :: Python
Programming Language :: Python :: 2.7
Topic :: Software Development
Topic :: Scientific/Engineering

"""

MAJOR = 0
MINOR = 1
MICRO = 10
ISRELEASED = True
VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)


def git_version():
    """Return the GIT version as a string."""
    def _minimal_ext_cmd(cmd):
        # construct minimal environment
        env = {}
        for k in ['SYSTEMROOT', 'PATH']:
            v = os.environ.get(k)
            if v is not None:
                env[k] = v
        # LANGUAGE is used on win32
        env['LANGUAGE'] = 'C'
        env['LANG'] = 'C'
        env['LC_ALL'] = 'C'
        out = \
            subprocess.Popen(cmd,
                             stdout=subprocess.PIPE, env=env).communicate()[0]
        return out

    try:
        out = _minimal_ext_cmd(['git', 'rev-parse', 'HEAD'])
        GIT_REVISION = out.strip().decode('ascii')
    except OSError:
        GIT_REVISION = "Unknown"

    return GIT_REVISION


def get_version_info():
    # Adding the git rev number needs to be done inside
    # write_version_py(), otherwise the import of pksci.version messes
    # up the build under Python 3.
    FULLVERSION = VERSION
    if os.path.exists('.git'):
        GIT_REVISION = git_version()
    elif os.path.exists('pksci/version.py'):
        # must be a source distribution, use existing version file
        # load it as a separate module to not load pksci/__init__.py
        import imp
        version = imp.load_source('pksci.version', 'pksci/version.py')
        GIT_REVISION = version.git_revision
    else:
        GIT_REVISION = "Unknown"

    if not ISRELEASED:
        FULLVERSION += '.dev-' + GIT_REVISION[:7]

    return FULLVERSION, GIT_REVISION


def write_version_py(filename='pksci/version.py'):
    cnt = """
# THIS FILE IS GENERATED FROM PKSCI SETUP.PY
short_version = '%(version)s'
version = '%(version)s'
full_version = '%(full_version)s'
git_revision = '%(git_revision)s'
release = %(isrelease)s

if not release:
    version = full_version
"""
    FULLVERSION, GIT_REVISION = get_version_info()

    a = open(filename, 'w')
    try:
        a.write(cnt % {'version': VERSION,
                       'full_version': FULLVERSION,
                       'git_revision': GIT_REVISION,
                       'isrelease': str(ISRELEASED)})
    finally:
        a.close()


def configuration(parent_package='', top_path=None):
    if os.path.exists('MANIFEST'):
        os.remove('MANIFEST')

    from numpy.distutils.misc_util import Configuration
    config = Configuration(None, parent_package, top_path)

    config.set_options(ignore_setup_xxx_py=True,
                       assume_default_configuration=True,
                       delegate_options_to_subpackages=True,
                       quiet=True)

    config.add_subpackage('pksci')

    return config


def setup_package():

    # Rewrite the version file everytime
    write_version_py()

    FULLVERSION, GIT_REVISION = get_version_info()

    setup_options = dict(
        name='pykit-sci',
        version=FULLVERSION,
        author='Andrew Merrill',
        author_email='androomerrill@gmail.com',
        description=DOCLINES[0],
        long_description="\n".join(DOCLINES[2:]),
        url='http://github.com/androomerrill/pykit-sci',
        license='BSD 2-Clause',
        classifiers=[_f for _f in CLASSIFIERS.split('\n') if _f],
        platforms=["Linux", "OS-X", "Unix", "Windows"],
        configuration=configuration,
        packages=find_packages(exclude=['doc']),
        include_package_data=True,
        exclude_package_data={'': ['README', 'README.rst',
                                   '*.gif', '*.html', '*.ui']},
        zip_safe=False,
        install_requires=['numpy>=1.8', 'scipy>=0.13', 'pint>=0.5',
                          'openpyxl>=1.8', 'configobj>=5.0'],
        entry_points={
            'console_scripts': [
                'analyze_txtlog = pksci.scripts.analyze_txtlog:main',
                'change_ext = pksci.scripts.change_ext:main',
                'mkbkupcp = pksci.scripts.mkbkupcp:main',
                'plot_CNT_Ch_map = pksci.scripts.plot_CNT_Ch_map:main',
                'plot_data = pksci.scripts.plot_data:main',
                'tachyon_render = pksci.scripts.tachyon_render:main',
                'timestamp_frames = pksci.scripts.timestamp_frames:main',
                'tga2png = pksci.scripts.tga2png:main',
                'txtlog2xlsx = pksci.scripts.txtlog2xlsx:main',
            ],
        }
    )

    setup(**setup_options)

if __name__ == '__main__':
    setup_package()
