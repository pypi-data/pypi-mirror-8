from setuptools import setup

import os
if 'vagrant' in str(os.environ):
    del os.link

setup(
    name='django-markdownx',
    version='0.1.0',
    description='Simple markdown editor (with live preview and images uploads) built for Django',
    url='https://github.com/adi-/django-markdownx',
    author='Adrian Drzewicki',
    author_email='adrian@enove.pl',
    license='BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development',
        'Topic :: Software Development :: User Interfaces',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: JavaScript',
    ],
    keywords='django markdown images upload jquery',
    install_requires=['Pillow==2.6.1'],
)
