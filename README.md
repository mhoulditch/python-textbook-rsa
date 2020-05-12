# python-textbook-rsa
attempt to create and learn from textbook rsa following: <https://nostarch.com/crackingcodes>. This repo is for learning purposes only and is not meant to be secure against sidechannel attacks and etc...

## use the keygen
import the keygen inside python:
```
$ python
>>> import keygen
```
then create keys:
```
keygen.make_key_files('yourname', 2048)
```
where the first arg will be appended to the filename for the keypair, and the second is the keybits.

## use the cipher
import the cipher inside python:
 
```
$ python
>>> import public_key_cipher
```
encrypt and write a message:
```
>>> public_key_cipher.encrypt_and_write_to_file('yourfile_encrypted.txt', 'yourname_pubkey.txt', "hello world")
```
decrypt and read the message:
```
>>> public_key_cipher.read_from_file_and_decrypt('yourfile_encrypted.txt', 'yourname_privkey.txt')
```
