# -*- coding: utf-8 -*-

#    This file is part of KTBS <http://liris.cnrs.fr/sbt-dev/ktbs>
#    Copyright (C) 2011-2012 Pierre-Antoine Champin <pchampin@liris.cnrs.fr> /
#    Françoise Conil <francoise.conil@liris.cnrs.fr> /
#    Universite de Lyon <http://www.universite-lyon.fr>
#
#    KTBS is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    KTBS is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with KTBS.  If not, see <http://www.gnu.org/licenses/>.

"""
I provide the pythonic interface to kTBS obsel collections.
"""
from rdfrest.interface import register_mixin, IResource
from rdfrest.utils import cache_result

from ..namespace import KTBS

@register_mixin(KTBS.StoredTraceObsels)
@register_mixin(KTBS.ComputedTraceObsels)
class AbstractTraceObselsMixin(IResource):
    """I provide the pythonic interface common to all kTBS obsel collections.
    """

    ######## Extension to the abstract kTBS API ########
    # (as this class is not defined by the API anyway)

    @property
    @cache_result
    def trace(self):
        """I return the trace owning this obsel collection.
        """
        trace_uri = self.state.value(None, KTBS.hasObselCollection, self.uri)
        return self.factory(trace_uri)
        # must be a .trace.AbstractTraceMixin
