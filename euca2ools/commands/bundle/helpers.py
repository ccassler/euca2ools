# Software License Agreement (BSD License)
#
# Copyright (c) 2013, Eucalyptus Systems, Inc.
# All rights reserved.
#
# Redistribution and use of this software in source and binary forms, with or
# without modification, are permitted provided that the following conditions
# are met:
#
#   Redistributions of source code must retain the above
#   copyright notice, this list of conditions and the
#   following disclaimer.
#
#   Redistributions in binary form must reproduce the above
#   copyright notice, this list of conditions and the
#   following disclaimer in the documentation and/or other
#   materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from euca2ools.commands.walrus.getobject import GetObject
from euca2ools.commands.walrus.listbucket import ListBucket
import os
import sys
from xml.dom import minidom


def get_manifest_parts(manifest, bucket=None):
    """Gets a list object containing the filenames of parts in the manifest.
    Returns a list of parts contained in the manifest.
    :param manifest: name of the local manifest file to parse.
    :param bucket: (optional) bucket name to append to the part key.
    """
    part_paths = []
    dom = minidom.parse(manifest)
    elem = dom.getElementsByTagName('manifest')[0]
    for tag in elem.getElementsByTagName('filename'):
        for node in tag.childNodes:
            if node.nodeType == node.TEXT_NODE:
                if bucket:
                    part_paths.append(os.path.join(bucket, node.data))
                else:
                    part_paths.append(node.data)
    return part_paths


def get_manifest_keys(bucket, prefix=None, **kwargs):
    """Gets the key names for manifests in the specified bucket with optional
    prefix.
    Returns list of manifest keys in the bucket.
    :param bucket: bucket to search for manifest keys.
    :param prefix: (optional) only return keys with this prefix.
    :param kwargs: (optional) extra options passed to ListBucket.
    """
    manifests = []
    kwargs.update(paths=[bucket])
    response = ListBucket(**kwargs).main()
    for item in response.get('Contents'):
        key = item.get('Key')
        if key.endswith('.manifest.xml'):
            if prefix:
                if key.startswith(prefix):
                    manifests.append(key)
            else:
                manifests.append(key)
    return manifests

def download_files(bucket, keys, directory, **kwargs):
    """Download manifests from a Walrus bucket to a local directory.
    :param bucket: The bucket to download manifests from.
    :param keys: keys of the files to download.
    :param directory: location to put downloaded manifests.
    :param kwargs: (optional) extra arguments passed to GetObject.
    """
    paths = [os.path.join(bucket, key) for key in keys]
    kwargs.update(paths=paths, opath=directory)
    GetObject(**kwargs).main()
