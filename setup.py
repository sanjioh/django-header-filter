from setuptools import find_packages, setup

setup(
    name='django-header-filter',
    version='0.0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    zip_safe=False,
    install_requires=[
        'Django>=1.8,<1.11',
    ]
)
