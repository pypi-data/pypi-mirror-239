""" Cluster configuration """

import functools
import json
import logging
import pathlib
from typing import Optional

logger = logging.getLogger(__name__)


class CSClusterConfig:
    """ Connection information for a Cerebras cluster """

    CSCONFIG_PATH = pathlib.Path("/opt/cerebras/config")
    DEFAULT_MGMT_ADDRESS = "cluster-server.cerebrassc.local:443"
    DEFAULT_AUTHORITY = "cluster-server.cerebrassc.local"

    """ Usernode configuration from /opt/cerebras/config """

    def __init__(
            self, mgmt_address: str, authority: str, credentials_path: Optional[str] = None,
    ):
        self.mgmt_address = mgmt_address
        self.authority = authority
        self.credentials_path = credentials_path

    def __str__(self):
        return str(
            f"CSClusterConfig{{mgmt_address={self.mgmt_address},"
            f"authority={self.authority},credentials_path={self.credentials_path}}}")


def load_cs_cluster_config() -> CSClusterConfig:
    """
    Load a csconfig file installed by the usernode installer. This file contains
    the management address and credentials for the cluster.
    Returns:
        The CSConfig with mgmt address and credentials file if the file was
        loaded successfully, or None if no csconfig file is found.
    """
    default_instance = CSClusterConfig(
        mgmt_address=CSClusterConfig.DEFAULT_MGMT_ADDRESS,
        authority=CSClusterConfig.DEFAULT_AUTHORITY
    )

    if not CSClusterConfig.CSCONFIG_PATH.exists():
        logger.info(
            f"csconfig file not found: {CSClusterConfig.CSCONFIG_PATH}, "
            f"loading default fallback {default_instance}")
        return default_instance

    try:
        doc = json.loads(CSClusterConfig.CSCONFIG_PATH.read_text())
        ctx = doc["currentContext"]
        contexts = {c["name"]: c for c in doc["contexts"]}
        cluster_name = contexts[ctx]["cluster"]
        clusters = {c["name"]: c for c in doc["clusters"]}
        cluster = clusters[cluster_name]
        cfg = CSClusterConfig(
            mgmt_address=cluster["server"],
            authority=cluster["authority"],
            credentials_path=cluster["certificateAuthority"],
        )
        logger.debug(
            f"CSconfig loaded {CSClusterConfig.CSCONFIG_PATH}, "
            f"mgmtAddress={cfg.mgmt_address}, "
            f"authority={cfg.authority}, "
            f"credentialsPath={cfg.credentials_path}"
        )
        return cfg
    except Exception as e:  # pylint: disable=broad-except
        logger.warning(
            f"Failed to load csconfig {CSClusterConfig.CSCONFIG_PATH}: {e}. "
            f"Using default fallback {default_instance}")
    return default_instance


@functools.lru_cache()
def get_cs_cluster_config() -> CSClusterConfig:
    """
    Load a cached csconfig file installed by the usernode installer. This file
    contains the management address and credentials for the cluster.
    Returns:
        The CSConfig with mgmt address and credentials file if the file was
        loaded successfully, or None if no csconfig file is found.
    """
    return load_cs_cluster_config()
