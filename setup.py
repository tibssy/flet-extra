from setuptools import setup, find_packages

setup(
    name='flet_extra',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    package_data={'flet_extra': ['*.png']},
    install_requires=[
        'flet'
    ],
)
