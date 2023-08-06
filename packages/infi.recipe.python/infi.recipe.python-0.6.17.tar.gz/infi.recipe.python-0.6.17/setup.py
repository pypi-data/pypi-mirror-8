
SETUP_INFO = dict(
    name = 'infi.recipe.python',
    version = '0.6.17',
    author = 'Guy Rozendorn',
    author_email = 'guy@rzn.co.il',

    url = 'https://github.com/Infinidat/infi.recipe.python',
    license = 'PSF',
    description = """a recipe for downloading and packing portable builds of Python""",
    long_description = """when building large applications in Python, you want to embed the interpreter within your app. This recipe lets you do it""",

    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Python Software Foundation License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    install_requires = [
'infi.os_info',
'setuptools',
'zc.buildout'
],
    namespace_packages = ['infi', 'infi.recipe'],

    package_dir = {'': 'src'},
    package_data = {'': []},
    include_package_data = True,
    zip_safe = False,

    entry_points = {
        'zc.buildout' : ['download = infi.recipe.python.download:Recipe',
                         'pack = infi.recipe.python.pack:Recipe',
                         'default = infi.recipe.python.download:Recipe']
    })

def setup():
    from setuptools import setup as _setup
    from setuptools import find_packages
    SETUP_INFO['packages'] = find_packages('src')
    _setup(**SETUP_INFO)

if __name__ == '__main__':
    setup()

