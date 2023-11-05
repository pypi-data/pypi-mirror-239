from setuptools import setup

setup(
    name='python3-sendtelesend',
    version='1.0.0',
    packages=['sender'],
    entry_points={
        'console_scripts': [
            'telesend=sender.sender:main'
        ]
    },
    requires=[
        'requests'
    ]
)