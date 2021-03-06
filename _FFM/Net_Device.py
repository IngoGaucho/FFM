# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012-2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package FFM.
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
#    FFM.Net_Device
#
# Purpose
#    Model a network device of FFM
#
# Revision Dates
#     6-Mar-2012 (CT) Creation
#    30-Aug-2012 (CT) Add `primary` attribute `node`
#     6-Dec-2012 (RS) Add `belongs_to_node`
#    14-Dec-2012 (CT) Change `belongs_to_node.kind` to `Attr.Query`
#    17-Dec-2012 (CT) Set `belongs_to_node.hidden` to `True`
#    26-Jan-2013 (CT) Define `belongs_to_node.query`, not `.query_fct`
#    ��revision-date�����
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM        import *
from   _FFM                   import FFM
import _FFM.Device
import _FFM.Net_Device_Type
import _FFM.Node

_Ancestor_Essence = FFM.Device

class Net_Device (_Ancestor_Essence) :
    """Model a network device of FFM."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class left (_Ancestor.left) :
            """Type of net device"""

            role_type          = FFM.Net_Device_Type

        # end class left

        class node (A_Id_Entity) :
            """`Node` to which the `net_device` is connected."""

            kind               = Attr.Primary
            P_Type             = FFM.Node

        # end class node

        class belongs_to_node (A_Id_Entity) :
            """Node to which this entity belongs."""

            kind               = Attr.Query
            auto_up_depends    = ("node", )
            hidden             = True
            P_Type             = FFM.Node
            query              = Q.node

        # end class belongs_to_node

    # end class _Attributes

# end class Net_Device

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.Net_Device
