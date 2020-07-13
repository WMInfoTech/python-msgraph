from setuptools import setup
import msgraph

description = 'Python wrapper to the Microsoft Graph API'
with open('README.md', 'r') as input_file:
    long_description = input_file.read()

setup(
    name='python-msgraph',
    version=msgraph.__version__,
    long_description_content_type='text/markdown',
    long_description=long_description,
    description='Python wrapper to the Microsoft Graph API',
    author='Doug Fenstermacher',
    author_email='dpfens@wm.edu',
    url='https://github.com/WMInfoTech/python-msgraph',
    packages=['msgraph'],
    keywords='microsoft, graph, api, group, calendar, event, site, list, listitem, drive, file',
    license='Apache2',
    project_urls={
        'Source': 'https://github.com/WMInfoTech/python-msgraph',
        'Tracker': 'https://github.com/WMInfoTech/python-msgraph/issues'
    },
    install_requires=['adal>=1.2.2', 'requests>=2.12.0'],
    options={
        'bdist_wheel': {
            'universal': True
        }
    }
)
