from setuptools import setup


setup(
    name='cloudwatch-to-graphite',
    description='Helper for pushing AWS CloudWatch metrics to Graphite',
    version='0.1.0',
    author='Chris Chang',
    author_email='c@crccheck.com',
    url='https://github.com/crccheck/cloudwatch-to-graphite',
    py_modules=['leadbutt'],
    entry_points={
        'console_scripts': [
            'leadbutt = leadbutt:main',
        ],
    },
    install_requires=[
        'boto',
        'PyYAML',
        'docopt',
    ],
    license='Apache License, Version 2.0',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)
