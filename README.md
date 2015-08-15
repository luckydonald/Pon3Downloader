# Pon3Downloader
Downloads pony related music from [Pony.fm](https://pony.fm/),
filling in all missing tags ID3 meta tags (like song title, album name, genre, etc.)
but also adds the advanced tags like lyrics and cover art, which are rarely found in the downloaded mp3 files.

----

Currently Supports pony.fm
### Install
```sh
pip install pon3downloader
```
    
If you prefer to install it manually from source, grab the code and run:    
```
python setup.py install
```

#### Usage
```sh
# start to enter url interactively:    
python -m Pon3Downloader    
# supply an url directly:    
python -m Pon3Downloader <url>    
```
You can use you pony.fm (poniverse.net) login to update your personal stats, and advanced features like automatic fave'ing and/or automatic comments when downloading.
To not have to type your login credentials, you can stay logged-in, or store your login-password-combination.


#### Dependencies 
(installed automatically when installing using ```pip``` or ```setup.py```)    
- ```DictObject```    
- [```luckydonald-utils```](https://github.com/luckydonald/python-utils/)    
- ```requests```    
- ```eyeD3```    
- ```python-magic```    

Needs Python 2 (sadly, until ```eyeD3``` is upgraded to support Python 3, too)

#### Todo
- Add Equestrian Beats [eqbeats.org](https://eqbeats.org) - not yet implemented. It will sadly shut down December :(
- Add tests

#### Notes
Of course your password will be stored encrypted, but with access to your computer, it is decryptable.    
I am working on a keychain solution so the en-/decryption key is safe too. (maybe 1Password, Apple Keychain, or some linux built-in? Does Windows have something similar?)

[Equestrian Beats](https://eqbeats.org) will probably not be implemented, as they are  shutting down end of the year...  :(
