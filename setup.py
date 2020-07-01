from setuptools import setup
import msgraph

setup(
    name='python-msgraph',
    version=msgraph.__version__,
    description='Python wrapper to the Microsoft Graph API',
    author='Doug Fenstermacher',
    author_email='dpfens@wm.edu',
    url='https://github.com/WMInfoTech/python-msgraph',
    packages=['msgraph'],
    keywords='microsoft graph api group calendar event site list listitem drive file',
    license='MIT',
    project_urls={
        'Source': 'https://github.com/WMInfoTech/python-msgraph',
        'Tracker': 'https://github.com/WMInfoTech/python-msgraph/issues'
    },
    install_requires=['adal>=1.2.2', 'requests>=2.12.0']
)
