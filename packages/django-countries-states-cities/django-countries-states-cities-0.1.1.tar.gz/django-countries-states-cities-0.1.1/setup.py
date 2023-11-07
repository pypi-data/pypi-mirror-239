from setuptools import setup, find_packages
import codecs
import os


REQUIREMENTS = [
    "drf-yasg"
    "djangorestframework"
    "django-modeltranslation"
    "django-filter",
]


CLASSIFIERS = [
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname), encoding='utf-8').read()


setup(
    name='django-countries-states-cities',
    version='0.1.1',
    description='Countries States Cities models for Django',
    author='Sunwook Kim',
    author_email='sun@runners.im',
    url='https://github.com/runners-2022/django-countries-states-cities',
    packages=find_packages(exclude=['config', 'config']),
    install_requires=REQUIREMENTS,
    python_requires='>=3.6',
    zip_safe=False,
    long_description=read('README.rst'),
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="django cities countries regions postal codes geonames",
    classifiers=CLASSIFIERS,
)
