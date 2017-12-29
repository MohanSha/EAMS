from setuptools import setup

setup(name='sha',
      version='1.0',
      description='Employee attendance management client',
      url='http://github.com/storborg/funniest',
      author='Mohan Sha',
      author_email='mohansha@outlook.com',
      license='MIT',
      install_requires=[
          'xlrd','xlsxwriter','pillow','python-ldap',
      ],
      zip_safe=False)