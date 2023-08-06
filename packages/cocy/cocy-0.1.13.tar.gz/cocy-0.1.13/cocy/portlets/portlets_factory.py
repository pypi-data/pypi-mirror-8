"""
..
   This file is part of the CoCy program.
   Copyright (C) 2012 Michael N. Lipp
   
   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.
   
   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.

.. codeauthor:: mnl
"""
from circuits.core.components import BaseComponent
from circuits.core.handlers import handler
from cocy.upnp.device_server import UPnPDeviceServer
from cocy.portlets.device_directory import UPnPDirectoryPortlet
from cocy.portlets.device_server import UPnPDeviceServerPortlet
from cocy.upnp.device_directory import UPnPDeviceDirectory

class PortletsFactory(BaseComponent):
    '''
    classdocs
    '''
    
    @handler("registered", channel="*")
    def _on_registered(self, c, m):
        if isinstance(c, UPnPDeviceDirectory):
            UPnPDirectoryPortlet(c).register(self)
        elif isinstance(c, UPnPDeviceServer):
            UPnPDeviceServerPortlet(c).register(self)

    