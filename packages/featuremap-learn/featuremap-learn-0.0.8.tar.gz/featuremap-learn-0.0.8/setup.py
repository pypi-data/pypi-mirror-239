#!/usr/bin/env python3
# -*- coding: utf-8 -*-



from setuptools import setup

#def readme():
#    with open('README.md') as readme_file:
#        return readme_file.read()

with open("README.md", "r") as fh:
    long_description = fh.read()
    
configuration = {
    'name' : 'featuremap-learn',
    'version': '0.0.8',
    'description' : 'FeatureMAP',
    'long_description' : long_description,
    'long_description_content_type' : "text/markdown",
    'classifiers' : [
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Programming Language :: C',
        'Programming Language :: Python',
        'Topic :: Software Development',
        'Topic :: Scientific/Engineering',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3.9',
    ],
    'keywords' : 'dimensionality reduction manifold feature',
    'url' : 'https://github.com/YYT1002/FeatureMAP',
    'maintainer' : 'Yang Yang',
    'maintainer_email' : 'yangyangnwpu@gmail.com',
    'license' : 'GPL',
    'packages' : ['featuremap'],
    'install_requires': ['numpy >= 1.13',
                         'scikit-learn >= 0.16',
                          'scipy >= 0.19',
                         'numba == 0.57.1'],
    # 'ext_modules' : [],
    # 'cmdclass' : {},
    # 'test_suite' : 'nose.collector',
    # 'tests_require' : ['nose'],
    # 'package_data' : {'densmap-learn' : ['densmap/trial_data.txt']}, 
    # 'include_package_data' : True, 
    # 'data_files' : (['densmap/trial_data.txt'])
    }

setup(**configuration)