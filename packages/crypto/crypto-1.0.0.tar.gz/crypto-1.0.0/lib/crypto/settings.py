#!/usr/bin/env python
# encoding: utf-8

#------------------------------------------------------------------------------
# Application Name
#------------------------------------------------------------------------------
app_name = 'crypto'

#------------------------------------------------------------------------------
# Version Number
#------------------------------------------------------------------------------
major_version = "1"
minor_version = "0"
patch_version = "0"

#------------------------------------------------------------------------------
# Debug Flag (switch to False for production release code)
#------------------------------------------------------------------------------
debug = False

#------------------------------------------------------------------------------
# Usage String
#------------------------------------------------------------------------------
usage = """
Encrypt by explicit file path:
------------------------------
  crypto [file path] <file path...>


Encrypt all top level files in directory:
-----------------------------------------
  crypto [directory path] <directory path...>


Decrypt by explicit file path:
------------------------------
  decrypto [file path] <file path...>


Decrypt all top level encrypted files in directory:
---------------------------------------------------
  decrypto [directory path] <directory path...>

"""

#------------------------------------------------------------------------------
# Help String
#------------------------------------------------------------------------------
help = """
---------------------------------------
crypto
Simple symmetric GPG file encryption
Copyright 2014 Christopher Simpkins
MIT license
https://github.com/chrissimpkins/crypto
---------------------------------------

ABOUT
crypto provides a simple interface to symmetric Gnu Privacy Guard (gpg) encryption and decryption for one or more files.  gpg must be installed on your system in order to use the crypto and decrypto executables.

USAGE
  ENCRYPTION
    crypto [file path] <file path...>
    crypto [directory path] <directory path...>

  DECRYPTION
    decrypto [file path] <file path...>
    decrypto [directory path] <directory path...>

CRYPTO OPTION
   --armor | -a          Use a portable ASCII armored encryption format

DECRYPTO OPTIONS
   --overwrite | -o      Overwrite an existing file with the decrypted file
   --stdout    | -s      Print file contents to the standard output stream

OTHER OPTIONS
   --help | -h           Display crypto and decrypto help
   --usage               Display crypto and decrypto usage
   --version | -v        Display version number

DESCRIPTION
Use one or more explicit file path arguments to encrypt or decrypt the file(s).  crypto and decrypto will attempt to encrypt or decrypt (respectively) any explicit filepaths that you include irrespective of the file type.  Encrypted files are generated on the path '<original_filepath>.crypt'.  The original file is not modified or removed by crypto.

Use one or more directory arguments with the crypto executable to encrypt all files in the top level of each directory with the same passphrase. Previously encrypted files with a '.crypt' file type will not be generated again in a directory.  Remove them before you run the command if you intend to repeat encryption with a file.

Use one or more directory arguments with decrypto to decrypt all .crypt, .gpg, .asc, and .pgp files in the top level of each directory.

Encryption is performed with the AES256 cipher algorithm.  Decryption will take place with any cipher algorithm that your version of gpg supports.
"""
