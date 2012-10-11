# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the program FFM.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    FFM.Nav
#
# Purpose
#    Provide configuration for GTW.NAV.E_Type.Admin entries
#
# Revision Dates
#    26-Mar-2012 (CT) Creation
#    10-May-2012 (CT) Add `Node_has_Net_Device`
#    10-May-2012 (CT) Add `Wired_Interface`, `Wired_Link`, and `Wireless_Link`
#    19-Jul-2012 (RS) Add `Person`
#    20-Jul-2012 (RS) Add `Person_has_Node`
#    20-Aug-2012 (RS) Add `Wireless_Standard`, `Wireless_Channel`,
#                     `Regulatory_Domain`, `Regulatory_Permission`,
#                     `Wireless_Interface_uses_Wireless_Channel`
#    06-Sep-2012 (RS) Remove `Node_has_Net_Device`
#    12-Sep-2012 (RS) Add `Nickname` and `Person_mentors_Person`
#    18-Sep-2012 (RS) Remove `Subject_owns_Node`
#    11-Oct-2012 (RS) `Nickname` from `PAP`
#    ��revision-date�����
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _TFL                     import TFL
from   _FFM                     import FFM
from   _GTW._OMP._PAP           import PAP

from   _TFL.I18N                import _

class Admin (object) :
    """Provide configuration for GTW.NAV.E_Type.Admin entries"""

    Antenna               = dict \
        ( ETM             = "FFM.Antenna"
        , list_display    = ("left", "name", "gain")
        )

    Antenna_Type          = dict \
        ( ETM             = "FFM.Antenna_Type"
        )

    Firmware_Binary       = dict \
        ( ETM             = "FFM.Firmware_Binary"
        )

    Firmware_Bundle       = dict \
        ( ETM             = "FFM.Firmware_Bundle"
        )

    Firmware_Type         = dict \
        ( ETM             = "FFM.Firmware_Type"
        )

    Firmware_Version      = dict \
        ( ETM             = "FFM.Firmware_Version"
        )

    IP_Network            = dict \
        ( ETM             = "FFM.IP_Network"
        )

    IP4_Network           = dict \
        ( ETM             = "FFM.IP4_Network"
        )

    Net_Credentials       = dict \
        ( ETM             = "FFM.Net_Credentials"
        )

    Net_Device            = dict \
        ( ETM             = "FFM.Net_Device"
        )

    Net_Device_Type       = dict \
        ( ETM             = "FFM.Net_Device_Type"
        )

    Net_Interface         = dict \
        ( ETM             = "FFM.Net_Interface"
        )

    Nickname              = dict \
        ( ETM             = "PAP.Nickname"
        )

    Node                  = dict \
        ( ETM             = "FFM.Node"
        )

    Person                = dict \
        ( ETM             = "PAP.Person"
        )

    Regulatory_Domain     = dict \
        ( ETM             = "FFM.Regulatory_Domain"
        )

    Regulatory_Permission = dict \
        ( ETM             = "FFM.Regulatory_Permission"
        )

    Routing_Zone          = dict \
        ( ETM             = "FFM.Routing_Zone"
        )

    Wired_Interface       = dict \
        ( ETM             = "FFM.Wired_Interface"
        )

    Wired_Link            = dict \
        ( ETM             = "FFM.Wired_Link"
        )

    Wireless_Channel      = dict \
        ( ETM             = "FFM.Wireless_Channel"
        )

    Wireless_Interface    = dict \
        ( ETM             = "FFM.Wireless_Interface"
        )

    Wireless_Link         = dict \
        ( ETM             = "FFM.Wireless_Link"
        )

    Wireless_Mode         = dict \
        ( ETM             = "FFM.Wireless_Mode"
        )

    Wireless_Standard     = dict \
        ( ETM             = "FFM.Wireless_Standard"
        )

    Zone                  = dict \
        ( ETM             = "FFM.Zone"
        )

    if False :
        Device_Type_made_by_Company = dict \
            ( ETM            = "FFM.Device_Type_made_by_Company"
            )

        Net_Interface_in_IP4_Network = dict \
            ( ETM            = "FFM.Net_Interface_in_IP4_Network"
            )

        Net_Interface_in_IP_Network = dict \
            ( ETM            = "FFM.Net_Interface_in_IP_Network"
            )

        Person_mentors_Person = dict \
            ( ETM            = "FFM.Person_mentors_Person"
            )

        Wireless_Interface_uses_Antenna = dict \
            ( ETM            = "FFM.Wireless_Interface_uses_Antenna"
            )

        Wireless_Interface_uses_Wireless_Channel = dict \
            ( ETM            = "FFM.Wireless_Interface_uses_Wireless_Channel"
            )

# end class Admin

from   _GTW._AFS._MOM import Spec

### FFM.Net_Device_Type.GTW.afs_spec = Spec.Entity (include_links = ("FFM.Device_Type_made_by_Company", ))
### ??? FFM.Antenna.GTW.afs_spec = Spec.Entity (include_links = ("interface", ))
FFM.Wireless_Interface.GTW.afs_spec = Spec.Entity \
    (include_links = ("antennas", ))

if __name__ != "__main__" :
    FFM._Export_Module ()
### __END__ FFM.Nav
