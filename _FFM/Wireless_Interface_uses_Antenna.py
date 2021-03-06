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
#    FFM.Wireless_Interface_uses_Antenna
#
# Purpose
#    Model the antenna used by a wireless interface
#
# Revision Dates
#    28-Mar-2012 (CT) Creation
#    10-May-2012 (RS) Allow multiple interfaces to use same antenna
#     6-Dec-2012 (RS) Add `belongs_to_node`
#    15-May-2013 (CT) Replace `auto_cache` by
#                     `rev_ref_attr_name`, `auto_rev_ref`
#    ��revision-date�����
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM        import *
from   _FFM                   import FFM

from   _FFM.Attr_Type         import *
import _FFM.Antenna
import _FFM.Wireless_Interface
import _FFM._Belongs_to_Node_

_Ancestor_Essence = FFM.Link2
_Mixin = FFM._Belongs_to_Node_

class Wireless_Interface_uses_Antenna (_Mixin, _Ancestor_Essence) :
    """Antenna used by a wireless interface"""

    class _Attributes (_Mixin._Attributes, _Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """Wireless interface."""

            role_type          = FFM.Wireless_Interface
            rev_ref_attr_name  = "interface"

        # end class left

        class right (_Ancestor.right) :
            """Antenna."""

            role_type          = FFM.Antenna
            auto_rev_ref       = True
            ui_allow_new       = True
            max_links          = 1

        # end class right

        ### Non-primary attributes

        class relative_height (A_Float) :
            """Height relative to device the antenna is connected to."""

            kind               = Attr.Optional
            Kind_Mixins        = (Attr.Sticky_Mixin, )
            default            = 0

        # end class relative_height

    # end class _Attributes

# end class Wireless_Interface_uses_Antenna

if __name__ != "__main__" :
    FFM._Export ("*")
### __END__ FFM.Wireless_Interface_uses_Antenna
