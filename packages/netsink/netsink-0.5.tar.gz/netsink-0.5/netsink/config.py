# Netsink - Network Sinkhole for Isolated Malware Analysis
# Copyright (C) 2013-2014 Steve Henderson
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from collections import namedtuple
from ConfigParser import ConfigParser
import os
from pkg_resources import DistributionNotFound, Requirement, ResourceManager

# path to conf files if package not installed
SOURCE_PATH = os.path.join(os.path.dirname(__file__), 'conf')
OVERRIDE_PATH = "/etc/netsink"

def parseints(val):
    """Given a string list of comma separated integers, returns the ints in order.
    Also handles range syntax such as 10-15.
    No Attempt is made to dedupe or re-sort the elements.
    @param val: String value to parse
    @return: Yielded ints parsed from the string
    @raise ValueError: Invalid token in string.
    """
    for x in val.split(','):
        if '-' in x:
            y, z = x.split('-')
            for i in range(int(y.strip()), int(z.strip()) + 1):
                yield i
        elif x.strip() != '':
            yield int(x.strip())
    
def installed_location(filename):
    """Returns the full path for the given installed file or None if not found.
    """
    try:
        return ResourceManager().resource_filename(Requirement.parse("netsink"), filename)
    except DistributionNotFound:
        return None
    
class Config:
    """Main config file parser for netsink.
    """
    def __init__(self, cfg='netsink.conf'):
        installed_path = installed_location(cfg) or 'notfound'
        parser = ConfigParser()
        parser.read([os.path.join(OVERRIDE_PATH),
                     installed_path,
                     os.path.join(SOURCE_PATH, cfg)])
        
        self.certfile = parser.get('netsink', 'certfile')
        self.keyfile = parser.get('netsink', 'keyfile')
        self.redirection = parser.get('netsink', 'redirection').lower() in ["yes", "true"]
        self.listeners = {}
        for x in parser.get('netsink', 'listeners').split(","):
            listener = namedtuple('listener', 'name ports module socktype config servers')
            listener.name = x.strip()
            listener.ports = list(parseints(parser.get(listener.name, 'ports')))
            listener.module = parser.get(listener.name, 'module')
            listener.socktype = parser.get(listener.name, 'socktype')
            listener.config = parser.get(listener.name, 'config')
            self.listeners[listener.name] = listener

class ModuleConfig:
    """Given a module config filename, will find/parse and make the
    ConfigParser instance availble as self.cfg
    """ 
    def __init__(self, cfg):
        installed_path = installed_location(cfg) or 'notfound'
        parser = ConfigParser()
        parser.read([os.path.join(OVERRIDE_PATH),
                     installed_path,
                     os.path.join(SOURCE_PATH, cfg)])
        self.cfg = parser
