from setuptools import setup, find_packages
from os.path import join, dirname
import BotDr
from BotDr.BotDr import super_main


setup(
    name='BotDr',
    author='botfg76',
    author_email='botfgbartenevfgzero76@gmail.com',
    license='Apache License Version 2.0',
    url='https://github.com/botfg/BotDr',
    description='Birth date control',
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    version=BotDr.__version__,
    packages=find_packages(),
    install_requires=[
        'pysqlcipher3==1.0.3',
        'numpy==1.17.4',
        'pyAesCrypt==0.4.3'],
    entry_points={
        'console_scripts':
            ['BotDr = BotDr.BotDr:super_main']
        },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3 :: Only",
        "Environment :: Console",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Unix",
    ],
    zip_safe=False,
    include_package_data=True,
    python_requires='>=3.6',)