
import codecs
import os

from setuptools import setup


def read(*parts):
    return codecs.open(os.path.join(os.path.dirname(__file__), *parts),
                       encoding='utf8').read()

setup(
    name='django-revproxy',
    description='Yet another Django reverse proxy application.',
    version='0.3.0',
    long_description=read('README.rst'),
    packages=['revproxy'],
    tests_require=['mock', 'diazo'],
    test_suite="tests.run.runtests",
    author='Sergio Oliveira',
    author_email='sergio@tracy.com.br',
    url='https://github.com/TracyWebTech/django-revproxy',
    license='MPL v2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        ],
)
