# -*- coding: utf-8 -*-
"""
OS file system utilities
"""
import glob
import os
import shutil


class OS:
    """
    S3 file system utilities
    """
    def __init__(self, path):
        self._path = path

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
        return shutil.copy(self._path, dst, **kwargs)

    def exists(self):
        """
        [summary]

        Returns
        -------
        [type]
            [description]
        """
        return os.path.exists(self._path)

    def isfile(self):
        """
        [summary]

        Returns
        -------
        [type]
            [description]
        """
        return os.path.isfile(self._path)

    def isdir(self):
        """
        [summary]

        Returns
        -------
        [type]
            [description]
        """
        return os.path.isdir(self._path)

    def glob(self, **kwargs):
        """
        [summary]

        Returns
        -------
        [type]
            [description]
        """
        return glob.glob(self._path, **kwargs)

    def ls(self):
        """
        [summary]

        Returns
        -------
        [type]
            [description]
        """
        return os.listdir(self._path)

    def mkdirs(self):
        """
        [summary]

        Returns
        -------
        [type]
            [description]
        """
        return os.makedirs(self._path)

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
        return shutil.move(self._path, dst, **kwargs)

    # pylint: disable=unused-argument
    def open(self, **kwargs):
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
        return self._path

    def rm(self, **kwargs):
        """
        [summary]

        Returns
        -------
        [type]
            [description]
        """
        if os.path.isfile(self._path):
            return os.remove(self._path)
        else:
            return shutil.rmtree(self._path, **kwargs)

    def walk(self):
        """
        [summary]

        Returns
        -------
        [type]
            [description]
        """
        return os.walk(self._path)
