# setup.py

from setuptools import setup, find_packages

setup(
    name='dmengine',
    version='0.1.1',
    author='Sebastian Bank',
    author_email='sebastian.bank@uni-leipzig.de',
    description='Distributed Morphology calculator',
    keywords='DM Halle Marantz impoverishment fission linguistics',
    license='MIT',
    url='http://github.com/xflr6/dmengine',
    packages=find_packages(),
    package_data={'dmengine': ['reporting/template.tex']},
    entry_points={'console_scripts': ['dmengine=dmengine.__main__:main']},
    install_requires=[
        'oset',
        'PyYAML',
    ],
    extras_require={
        'test': ['nose', 'coverage', 'flake8', 'pep8-naming'],
        'dev': ['wheel'],
    },
    platforms='any',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
