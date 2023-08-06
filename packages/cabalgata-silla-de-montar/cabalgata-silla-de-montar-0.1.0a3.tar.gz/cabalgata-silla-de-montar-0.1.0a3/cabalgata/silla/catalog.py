#
# Copyright 2014 the original author or authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
""" Catalog management functions
"""
import contextlib
import json
import logging
import os

from cabalgata import silla
from cabalgata.silla.util import disk


CATALOG_DIR = '.cabalgata'
CATALOG_FILE = 'catalog.json'

log = logging.getLogger(__name__)


class CorruptedCatalogError(Exception):
    """Error for corrupted catalog."""


class Catalog(object):
    def __init__(self, version):
        self.version = version

    def as_tuple(self):
        return self.version,

    def __eq__(self, other):
        return self.as_tuple() == other.as_tuple()

    def __repr__(self):
        return 'Catalog(%r)' % self.as_tuple()

    @classmethod
    def from_json(cls, json):
        return cls(json['version'])

    def to_json(self):
        return {
            'version': self.version
        }


def initialize(catalog_dir=None):
    catalog_dir = catalog_dir or os.path.join(os.path.abspath('~'), CATALOG_DIR)

    if not os.path.exists(catalog_dir):
        disk.make_directories(catalog_dir)
        with load_catalog(catalog_dir):
            pass


@contextlib.contextmanager
def load_catalog(catalog_dir):
    catalog_file = os.path.join(catalog_dir, CATALOG_FILE)
    if os.path.exists(catalog_file):
        try:
            with open(catalog_file) as fp:
                json_catalog = json.load(fp)
                catalog = Catalog.from_json(json_catalog)
        except Exception:
            log.exception('Unable to read %s' % catalog_file)
            raise CorruptedCatalogError('Unable to read %s' % catalog_file)
    else:
        catalog = Catalog(silla.VERSION)

    yield catalog

    try:
        json_catalog = catalog.to_json()
        with open(catalog_file, 'w') as fp:
            json.dump(json_catalog, fp)
    except Exception:
        log.exception('Unable to write %s' % catalog_file)
        raise CorruptedCatalogError('Unable to write %s' % catalog_file)
