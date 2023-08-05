import codecs
from setuptools import setup, find_packages

with codecs.open('README.md', 'r', 'utf-8') as f:
    long_description = f.read()
    try:
        import markdown2
        long_description = markdown2.markdown(long_description)
    except ImportError:
        pass

setup(
    name = 'django-markdown2',
    version = '0.2.0',
    description = 'This is a simple app, which supplies a single template tag for markdown markup.',
    long_description = long_description,
    keywords = 'django apps utils',
    license = 'New BSD License',
    author = 'Alexander Artemenko',
    author_email = 'svetlyak.40wt@gmail.com',
    url = 'http://github.com/svetlyak40wt/django-markdown2/',
    install_requires = ['markdown2'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages = find_packages(),
    include_package_data = True,
)

