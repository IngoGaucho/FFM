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
#    ��revision-date�����
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _TFL                     import TFL
from   _FFM                     import FFM

from   _TFL.I18N                import _

class Admin (object) :
    """Provide configuration for GTW.NAV.E_Type.Admin entries"""

    Antenna              = dict \
        ( ETM            = "FFM.Antenna"
        )

    Antenna_Type         = dict \
        ( ETM            = "FFM.Antenna_Type"
        )

    Net_Credentials      = dict \
        ( ETM            = "FFM.Net_Credentials"
        )

    Net_Device           = dict \
        ( ETM            = "FFM.Net_Device"
        )

    Net_Device_Type      = dict \
        ( ETM            = "FFM.Net_Device_Type"
        )

    Net_Interface        = dict \
        ( ETM            = "FFM.Net_Interface"
        )

    Node                 = dict \
        ( ETM            = "FFM.Node"
        )

    Routing_Zone         = dict \
        ( ETM            = "FFM.Routing_Zone"
        )

    Wireless_Interface   = dict \
        ( ETM            = "FFM.Wireless_Interface"
        )

    Wireless_Mode        = dict \
        ( ETM            = "FFM.Wireless_Mode"
        )

    Zone                 = dict \
        ( ETM            = "FFM.Zone"
        )
# end class Admin

from   _GTW._AFS._MOM import Spec

### FFM.Net_Device_Type.GTW.afs_spec = Spec.Entity (include_links = ("FFM.Device_Type_made_by_Company", ))

if __name__ != "__main__" :
    FFM._Export_Module ()
### __END__ FFM.Nav