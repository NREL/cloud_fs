# -*- coding: utf-8 -*-
"""
Utilities to abstractly handle filesystem operations
"""
from .filesystems import OS, S3


class FileSystem:
    """
    Class to abstract file location and allow file-system commands that are
    """
    def __init__(self, path, anon=False, profile=None, **kwargs):
        """
        Parameters
        ----------
        path : str
            S3 object path or file path
        anon : bool, optional
            Whether to use anonymous credentials, by default False
        profile : str, optional
            AWS credentials profile, by default None
        """
        self._path = path
        if path.startswith('s3:'):
            self._fs = S3(path, anon=anon, profile=profile, **kwargs)
        else:
            self._fs = OS(path)

    def __repr__(self):
        msg = ("{} operations on {}"
               .format(self.__class__.__name__, self.path))

        return msg

    def path(self):
        """
        File path to perform filesystem operation on

        Returns
        -------
        str
        """
        return self._path

    def cp(self, dst, **kwargs):
        """
        Copy file to given destination

        Parameters
        ----------
        dst : str
            Destination path
        kwargs : dict
            kwargs for s3fs.S3FileSystem.copy

        Returns
        -------
        str
        """
        return self._fs['cp'](self.path, dst, **kwargs)

    def exists(self):
        """
        Check if file path exists

        Returns
        -------
        bool
        """
        return self._fs['exists'](self.path)

    def isfile(self):
        """
        Check if path is a file

        Returns
        -------
        bool
        """
        return self._fs['isfile'](self.path)

    def isdir(self):
        """
        Check if path is a directory

        Returns
        -------
        bool
        """
        return self._fs['isdir'](self.path)

    def glob(self, **kwargs):
        """
        Find all file paths matching the given pattern

        Parameters
        ----------
        kwargs : dict
            kwargs for s3fs.S3FileSystem.glob

        Returns
        -------
        list
        """
        return self._fs['glob'](self.path, **kwargs)

    def ls(self):
        """
        List everyting under given path

        Returns
        -------
        list
        """
        return self._fs['ls'](self.path)

    def mkdirs(self, **kwargs):
        """
        Make desired directory and any intermediate directories

        Parameters
        ----------
        kwargs : dict
            kwargs for s3fs.S3FileSystem.mkdirs

        Returns
        -------
        str
        """
        return self._fs['mkdirs'](self.path, **kwargs)

    def mv(self, dst, **kwargs):
        """
        Move file or all files in directory to given destination

        Parameters
        ----------
        dst : str
            Destination path
        kwargs : dict
            kwargs for s3fs.S3FileSystem.mv

        Returns
        -------
        str
        """
        return self._fs['mv'](self.path, dst, **kwargs)

    def open(self, mode='r', **kwargs):
        """
        Open S3 object and return a file-like object

        Parameters
        ----------
        mode : str
            Mode with which to open the s3 object
        kwargs : dict
            kwargs for s3fs.S3FileSystem.open

        Returns
        -------
        Return a file-like object from the filesystem
        """
        return self._fs['open'](self.path, mode=mode, **kwargs)

    def rm(self, **kwargs):
        """
        Delete file or files in given directory

        Parameters
        ----------
        kwargs : dict
            kwargs for s3fs.S3FileSystem.rm

        Returns
        -------
        str
        """
        return self._fs['rm'](self.path, **kwargs)

    def walk(self):
        """
        Recursively search directory and all sub-directories

        Returns
        -------
        path : str
            Root path
        directory : list
            All directories in path
        file : list
            All files in path
        """
        return self._fs['walk'](self.path)
