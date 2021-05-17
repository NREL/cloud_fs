# -*- coding: utf-8 -*-
"""
System specific filesystem utilities
"""
from abc import ABC
import glob
import os
import s3fs
import shutil


class FileSystemError(Exception):
    """
    Custom filesystem error
    """


class FauxOpen:
    """
    Class to mimic context handling on open as needed for cloud based files
    """
    # pylint: disable=unused-argument
    def __init__(self, path, mode='rb', **kwargs):
        """
        Parameters
        ----------
        path : str
            File path
        mode : str
            mode placeholder
        kwargs : dict
            placeholder
        """
        self.path = path

    def __enter__(self):
        return self.path

    def __exit__(self, type, value, traceback):
        if type is not None:
            raise


class BaseFileSystem(ABC):
    """
    Abstract Base class for handling filesystem operations
    """
    def __init__(self, path):
        """
        Parameters
        ----------
        path : str
            File path
        """
        self._path = path
        self._operations = {'cp': None,
                            'exists': None,
                            'isfile': None,
                            'isdir': None,
                            'glob': None,
                            'ls': None,
                            'mkdirs': None,
                            'mv': None,
                            'open': None,
                            'rm': None,
                            'walk': None}

    def __repr__(self):
        msg = ("{} filesystem operations on {}"
               .format(self.__class__.__name__, self.path))

        return msg

    def __contains__(self, key):
        return key in self.operations

    def __getitem__(self, operation):
        """
        Get filesystem specific operation function/method

        Parameters
        ----------
        operation : str
            Filesystem operation name

        Returns
        -------
        obj
        """
        if operation not in self:
            msg = ('{} is not a valid {} filesystem operation! Please select '
                   'one of:\n{}'
                   .format(operation, self.__class__.__name__,
                           self.operations))
            raise FileSystemError(msg)

        return self._operations[operation]

    @property
    def path(self):
        """
        File path to perform filesystem operation on

        Returns
        -------
        str
        """
        return self._path

    @property
    def operations(self):
        """
        Available filesystem operations

        Returns
        -------
        list
        """
        return sorted(self._operations)


class Local(BaseFileSystem):
    """
    Local filesystem utilities
    """
    def __init__(self, path):
        """
        Parameters
        ----------
        path : str
            File path
        """
        self._path = path
        self._operations = {'cp': self.cp,
                            'exists': os.path.exists,
                            'isfile': os.path.isfile,
                            'isdir': os.path.isdir,
                            'glob': glob.glob,
                            'ls': os.listdir,
                            'mkdirs': os.makedirs,
                            'mv': shutil.move,
                            'open': FauxOpen,
                            'rm': self.rm,
                            'walk': os.walk}

    @staticmethod
    def cp(src, dst, **kwargs):
        """
        Copy file or recursively copy directory at src to dst

        Parameters
        ----------
        src : path
            File or directory to copy
        dst : path
            Destination to copy file or directory too
        """
        if os.path.isfile(src):
            shutil.copy(src, dst, **kwargs)
        else:
            shutil.copytree(src, dst, **kwargs)

    @staticmethod
    def rm(path, **kwargs):
        """
        Delete file or files in given directory

        Parameters
        ----------
        kwargs : dict
            kwargs for shutil.rmtree

        Returns
        -------
        str
        """
        if os.path.isfile(path):
            os.remove(path)
        else:
            shutil.rmtree(path, **kwargs)


class S3(BaseFileSystem):
    """
    S3 filesystem utilities
    """
    def __init__(self, s3_path, anon=False, profile=None, **kwargs):
        """
        Parameters
        ----------
        s3_path : str
            S3 object path
        anon : bool, optional
            Whether to use anonymous credentials, by default False
        profile : str, optional
            AWS credentials profile, by default None
        """
        self._path = s3_path
        self._s3fs = s3fs.S3FileSystem(anon=anon, profile=profile,
                                       **kwargs)

        self._operations = {'cp': self._s3fs.copy,
                            'exists': self._s3fs.exists,
                            'isfile': self._s3fs.isfile,
                            'isdir': self._s3fs.isdir,
                            'glob': self._s3fs.glob,
                            'ls': self._s3fs.ls,
                            'mkdirs': self._s3fs.mkdirs,
                            'mv': self._s3fs.mv,
                            'open': self._s3fs.open,
                            'rm': self._s3fs.rm,
                            'walk': self._s3fs.walk}