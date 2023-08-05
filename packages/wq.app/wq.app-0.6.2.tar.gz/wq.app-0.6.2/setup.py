import os
from setuptools import setup, find_packages

LONG_DESCRIPTION = """
JavaScript web apps with RequireJS, jQuery Mobile, Mustache, and Leaflet
"""


def parse_markdown_readme():
    """
    Convert README.md to RST via pandoc, and load into memory
    (fallback to LONG_DESCRIPTION on failure)
    """
    # Attempt to run pandoc on markdown file
    import subprocess
    try:
        subprocess.call(
            ['pandoc', '-t', 'rst', '-o', 'README.rst', 'README.md']
        )
    except OSError:
        return LONG_DESCRIPTION

    # Attempt to load output
    try:
        readme = open(os.path.join(
            os.path.dirname(__file__),
            'README.rst'
        ))
    except IOError:
        return LONG_DESCRIPTION
    return readme.read()


def list_package_data(root):
    """
    List top level js, css, & scss folders for inclusion as package data
    """
    paths = []
    for base, dirs, files in os.walk(root):
        paths.extend([os.path.join(base, name) for name in files])
    return paths


def create_wq_namespace():
    """
    Generate the wq namespace package
    (not checked in, as it technically is the parent of this folder)
    """
    if os.path.isdir("wq"):
        return
    os.makedirs("wq")
    init = open(os.path.join("wq", "__init__.py"), 'w')
    init.write("__import__('pkg_resources').declare_namespace(__name__)")
    init.close()


create_wq_namespace()
package_data = [os.path.join("build", "r.js")]
for folder in ['js', 'css', 'scss']:
    package_data.extend(list_package_data(folder))

setup(
    name='wq.app',
    version='0.6.2',
    author='S. Andrew Sheppard',
    author_email='andrew@wq.io',
    url='http://wq.io/wq.app',
    license='MIT',
    packages=['wq', 'wq.app', 'wq.app.build'],
    package_dir={
        'wq.app': '.',
        'wq.app.build': './build',
    },
    package_data={
        'wq.app': package_data
    },
    namespace_packages=['wq'],
    description=LONG_DESCRIPTION.strip(),
    long_description=parse_markdown_readme(),
    install_requires=['pyscss==1.1.5'],
    scripts=[os.path.join('.', 'build', 'wq')],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: JavaScript',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Pre-processors',
    ]
)
