"""
Salt execution module

Elasticsearch - A distributed RESTful search and analytics server for Elasticsearch 8
Module to provide Elasticsearch compatibility to Salt
(compatible with Elasticsearch version 8+).  Copied from elasticsearch.py module and updated.

.. versionadded:: 3005.1

:codeauthor: Cesar Sanchez <cesan3@gmail.com>

:depends: elasticsearch-py <http://elasticsearch-py.readthedocs.org/en/latest/>

:configuration: This module accepts connection configuration details either as
                parameters or as configuration settings in /etc/salt/minion on the relevant
                minions:

.. code-block:: yaml

    elasticsearch:
      host: '10.10.10.100:9200'

    elasticsearch-cluster:
      hosts:
        - '10.10.10.100:9200'
        - '10.10.10.101:9200'
        - '10.10.10.102:9200'

    elasticsearch-extra:
      hosts:
        - '10.10.10.100:9200'
      use_ssl: True
      verify_certs: True
      ca_certs: /path/to/custom_ca_bundle.pem
      number_of_shards: 1
      number_of_replicas: 0
      functions_blacklist:
        - 'saltutil.find_job'
        - 'pillar.items'
        - 'grains.items'

      proxies:
        - http: http://proxy:3128
        - https: http://proxy:1080

When specifying proxies the requests backend will be used and the 'proxies'
data structure is passed as-is to that module.

This data can also be passed into pillar. Options passed into opts will
overwrite options passed into pillar.

Some functionality might be limited by elasticsearch-py and Elasticsearch server versions.
"""
# pylint: disable=too-many-lines
import logging

log = logging.getLogger(__name__)

__salt__ = globals().get("__salt__", {})

try:
    import elasticsearch

    HAS_ELASTICSEARCH = True
except ImportError:
    HAS_ELASTICSEARCH = False
    ES_MAJOR_VERSION = 0

__virtualname__ = "elasticsearch"

if HAS_ELASTICSEARCH:
    ES_MAJOR_VERSION = elasticsearch.__version__[0]
    logging.getLogger("elasticsearch").setLevel(logging.CRITICAL)
    profile = __salt__.get("config.option", {}).get("elasticsearch")
    if ES_MAJOR_VERSION >= 8:
        from . import es_module_8
        ESModule = es_module_8.ESModule8(elasticsearch)
        ESModule.set_profile(profile)
        ESModule.set_salt_globals(__salt__)
    else:
        from . import es_module_6
        ESModule = es_module_6.ESModule6(elasticsearch)
        ESModule.set_profile(profile)
        ESModule.set_salt_globals(__salt__)

else:
    ESModule = None


def __virtual__():
    """
    Only load if elasticsearch librarielastic exist and ES version is 8+.
    """
    if not HAS_ELASTICSEARCH:
        return (
            False,
            "Cannot load module elasticsearch: elasticsearch librarielastic not found",
        )

def __getattr__(name):
    """
    Redirect function calls to ESModule
    """
    if ESModule is not None:
        return getattr(ESModule, name)
