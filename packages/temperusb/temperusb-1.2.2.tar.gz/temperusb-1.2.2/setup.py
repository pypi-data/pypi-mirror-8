from setuptools import setup

setup(
    name='temperusb',
    author='Philipp Adelt',
    author_email='autosort-github@philipp.adelt.net ',
    url='https://github.com/padelt/temper-python',
    version='1.2.2',
    description='Reads temperature from TEMPerV1 devices (USB 0c45:7401)',
    long_description=open('README.md').read(),
    packages=['temperusb'],
    install_requires=[
        'pyusb>=1.0.0b2',
    ],
    entry_points={
        'console_scripts': [
            'temper-poll = temperusb.cli:main',
            'temper-snmp = temperusb.snmp:main'
        ]
    }
)
