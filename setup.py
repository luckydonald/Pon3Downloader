# -*- coding: utf-8 -*-
__author__ = 'luckydonald'

from setuptools import setup, find_packages
from Pon3Downloader import VERSION

long_description = """Downloads Music from pony.fm and eqbeat.org, filling in all the advanced ID3 meta tags, like lyrics and cover art."""
main_package = 'Pon3Downloader'
packages = [main_package, 'pon3down']
for package in find_packages(where='Pon3Downloader'):
	packages.append(main_package + "." + package)
# http://peterdowns.com/posts/first-time-with-pypi.html
# $ python setup.py register -r pypi
# $ python setup.py sdist upload -r pypi

setup(
	name="pon3downloader",
	packages=packages,
	version=VERSION,
	author="luckydonald",
	author_email="code@luckydonald.de",
	description=long_description,
	license="GPLv3+",
	keywords="download, music, ponies, DJ Pon3, pony.fm, eqbeats.org, Equestrian Beats, mp3, cover art images, "
			 "lyrics, ID3, pony, littlepip is best pony",
	url="https://github.com/luckydonald/pon3downloader/",
	install_requires=["DictObject", "requests", "eyeD3", "python-magic", "luckydonald-utils", 'usersettings',
					  'beautifulsoup4'],
	long_description=long_description,
	classifiers=[
		"Development Status :: 4 - Beta",
		"Intended Audience :: End Users/Desktop",
		"Topic :: Utilities",
		"Topic :: Internet",
		"Topic :: Internet :: WWW/HTTP",
		"Topic :: Multimedia",
		"Topic :: Multimedia :: Sound/Audio",
		"Topic :: Multimedia :: Sound/Audio :: Capture/Recording",
		"Topic :: System :: Archiving",
		"Programming Language :: Python",
		"Programming Language :: Python :: 2",
		"Programming Language :: Python :: 2.7",
		"License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
	],
	entry_points={
    'console_scripts': [
		'pon3music = Pon3Downloader.main:main',
		'pon3down = pon3down.main:main',
	]},
)
