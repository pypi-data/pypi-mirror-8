from setuptools import setup

import imp


def get_version():
    ver_file = None
    try:
        ver_file, pathname, description = imp.find_module('__version__', ['src/vcstools'])
        vermod = imp.load_module('__version__', ver_file, pathname, description)
        version = vermod.version
        return version
    finally:
        if ver_file is not None:
            ver_file.close()


setup(name='vcstools',
      version=get_version(),
      packages=['vcstools'],
      package_dir={'': 'src'},
      scripts=[],
      install_requires=['pyyaml', 'python-dateutil'],
      author="Tully Foote, Thibault Kruse, Ken Conley",
      author_email="tfoote@osrfoundation.org",
      url="http://wiki.ros.org/vcstools",
      download_url="http://download.ros.org/downloads/vcstools/",
      keywords=["scm", "vcs", "git", "svn", "hg", "bzr"],
      classifiers=["Programming Language :: Python",
                   "Programming Language :: Python :: 2",
                   "Programming Language :: Python :: 3",
                   "License :: OSI Approved :: BSD License"],
      description="VCS/SCM source control library for svn, git, hg, and bzr",
      long_description="""\
Library for managing source code trees from multiple version control systems.
Current supports svn, git, hg, and bzr.
""",
      license="BSD")
