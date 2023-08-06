from setuptools import setup

setup(
    name='LipidConverter',
    version='0.1.6',
    author='Per Larsson',
    author_email='larsson.r.per@gmail.com',
    packages=['lipid_conv'],
    package_data={'lipid_conv': ['berger/*.top',
                                 'charmm36/*.top',
                                 'gromos43a1-S3/*.top',
                                 'gromos53a6/*.top',
                                 'gromos54a7/*.top',
                                 'lipid11/*.top',
                                 'opls/*.top'],
                  '':['docs/usage.txt'],
                  },
    scripts=['bin/lipid_converter.py'],
    url='http://lipid-converter.appspot.com',
    license='LICENSE.txt',
    description='Useful descripton text',
    long_description=open('README.txt').read(),
    install_requires=['NumPy >= 1.6','NetworkX >= 1.9','python-gflags >= 1.8'],
)

