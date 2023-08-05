from setuptools import setup, find_packages
import os

version = '0.9.0'

setup(
    name='proso-apps',
    version=version,
    description='General library for applications in PROSO projects',
    author='Jan Papousek',
    author_email='jan.papousek@gmail.com',
    namespace_packages = ['proso', 'proso.django'],
    packages=[
        'proso_models',
        'proso_models.migrations',
        'proso_models.management',
        'proso_questions',
        'proso_questions.management',
        'proso_questions.migrations',
        'proso_common',
        'proso_common.templatetags',
        'proso_ab',
        'proso_ab.migrations',
        'proso_ab.management',
        'proso', 'proso.django', 'proso.models'],
    install_requires=[
        'Django>=1.6',
        'django-debug-toolbar>=1.1',
        'django-ipware>=0.0.8',
        'django-lazysignup>=0.12.2',
        'django-social-auth>=0.7.28',
        'Markdown>=2.4.1',
        'numpy>=1.8.2',
        'PIL>=1.1.7',
        'psycopg2>=2.5.4',
        'South>=0.8'
    ],
    license='Gnu GPL v3',
)
