# Pon3Downloader
Downloads Music from [Pony.fm](https://pony.fm/) and [Eqbeats](https://eqbeats.com),
filling in all the ID3 meta tags,
like artist name, album title, genere, etc. (all the standard things)
but also adds the lyrics and cover art, which are rarely in the mp3 file.

#### Dependencies: 
(install with pip)
- ```DictObject```
- ```requests```
- ```eyeD3```
- ```python-magic```

Needs python 2 (sadly, until ```eyeD3``` is upgraded to support Python 3, too)

#### Usage
Use from command line, launch ```Pon3Downloader/__init__.py```
(later this will be ```python -m Pon3Downloader```)
