#!/usr/bin/env python
# encoding: utf-8

"""This extension provides support for clusters using Kerberos authentication.

Namely, it adds a new :class:`~hdfs.client.Client` subclass,
:class:`KerberosClient`, which handles authentication appropriately.

"""

from ..client import Client
from requests_kerberos import HTTPKerberosAuth, OPTIONAL


class KerberosClient(Client):

  """HDFS web client using Kerberos authentication.

  :param url: Hostname or IP address of HDFS namenode, prefixed with protocol,
    followed by WebHDFS port on namenode
  :param proxy: User to proxy as.
  :param root: Root path. Used to allow relative path parameters.

  """

  def __init__(self, url, proxy=None, root=None):
    super(KerberosClient, self).__init__(
      url,
      auth=HTTPKerberosAuth(OPTIONAL),
      proxy=proxy,
      root=root,
    )
