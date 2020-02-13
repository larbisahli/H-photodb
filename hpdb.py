# using python 3.8
# -*- coding: utf-8 -*-

# Copyright 2020 Larbi Sahli

import os
import hashlib
import time

import pickledb

current_directory = os.path.dirname(os.path.realpath(__file__))
default_key = "37e1f5637615c8ab9474184a2970f4cd8814303f49e56deb6c31cb7a1c12655c"


def _hash_(dir_, reduce=True):
    return hashlib.sha256(dir_.encode()).hexdigest()[:(20 if reduce else 64)]


class _LocAuth:
    def __init__(self, dir_path, dir_name, auth_key):

        self._key = auth_key
        self.MetaData = os.path.join(f"{dir_path}", "Imagedb.db")
        self.db = pickledb.load(self.MetaData, True)

        if not os.path.isdir(os.path.join(f"{dir_path}", f"{dir_name}")):
            ''' Initialise the database for the first time'''
            self.db.lcreate("deleted_id")
            self.db.set("last_entry", "")
            self.db.set("total_images", "0")
            self.db.set("unauth_access", "0")
            self.db.set("auth_key", _hash_(self._key, False))

        if self.db.exists("auth_key") and \
                self.db.get("auth_key") == _hash_(self._key, False):

            ''' Access to database and the path authorised only for the key holder '''
            self.path = os.path.join(f"{dir_path}", f"{dir_name}")
            if not os.path.isdir(self.path):
                os.mkdir(self.path)

        else:

            try:
                ''' Count the unauthorised access '''
                self.db.set("unauth_access", str(int(self.db.get("unauth_access")) + 1))
            except Exception:
                pass
            raise TypeError(f"Unauthorised Access, the auth key {self._key}"
                            f" is not a valid key.")


class Imagedb(_LocAuth):

    def __init__(self, dir_path=current_directory, dir_name="Imagedb", auth_key=default_key):
        super().__init__(dir_path, dir_name, auth_key)

    def _directoriesManager(self, *, t, b, m, k):

        if not os.path.isdir(_t_ := os.path.join(f"{self.path}", _hash_(f"_Trillion_{t}"))):
            os.mkdir(_t_)
        if not os.path.isdir(_b_ := os.path.join(f"{self.path}", _hash_(f"_Trillion_{t}"),
                                                 _hash_(f"_Billion_{b}"))):
            os.mkdir(_b_)
        if not os.path.isdir(_m_ := os.path.join(f"{self.path}", _hash_(f"_Trillion_{t}"),
                                                 _hash_(f"_Billion_{b}"), _hash_(f"_Million_{m}"))):
            os.mkdir(_m_)
        if not os.path.isdir(_k_ := os.path.join(f"{self.path}", _hash_(f"_Trillion_{t}"),
                                                 _hash_(f"_Billion_{b}"), _hash_(f"_Million_{m}"),
                                                 _hash_(f"_Thousand_{k}"))):
            os.mkdir(_k_)
        return os.path.join(f"{self.path}", _hash_(f"_Trillion_{t}"), _hash_(f"_Billion_{b}"),
                            _hash_(f"_Million_{m}"), _hash_(f"_Thousand_{k}"))

    @staticmethod
    def _slice(_id):
        ''' Slice the string and get the image path hint and the file extension '''
        _list = [i for i in _id.split(':')]
        x = [int(v) for i, v in enumerate(_list) if i != 5 and i != 6]
        x.append(_list[5])
        if len(_list[6]) != 0:
            x.append(_list[6])

        return x

    @staticmethod
    def _path(*, t, b, m, k, c, f, db):
        path_id = f"{t}:{b}:{m}:{k}:{c}:{f}"
        db.set("last_entry", path_id)
        return path_id

    def getpath(self, path_id, name=None):
        ''' Return image location.
        Converting the image path_id (string ex: _1:1:1:1:2:png)
        into a valid image path the image location. '''

        if len(slice_ := self._slice(path_id)) == 7:
            t, b, m, k, c, f, name = slice_
        else:
            t, b, m, k, c, f = slice_

        img_path = os.path.join(f"{self.path}", _hash_(f"_Trillion_{t}"), _hash_(f"_Billion_{b}"),
                                _hash_(f"_Million_{m}"), _hash_(f"_Thousand_{k}"),
                                f"{name if name else '' }_{_hash_(str(c))}.{f}")
        return img_path

    def delete(self, path_id):
        ''' Delete image from directory and it's path id from database '''
        img = self.getpath(path_id)
        if not self.db.lexists("deleted_id", path_id) and os.path.isfile(img):
            self.db.ladd("deleted_id", path_id)
            self.db.set("total_images", str(int(self.db.get("total_images")) - 1))
            os.remove(img)
            return True
        else:
            return False

    def push(self, path, name=None):
        ''' Rename and push an image to a new directory and return the image path_id (string ex: 1:1:1:1:2:png)
            that you can store in a database as a reference to an image file path. '''
        _, f = os.path.splitext(path)
        f = f.split(".")[1]
        del_state = False
        if len(del_id := self.db.get("deleted_id")) != 0:
            t, b, m, k, c, _ = self._slice(del_id[0])
            del_state = True
        elif len((last_entry := self.db.get("last_entry"))) != 0:
            t, b, m, k, c, _ = self._slice(last_entry)
        else:
            t = b = m = k = c = 0

        path_id = f"{t}:{b}:{m}:{k}:{c}:{f}"  # in case del_state is True pass the path
        if not del_state:
            c += 1
            path_id = self._path(t=t, b=b, m=m, k=k, c=c, f=f, db=self.db)
            if c == 1001:
                path_id = self._path(t=t, b=b, m=m, k=(k + 1), c=1, f=f, db=self.db)
            if k == 1001:
                path_id = self._path(t=t, b=b, m=(m + 1), k=1, c=1, f=f, db=self.db)
            if m == 1001:
                path_id = self._path(t=t, b=(b + 1), m=1, k=1, c=1, f=f, db=self.db)
            if b == 1001:
                path_id = self._path(t=(t + 1), b=1, m=1, k=1, c=1, f=f, db=self.db)
            if t == 2:
                return False
        else:
            self.db.lremvalue("deleted_id", del_id[0])

        self.db.set("total_images", str(int(self.db.get("total_images")) + 1))
        self._directoriesManager(t=t, b=b, m=m, k=k)
        os.rename(path, self.getpath(path_id, name=name))

        return f"{path_id}:{name if name else '' }"

    def __len__(self):
        ''' Return the number on images in the directory '''
        return abs(int(self.db.get("total_images")))

    def unauth(self):
        ''' Return the number of unauthorised access'''
        return int(self.db.get("unauth_access"))
