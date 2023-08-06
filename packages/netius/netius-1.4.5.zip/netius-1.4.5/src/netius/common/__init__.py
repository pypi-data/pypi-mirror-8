#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Netius System
# Copyright (C) 2008-2014 Hive Solutions Lda.
#
# This file is part of Hive Netius System.
#
# Hive Netius System is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Netius System is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Netius System. If not, see <http://www.apache.org/licenses/>.

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

from . import asn
from . import calc
from . import dhcp
from . import dkim
from . import http
from . import mime
from . import parser
from . import pop
from . import rsa
from . import smtp
from . import socks
from . import structures
from . import torrent
from . import util
from . import ws

from .asn import *
from .calc import *
from .dhcp import *
from .dkim import *
from .http import *
from .mime import *
from .parser import *
from .pop import *
from .rsa import *
from .smtp import *
from .socks import *
from .structures import *
from .torrent import *
from .util import *
from .ws import *
