#!/usr/bin/env python3

import hashlib
import os
import shutil

class File:
    '''A class reprensenting a file.

    Exposed members:
      - dir: str, the directory of the file,
      - file: str, the name and extension of the file,
      - hash: str, the hexadecimal MD5 hash of the file.

    hash is guaranteed to stay constant throughout renamings and copies.'''

    @staticmethod
    def GetHash(path):
        '''Get the hexadecimal MD5 hash of the file.'''
        with open(path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()

    def __init__(self, path):
        self.dir, self.file = os.path.split(path)
        self.hash = File.GetHash(path)

    def SafeCopy(self, topath):
        '''Copy this file to another location. Retry if hashes do not match.'''
        frompath = os.path.join(self.dir, self.file)
        if frompath == topath:
            return
        print("SafeCopy:", frompath, '→', topath)
        if os.path.isfile(topath):
            raise FileExistsError(topath)

        shutil.copy2(frompath, topath)
        tohash = File.GetHash(topath)
        while self.hash != tohash:
            print("SafeCopy:", frompath, '→', topath)
            shutil.copy2(frompath, topath)
            tohash = File.GetHash(topath)

    def SafeMove(self, topath):
        '''SafeCopy this file then delete original. This object is altered to
        represent the new file.'''
        self.SafeCopy(topath)
        self.Remove()
        self.dir, self.file = os.path.split(topath)

    def SafeRename(self, toname):
        '''SafeMove this file to a new name while keeping extension. This object
        is altered to represent the new file.'''
        _, ext = os.path.splitext(self.file)
        self.SafeMove(os.path.join(self.dir, toname + ext))

    def SafeSelfCopy(self, toname):
        '''SafeCopy this file to a new name while keeping extension.'''
        _, ext = os.path.splitext(self.file)
        self.SafeCopy(os.path.join(self.dir, toname + ext))

    def Remove(self):
        '''Remove that file.'''
        os.remove(os.path.join(self.dir, self.file))
