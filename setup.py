from distutils.core import setup
import msgraph

print(vars(msgraph))
setup(
    name='msgraph',
    version=msgraph.__version__,
    description='Python Wrapper to the Microsoft Graph API',
    author='Doug Fenstermacher',
    author_email='dpfens@wm.edu',
    url='https://code.wm.edu/IT/software-systems/eispippackages/msgraph',
    packages=['msgraph'],
    keywords=['microsoft', 'graph', 'api', 'calendar', 'event'],
    license='',
    install_requires=['adal>=1.2.2', 'requests>=2.12.0']
)
