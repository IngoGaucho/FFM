import os
import re
from   rsclib.HTML_Parse  import tag, Page_Tree
from   rsclib.stateparser import Parser
from   rsclib.autosuper   import autosuper
from   rsclib.IP_Address  import IP4_Address

def is_rfc1918 (ip) :
    networks = \
        [IP4_Address (x)
         for x in ('10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16')
        ]
    ip = IP4_Address (ip)
    for n in networks :
        if ip in n :
            return True
    return False
# end def is_rfc1918

class Guess (Page_Tree) :
    site  = 'http://%(ip)s/'
    url   = ''
    delay = 0

    status_url = 'cgi-bin-status.html'

    def parse (self) :
        #print self.tree_as_string ()
        root = self.tree.getroot ()
        for meta in root.findall (".//%s" % tag ("meta")) :
            if meta.get ('http-equiv') == 'refresh' :
                c = meta.get ('content')
                if c and c.endswith ('cgi-bin/luci') :
                    self.status  = Backfire (site = self.site)
                    self.version = self.status.version
                    break
        else : # Freifunk
            for sm in root.findall (".//%s" % tag ("small")) :
                if sm.text.startswith ('v1') :
                    self.version = sm.text
                    break
            else :
                self.version = "Unknown"
            #print "Version: %s" % self.version
            for a in root.findall (".//%s" % tag ("a")) :
                if a.get ('class') == 'plugin' and a.text == 'Status' :
                    self.status_url = a.get ('href')
            self.status = Freifunk (site = self.site, url = self.status_url)
        self.type = self.status.__class__.__name__
    # end def parse

    def __getattr__ (self, name) :
        r = getattr (self.status, name)
        setattr (self, name, r)
        return r
    # end def __getattr__

# end class Guess

class Net_Link (autosuper) :
    """Physical layer link interface
    """

    def __init__ (self, linktype, mac, bcast) :
        self.linktype = linktype
        self.mac      = mac
        self.bcast    = bcast
    # end def __init__

    def __str__ (self) :
        return "Net_Link (%(linktype)s, %(mac)s, %(bcast)s)" % self.__dict__
    # end def __str__
    __repr__ = __str__

# end class Net_Link

class Inet (autosuper) :
    """IP Network address
    """

    def __init__ (self, ip, netmask, scope = None, iface = None) :
        self.ip      = ip
        self.netmask = netmask
        self.scope   = scope
        self.iface   = iface
        self.bcast   = None
    # end def __init__

    def __str__ (self) :
        return self.__class__.__name__ \
            + " (%(ip)s/%(netmask)s, %(bcast)s, %(scope)s)" % self.__dict__
    # end def __str__
    __repr__ = __str__

# end class Inet

class Inet4 (Inet) :

    def __init__ (self, ip, netmask, bcast, scope = None, iface = None) :
        self.__super.__init__ (ip, netmask, scope, iface)
        self.bcast = bcast
    # end def __init__

# end class Inet4

class Inet6 (Inet) :
    pass
# end class Inet6

class Interface (autosuper) :
    """Network interface
    """

    def __init__ (self, number, name, mtu, qdisc = None, qlen = None) :
        self.number = number
        self.name   = name
        self.mtu    = mtu
        self.qdisc  = qdisc
        self.qlen   = qlen
        self.link   = None
        self.inet4  = []
        self.inet6  = []
        self.is_wl  = None
    # end def __init__

    def append_inet4 (self, inet) :
        self.inet4.append (inet)
        assert inet.iface == self.name
        inet.iface = self
    # end def append_inet4

    def append_inet6 (self, inet) :
        self.inet6.append (inet)
        assert inet.iface is None
        inet.iface = self
    # end def append_inet6

    def __str__ (self) :
        r = []
        r.append \
            ( "Interface (%(name)s, %(number)s, is_wl=%(is_wl)s)"
            % self.__dict__
            )
        if self.link :
            r.append (str (self.link))
        for i in self.inet4 :
            r.append (str (i))
        for i in self.inet6 :
            r.append (str (i))
        return "\n    ".join (r)
    # end def __str__
    __repr__ = __str__

# end class Interface

class Interface_Config (Parser) :
    re_assign = re.compile (r'^([a-zA-Z0-9_]+)\s*=\s*([a-zA-Z0-9 ]*)$')
    re_brhead = re.compile (r'^bridge name.*$')
    re_bridge = re.compile (r'^(\S+)\s*(\S+)\s*(\S+)\s*(\S+)$')
    re_if     = re.compile \
        (r'^(\d+):\s*(\S+):\s*mtu\s*(\d+)\s*qdisc\s*(\S+)(?:qlen\s*(\d+))?')
    pt_mac    = r'((?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2})'
    re_link   = re.compile \
        (r'^\s*link/(\S+)(?:\s*(\S+)\s*brd\s*(\S+))?$' % locals ())
    pt_ip     = r'((?:\d{1,3}[.]){3}\d{1,3})'
    re_inet   = re.compile \
        ( r'^\s*inet\s+%(pt_ip)s/(\d+)\s+'
          r'(?:brd\s+%(pt_ip)s\s+)?scope\s+(\S+)\s+(\S+)$'
        % locals ()
        )
    pt_ip6    = r'([0-9a-fA-F:]+)'
    re_inet6  = re.compile \
        ( r'^\s*inet6\s+%(pt_ip6)s/(\d+)\s+scope\s+(\S+)$' % locals ())
    matrix = \
        [ ["init",   re_assign, "init",   "assign"]
        , ["init",   re_brhead, "bridge", None]
        , ["init",   re_if,     "iface",  "iface"]
        , ["init",   None,      "init",   None]
        , ["bridge", re_bridge, "bridge", "bridge"]
        , ["bridge", '',        "init",   None]
        , ["iface",  re_link,   "iface",  "link"]
        , ["iface",  re_inet,   "iface",  "inet"]
        , ["iface",  re_inet6,  "iface",  "inet6"]
        , ["iface",  None,      "init",   "pop"]
        ]

    def __init__ (self, **kw) :
        self.assignments = {}
        self.bridges     = []
        self.interfaces  = []
        self.if_by_name  = {}
        self.__super.__init__ (**kw)
    # end def __init__

    def assign (self, state, new_state, match) :
        self.assignments [match.group (1)] = match.group (2)
    # end def assign

    def bridge (self, state, new_state, match) :
        self.bridges.append (match.groups ())
    # end def bridge

    def iface (self, state, new_state, match) :
        self.interface = Interface (* match.groups ())
        self.interfaces.append (self.interface)
        self.if_by_name [self.interface.name] = self.interface
        self.push (state, new_state, match)
    # end def iface

    def link (self, state, new_state, match) :
        self.interface.link = Net_Link (* match.groups ())
    # end def link

    def inet (self, state, new_state, match) :
        self.interface.append_inet4 (Inet4 (* match.groups ()))
    # end def link

    def inet6 (self, state, new_state, match) :
        self.interface.append_inet6 (Inet6 (* match.groups ()))
    # end def link

    def __str__ (self) :
        r = []
        for k, v in self.assignments.iteritems () :
            r.append ("%(k)s = %(v)s" % locals ())
        for b in self.bridges :
            r.append ("Bridge: %s" % str (b))
        for i in self.interfaces :
            r.append (str (i))
        return '\n'.join (r)
    # end def __str__
    __repr__ = __str__

# end class Interface_Config

class Freifunk (Page_Tree) :
    url = 'cgi-bin-status.html'

    def parse (self) :
        #print self.tree_as_string ()
        root = self.tree.getroot ()
        for pre in root.findall (".//%s" % tag ("pre")) :
            if pre.get ('id') == 'ifconfig' :
                self.ifconfig = Interface_Config ()
                self.ifconfig.parse (pre.text.split ('\n'))
                #print pre.text
                self.if_by_name = {}
                self.ips        = {}
                for k, v in self.ifconfig.assignments.iteritems () :
                    v = v.strip ()
                    if not v :
                        continue
                    if k == 'lan_ifname' :
                        wlan = False
                    elif k == 'wan_ifname' :
                        wlan = False
                    elif k.startswith ('wl') and k.endswith ('_ifname') :
                        wlan = True
                    elif k == 'wifi_ifname' :
                        wlan = True
                    else :
                        continue
                    iface = self.ifconfig.if_by_name [v]
                    found = False
                    for ip4 in iface.inet4 :
                        if is_rfc1918 (ip4.ip) :
                            continue
                        found = True
                        self.ips [ip4] = True
                    if found :
                        self.if_by_name [iface.name] = iface
                break
        else :
            raise ValueError, "No interface config found"
    # end def parse

# end class Freifunk

class Backfire (Page_Tree) :
    url = 'cgi-bin/luci/freifunk/olsr/interfaces'

    def parse (self) :
        root = self.tree.getroot ()
        self.if_by_name = {}
        self.ips        = {}
        self.version    = "Unknown"
        self.luci_version = self.bf_version = None
        for div in root.findall (".//%s" % tag ("div")) :
            if div.get ('class') == 'footer' :
                for p in div.findall (".//%s" % tag ("p")) :
                    if  (   p.get ('class') == 'luci'
                        and len (p)
                        and p [0].tag == tag ("a")
                        ) :
                        a = p [0]
                        if a.text.startswith ("Powered by LuCI") :
                            t = a.text.split ('(', 1) [-1].rstrip (')')
                            self.luci_version = t
            if div.get ('class') == 'header_right' :
                self.bf_version = div.text
            if div.get ('id') == 'maincontent' and not self.if_by_name :
                tbl = div.find (".//%s" % tag ("table"))
                for n, tr in enumerate (tbl) :
                    if tr [0].tag == tag ('th') :
                        assert tr [0].text == 'Interface'
                        continue
                    name, status, mtu, wlan, ip, mask, bcast = \
                        (x.text for x in tr)
                    if name in self.if_by_name :
                        iface = self.if_by_name [name]
                    else :
                        iface = Interface (n, name, mtu)
                        iface.is_wl = wlan == 'Yes'
                    i4 = Inet4 (ip, mask, bcast, iface = name)
                    iface.append_inet4 (i4)
                    if not is_rfc1918 (i4.ip) :
                        self.if_by_name [name] = iface
                        self.ips [i4] = True
        if not self.if_by_name :
            raise ValueError, "No interface config found"
        if self.bf_version and self.luci_version :
            self.version = "%s / Luci %s" % (self.bf_version, self.luci_version)
    # end def parse

# end class Backfire

if __name__ == '__main__' :
    import sys
    # For testing we download the index page and cgi-bin-status.html
    # page into a directory named with the ip address
    ip   = '193.238.158.241'
    if len (sys.argv) > 1 :
        ip = sys.argv [1]
    site = Guess.site % locals ()
    site = 'file:///' + os.path.abspath (ip)
    url  = 'index.html'
    ff   = Guess (site = site, url = url)
    print "Type:    %s" % ff.type
    print "Version: %s" % ff.version
    for v in ff.if_by_name.itervalues () :
        print v
    for ip in ff.ips.iterkeys () :
        print ip