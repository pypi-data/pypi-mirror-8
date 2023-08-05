
SETUP_INFO = dict(
    name = 'infi.recipe.application_packager',
    version = '0.5.9',
    author = 'Arnon Yaari',
    author_email = 'arnony@infinidat.com',

    url = 'https://github.com/Infinidat/infi.recipe.application_packager',
    license = 'PSF',
    description = """buildout recipe for packaging projects as applications""",
    long_description = """buildout recipe for packaging projects are applications""",

    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Python Software Foundation License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    install_requires = ['Archive',
'git-py',
'infi.execute',
'infi.pypi_manager',
'infi.pyutils',
'infi.recipe.buildout_logging',
'infi.recipe.close_application',
'infi.recipe.console_scripts',
'infi.registry',
'lxml',
'pystick',
'setuptools',
'zc.buildout'],
    namespace_packages = ['infi', 'infi.recipe'],

    package_dir = {'': 'src'},
    package_data = {'': ['changelog.in',
'control.in',
'ez_setup.txt',
'main.c',
'md5sums.in',
'Microsoft.VC90.CRT.manifest-x64',
'Microsoft.VC90.CRT.manifest-x86',
'postinst.in',
'prerm.in',
'rpmspec.in',
'rules.in',
'SConstruct',
'setup.py.example',
'signtool.exe',
'silent_launcher-x64.exe',
'silent_launcher-x86.exe',
'template.wxs']},
    include_package_data = True,
    zip_safe = False,

    entry_points = {
        'console_scripts': [],
        'gui_scripts': [],
        'zc.buildout': [
                        'default = infi.recipe.application_packager.auto:Recipe',
                        'executable = infi.recipe.application_packager.embedded:Executable',
                        'static_library = infi.recipe.application_packager.embedded:StaticLibrary',
                        'msi = infi.recipe.application_packager.msi:Recipe',
                        'rpm = infi.recipe.application_packager.rpm:Recipe',
                        'deb = infi.recipe.application_packager.deb:Recipe',
                       ]
        },
    )

def setup():
    from setuptools import setup as _setup
    from setuptools import find_packages
    SETUP_INFO['packages'] = find_packages('src')
    _setup(**SETUP_INFO)

if __name__ == '__main__':
    setup()

