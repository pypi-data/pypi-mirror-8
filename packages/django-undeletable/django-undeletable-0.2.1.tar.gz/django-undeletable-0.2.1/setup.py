# coding=utf-8
from distutils.core import setup

setup(
    name='django-undeletable',
    packages=['django_undeletable'],  # this must be the same as the name above
    version='0.2.1',
    description='Deleted data stays in the database and will be hidden from the default manager.',
    author='Andy Grabow',
    author_email='andy@freilandkiwis.de',
    url='https://github.com/kakulukia/django-undeletable',  # use the URL to the github repo
    download_url='https://github.com/kakulukia/django-undeletable/tarball/0.2.1',  # I'll explain this in a second
    keywords=['orm', 'undelete', 'shadow db'],  # arbitrary keywords
    classifiers=[],
    install_requires=['Django>=1.6'],
    license="MIT",
)
