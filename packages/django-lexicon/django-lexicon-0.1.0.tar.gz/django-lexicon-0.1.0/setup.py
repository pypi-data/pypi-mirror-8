from setuptools import setup, find_packages

kwargs = {
    # Packages
    'packages': find_packages(exclude=[
        'tests',
        '*.tests',
        '*.tests.*',
        'tests.*',
    ]),
    'include_package_data': True,

    # Dependencies
    'install_requires': [
        'django>=1.4',
    ],

    'tests_require': [
        'avocado',
        'python-memcached',
    ],

    'test_suite': 'test_suite',

    # Metadata
    'name': 'django-lexicon',
    'version': __import__('lexicon').get_version(),
    'author': 'Byron Ruth',
    'author_email': 'b@devel.io',
    'description': 'Abstract classes for defining a lexicon',
    'license': 'BSD',
    'keywords': 'lexicon',
    'url': 'http://cbmi.github.io/django-lexicon/',
    'classifiers': [
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Framework :: Django',
        'Topic :: Internet :: WWW/HTTP',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Information Technology',
    ],
}

setup(**kwargs)
