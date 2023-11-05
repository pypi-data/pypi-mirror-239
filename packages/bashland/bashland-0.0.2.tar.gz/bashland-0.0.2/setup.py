from setuptools import setup, find_packages

setup(
    name='bashland',
    version='0.0.2',
    description='A demo Python package',
    author='bashland',
    author_email='bash.land@hotmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={
          'console_scripts': ['bl=bashland.bl:main',
                              'bashland=bashland.bh:main']
    },
)