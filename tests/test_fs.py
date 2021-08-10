# -*- coding: utf-8 -*-
"""
pytests for FileSystem utilities
"""
import h5py
import numpy as np
import os
import pytest
from tempfile import TemporaryDirectory

from cloud_fs import FileSystem
from cloud_fs.filesystems import Local, S3


@pytest.mark.parametrize(('path', 'cls'),
                         [('/test/test', Local),
                          ('s3://test', S3)])
def test_fs_type(path, cls):
    """
    Ensure Filesystem picks the proper utility class
    """
    fs = FileSystem(path)
    msg = 'FileSystem handler class is not {}'.format(cls)
    assert isinstance(fs._fs, cls), msg


def test_Local_file():
    """
    Test Local filesystem file utilities
    """
    root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    with TemporaryDirectory() as td:
        src_dir = os.path.join(root, 'cloud_fs')
        src = os.path.join(src_dir, 'version.py')
        dst = td
        fs = FileSystem(src)
        fs.cp(dst)

        fs = FileSystem(dst)
        test = fs.ls()
        truth = sorted(os.path.join(dst, file) for file in os.listdir(dst))
        assert test == truth, "Destination files were not listed properly"

        truth = ['version.py']
        assert test == truth, "Source files don't match destination files"

        fs = FileSystem(os.path.join(dst, 'version.py'))
        with fs as faux:
            with open(faux, encoding="utf-8") as f:
                version = f.read()
                assert '__version__' in version

        fs.rm()
        assert not fs.exists(), 'Remove did not work!'
        assert not sorted(os.path.join(dst, file)
                          for file
                          in os.listdir(dst)), 'Destination is not empty'


def test_Local_dir():
    """
    Test Local filesystem directory utilities
    """
    root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    with TemporaryDirectory() as td:
        src = os.path.join(root, 'cloud_fs')
        dst = os.path.join(td, 'cloud_fs')
        fs = FileSystem(src)
        fs.cp(dst)

        test = fs.ls()
        truth = sorted(os.path.join(dst, file) for file in os.listdir(dst))
        assert test == truth, "Source files were not listed properly"

        fs = FileSystem(dst)
        test = fs.ls()
        truth = sorted(os.path.join(dst, file) for file in os.listdir(dst))
        assert test == truth, "Destination files were not listed properly"

        truth = sorted(os.path.join(dst, file) for file in os.listdir(dst))
        assert test == truth, "Source files don't match destination files"

        fs.rm()
        assert not fs.exists(), 'Destination is not empty!'


def test_S3():
    """
    Test S3 utilities
    """
    bucket = 's3://nrel-pds-nsrdb/v3'
    fs = FileSystem(bucket, anon=True)

    test = fs.ls()
    assert isinstance(test, list)

    s3_file = 's3://nrel-pds-nsrdb/v3/nsrdb_2000.h5'
    # pylint: disable=bad-str-strip-call
    assert s3_file.lstrip('s3://') in test
    with FileSystem(s3_file, anon=True) as s3_f:
        with h5py.File(s3_f, mode='r') as f:
            assert 'meta' in f, 'could not search nsrdb file on S3!'
            assert 'time_index' in f, 'could not search nsrdb file on S3!'

            ti = f['time_index'][...]
            assert isinstance(ti, np.ndarray), 'could not extract time_index'
