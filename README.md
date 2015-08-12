# Pon3Downloader
Downloads pony related music from [Pony.fm](https://pony.fm/) and [Equestrian Beats](https://eqbeats.org),
filling in all the ID3 meta tags,
like artist name, album title, genre, etc. (all the standard things)
but also adds the lyrics and cover art, which are rarely in the downloaded mp3 file.

----

Currently only supports pony.fm, and Equestrian Beats will probably not be implemented, as it is shutting down end of the year...  :(


#### Dependencies 
(install with pip)
- ```DictObject```
- ```requests```
- ```eyeD3```
- ```python-magic```

Needs python 2 (sadly, until ```eyeD3``` is upgraded to support Python 3, too)

#### Usage
Use from command line, launch ```Pon3Downloader/__init__.py``` with python 2
(later this will be ```python -m Pon3Downloader``` or something easy to use)


#### Todo
- Add Equestrian Beats (Eqbeats.org) is not yet implemented - also it will sadly shut down December :(
- Install script is missing for more pleasant usage as module
- Pony.fm is working fine
