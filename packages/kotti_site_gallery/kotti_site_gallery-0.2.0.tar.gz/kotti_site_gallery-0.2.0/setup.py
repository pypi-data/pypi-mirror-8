import os
from setuptools import find_packages
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

development_requires = ['minify', ]
install_requires = [
    'Kotti >= 0.10b1',
]

setup(
    name='kotti_site_gallery',
    version='0.2.0',
    description="Site gallery for Kotti sites",
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "License :: OSI Approved :: BSD License",
    ],
    keywords='kotti site gallery',
    author='Kotti developers',
    author_email='kotti@googlegroups.com',
    url='http://pypi.python.org/pypi/kotti_site_gallery',
    license='BSD-2-Clause',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    extras_require={'development': development_requires, },
    entry_points={
        'fanstatic.libraries': [
            'kotti_site_gallery = kotti_site_gallery:lib_kotti_site_gallery',
        ],
    },
)
