# -*- coding: utf-8 -*-
"""
Utilities to abstractly handle filesystem operations
"""
from .os_fs import OS
from .s3_fs import S3


class FileSystem:
    """
    Class to abstract file location and allow file-system commands that are
    """
    def __init__(self, path, anon=False, profile=None, **kwargs):
        self._path = path
        if path.startswith('s3:'):
            self._fs = S3(path, anon=anon, profile=profile, **kwargs)
        else:
            self._fs = OS(path)

    def cp(self, dst, **kwargs):
        """
        [summary]

        Parameters
        ----------
        src : [type]
            [description]
        dst : [type]
            [description]

        Returns
        -------
        [type]
            [description]
        """
        return self._fs.cp(self._path, dst, **kwargs)

    def exists(self):
        """
        [summary]

        Returns
        -------
        [type]
            [description]
        """
        return self._fs.exists(self._path)

    def isfile(self):
        """
        [summary]

        Returns
        -------
        [type]
            [description]
        """
        return self._fs.isfile(self._path)

    def isdir(self):
        """
        [summary]

        Returns
        -------
        [type]
            [description]
        """
        return self._fs.isdir(self._path)

    def glob(self, **kwargs):
        """
        [summary]

        Returns
        -------
        [type]
            [description]
        """
        return self._fs.glob(self._path, **kwargs)

    def ls(self):
        """
        [summary]

        Returns
        -------
        [type]
            [description]
        """
        return self._fs.ls(self._path)

    def mkdirs(self, **kwargs):
        """
        [summary]

        Returns
        -------
        [type]
            [description]
        """
        return self._fs.mkdirs(self._path, **kwargs)

    def mv(self, dst, **kwargs):
        """
        [summary]

        Parameters
        ----------
        dst : [type]
            [description]

        Returns
        -------
        [type]
            [description]
        """
        return self._fs.mv(self._path, dst, **kwargs)

    def open(self, mode, **kwargs):
        """
        [summary]

        Parameters
        ----------
        mode : [type]
            [description]

        Returns
        -------
        [type]
            [description]
        """
        return self._fs.open(self._path, mode=mode, **kwargs)

    def rm(self, **kwargs):
        """
        [summary]

        Returns
        -------
        [type]
            [description]
        """
        return self._fs.rm(self._path, **kwargs)

    def walk(self):
        """
        [summary]

        Returns
        -------
        [type]
            [description]
        """
        return self._fs.walk(self._path)
