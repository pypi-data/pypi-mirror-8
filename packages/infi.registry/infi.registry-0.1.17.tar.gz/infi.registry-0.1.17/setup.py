
SETUP_INFO = dict(
    name = 'infi.registry',
    version = '0.1.17',
    author = 'Shai Keren',
    author_email = 'shaik@infinidat.com',

    url = 'https://github.com/Infinidat/infi.registry',
    license = 'PSF',
    description = """a Python dictionary-like interface to the Windows Registry""",
    long_description = """an easy-to-use wrapper to the Windows Registry APIs:
* implemented directly over ctypes, not _winreg or pywin32
* fully supports unicode""",

    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Python Software Foundation License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    install_requires = ['munch',
'setuptools'],
    namespace_packages = ['infi'],

    package_dir = {'': 'src'},
    package_data = {'': []},
    include_package_data = True,
    zip_safe = False,

    entry_points = dict(
        console_scripts = [],
        gui_scripts = [],
        ),
)

if SETUP_INFO['url'] is None:
    _ = SETUP_INFO.pop('url')

def setup():
    from setuptools import setup as _setup
    from setuptools import find_packages
    SETUP_INFO['packages'] = find_packages('src')
    _setup(**SETUP_INFO)

if __name__ == '__main__':
    setup()

