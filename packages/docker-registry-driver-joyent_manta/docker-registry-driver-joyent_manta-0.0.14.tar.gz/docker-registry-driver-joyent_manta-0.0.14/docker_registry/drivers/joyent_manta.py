# -*- coding: utf-8 -*-
"""
docker_registry.drivers.manta
~~~~~~~~~~~~~~~~~~~~~~~~~~

This is a manta based driver.

"""

from docker_registry.core import driver
from docker_registry.core import exceptions
from docker_registry.core import lru

import base64
import hashlib
import os

from manta import PrivateKeySigner, MantaClient


class Storage(driver.Base):
    def __init__(self, path=None, config=None):
        self.config = config

        self.signer = PrivateKeySigner(key_id=config.key_id,
                                       priv_key=open(config.private_key).read())

        account = config.account

        if type(config.subuser) is str and len(config.subuser) > 0:
            account += '/' + config.subuser

        self.client = MantaClient(config.url, account, self.signer,
                                  disable_ssl_certificate_validation=config.insecure,
                                  cache_dir='/tmp')

        self.mkdirp(self.create_manta_path())

    def put_object(self, mpath, content=None, path=None, file=None,
                   content_length=None,
                   content_type="application/octet-stream",
                   durability_level=None):

        headers = {
            "Content-Type": content_type,
        }

        if type(self.config.role_tags) is str and len(self.config.subuser) > 0:
            headers["role-tag"] = self.config.role_tags
            headers["role"] = self.config.role_tags

        if durability_level:
            headers["x-durability-level"] = durability_level

        methods = [m for m in [content, path, file] if m is not None]
        if len(methods) != 1:
            raise self.client.errors.MantaError("exactly one of 'content', 'path' or "
                "'file' must be provided")
        if content is not None:
            pass
        elif path:
            f = open(path)
            try:
                content = f.read()
            finally:
                f.close()
        else:
            content = file.read()
        if not isinstance(content, bytes):
            raise self.client.errors.MantaError("'content' must be bytes, not unicode")

        headers["Content-Length"] = str(len(content))
        md5 = hashlib.md5(content)
        headers["Content-MD5"] = base64.b64encode(md5.digest())
        res, content = self.client._request(mpath, "PUT", body=content,
                                     headers=headers)
        if res["status"] != "204":
            raise self.client.errors.MantaAPIError(res, content)

    def put_directory(self, mdir):
        headers = {
            "Content-Type": "application/json; type=directory"
        }
        if type(self.config.role_tags) is str and len(self.config.subuser) > 0:
            headers["role-tag"] = self.config.role_tags
            headers["role"] = self.config.role_tags

        res, content = self.client._request(mdir, "PUT", headers=headers)
        if res["status"] != "204":
            raise self.client.errors.MantaAPIError(res, content)

    def mkdirp(self, mpath):

        if len(mpath) == 0:
            return

        defaultpath = self.create_manta_path().split('/')
        parts = mpath.split('/')[len(defaultpath)-1:]
        mpath = '/'.join(defaultpath[:-1])

        for part in parts:
            mpath += '/' + part
            self.put_directory(mpath)

    def create_manta_path(self, path=None):
        if path is None:
            return self.config.path % self.config.account
        return os.path.join(self.config.path % self.config.account, path)

    @lru.get
    def get_content(self, path):
        mpath = self.create_manta_path(path)

        try:
            return self.client.get_object(mpath)
        except Exception:
            raise exceptions.FileNotFoundError("File %s not found" % path)

    @lru.set
    def put_content(self, path, content):
        if not isinstance(content, bytes):
            content = bytes(content)

        mpath = self.create_manta_path(path)
        self.mkdirp(os.path.dirname(mpath))
        self.put_object(mpath, content=content, content_type='text/plain')

    def exists(self, path):
        mpath = self.create_manta_path(path)
        res, status = self.client._request(path=mpath, method='HEAD')
        return str(res.status) != '404'

    def stream_write(self, path, fp):
        mpath = self.create_manta_path(path)
        self.mkdirp(os.path.dirname(mpath))
        self.put_object(mpath, file=fp)

    def stream_read(self, path, bytes_range=None):
        mpath = self.create_manta_path(path)
        return self.client.get_object(mpath)

    def list_directory(self, path):
        mpath = self.create_manta_path(path)
        try:
            entries = self.client.list_directory(mpath)
        except Exception:
            raise exceptions.FileNotFoundError("File %s not found" % path)

        files = []
        for fileObj in entries:
            files.append(os.path.join(path, fileObj['name']))

        return files

    @lru.remove
    def remove(self, path):
        mpath = self.create_manta_path(path)
        self.client.delete_object(mpath)

    def content_redirect_url(self, path):
        return self.config.url + path
