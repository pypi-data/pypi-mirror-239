from setuptools import setup , find_packages
import os

k=find_packages()

reqs = os.popen('pipreqs requirements.txt').read().splitlines()

with open('README.md','r') as f:
    ld=f.read()

setup(
    name='passwordManager_jsv',
    version='0.0.2',
    packages=find_packages(),
    author='Sahaya Valan J',
    author_email='sahayavalanj1@gmail.com',
    description='',
    long_description=ld,
    long_description_content_type='markdown',
    install_requires=reqs,
    entry_points={
        'console_scripts':['pass_manager=passmanager_jsv.passwd_manager:main']
    }
    

)


