from setuptools import setup

setup(
	name = "coursera_offline",

	version = "1.0.1",

	author="Sanketh Mopuru",
	author_email="sanketh.mopuru@gmail.com",

	url='https://github.com/sanketh95/coursera-offline',
	license='GPLv3',

	package_data = {
	        # If any package contains *.txt or *.rst files, include them:
	        '': ['*.rst', '*.md', '*.txt'],
	    },

	description = 'Download Coursera videos for offline viewing',

	long_description=(
		open('README.rst').read()
	),

	install_requires=[
		"pyquery>=1.2.9",
		"python-crontab>=1.8.1",
		"docutils>=0.3"
	],

	keywords = "coursera offline download lecture lectures video videos",

	scripts=['coursera_offline.py']
	)