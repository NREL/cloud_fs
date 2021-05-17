# -*- coding: utf-8 -*-
"""
OS file system utilities
"""
import glob
import os
import shutil


class FauxOpen:
    """
    Class to mimic context handling on open as needed for cloud based files
    """
    # pylint: disable=unused-argument
    def __init__(self, path, mode='r', **kwargs):
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


class OS:
    """
    S3 file system utilities
    """
    def __init__(self, path):
        """
        Parameters
        ----------
        path : str
            File path
        """
        self._path = path

    def cp(self, dst, **kwargs):
        """
        Copy file to given destination

        Parameters
        ----------
        dst : str
            Destination path
        kwargs : dict
            kwargs for shutil.copy

        Returns
        -------
        str
        """
        return shutil.copy(self._path, dst, **kwargs)

    def exists(self):
        """
        Check if file path exists

        Returns
        -------
        bool
        """
        return os.path.exists(self._path)

    def isfile(self):
        """
        Check if path is a file

        Returns
        -------
        bool
        """
        return os.path.isfile(self._path)

    def isdir(self):
        """
        Check if path is a directory

        Returns
        -------
        bool
        """
        return os.path.isdir(self._path)

    def glob(self, **kwargs):
        """
        Find all file paths matching the given pattern

        Parameters
        ----------
        kwargs : dict
            kwargs for glob.glob

        Returns
        -------
        list
        """
        return glob.glob(self._path, **kwargs)

    def ls(self):
        """
        List everyting under given path

        Returns
        -------
        list
        """
        return os.listdir(self._path)

    def mkdirs(self, **kwargs):
        """
        Make desired directory and any intermediate directories

        Parameters
        ----------
        kwargs : dict
            kwargs for os.makedirs

        Returns
        -------
        str
        """
        return os.makedirs(self._path, **kwargs)

    def mv(self, dst, **kwargs):
        """
        Move file or all files in directory to given destination

        Parameters
        ----------
        dst : str
            Destination path
        kwargs : dict
            kwargs for shutil.move

        Returns
        -------
        str
        """
        return shutil.move(self._path, dst, **kwargs)

    def open(self, mode='r', **kwargs):
        """
        Faux context manager to mimic cloud open operation

        Parameters
        ----------
        mode : str
            mode placeholder
        kwargs : dict
            placeholder

        Returns
        -------
        Return a file path
        """
        return FauxOpen(self._path, mode=mode, **kwargs)

    def rm(self, **kwargs):
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
        if os.path.isfile(self._path):
            return os.remove(self._path)
        else:
            return shutil.rmtree(self._path, **kwargs)

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
        return os.walk(self._path)
