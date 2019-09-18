from distutils.core import setup

setup(
    name='msgraph',
    version='0.1',
    description='Python Wrapper to the Microsoft Graph API',
    author='Doug Fenstermacher',
    author_email='dpfens@wm.edu',
    url='https://code.wm.edu/IT/software-systems/eispippackages/msgraph',
    packages=['msgraph'],
    keywords=['microsoft', 'graph', 'api', 'calendar', 'event'],
    license='',
    install_requires=['adal>=1.2.2', 'requests>=2.21.0']
)
