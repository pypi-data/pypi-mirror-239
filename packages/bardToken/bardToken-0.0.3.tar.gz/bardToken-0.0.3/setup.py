# coding:utf-8

#from setuptools import setup
from setuptools import setup, Extension
# or
#from distutils.core import setup  
with open('README.md',encoding='utf-8') as f:
    long_description = f.read()

setup(
        name='bardToken',   
        version='0.0.3',   
        description='auto login google account by selenium chrome driver ',#long_description=foruser,
        long_description=long_description,
        long_description_content_type='text/markdown',
        author='KuoYuan Li',  
        author_email='funny4875@gmail.com',  
        url='https://pypi.org/project/bardToken',      
        packages=['bardToken'],   
        include_package_data=True,
        keywords = ['bardToken','auto bard token','bard api','selenium', 'google auth' , 'chromedriver'],   # Keywords that define your package best
          install_requires=[            
          'seleniumGoogleLogin'
          ],
      classifiers=[
        'License :: OSI Approved :: MIT License',   
        'Programming Language :: Python :: 3',
      ]
)
