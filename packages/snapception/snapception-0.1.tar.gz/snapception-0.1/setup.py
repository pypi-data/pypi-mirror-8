from setuptools import setup, find_packages

scripts = ['bin/snapception']

setup(name='snapception',
	  version='0.1',
	  author='Bradley Bain',
	  license='MIT',
	  packages=['snapception'],
	  install_requires=[
	  	'requests',
	  	'click',
	  	'mitmproxy'
	  ],
	  include_package_data=True,
	  entry_points={'console_scripts' : ['snapception=snapception.command_line:main']}
	  )
	 