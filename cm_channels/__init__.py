# Copyright 2016 CrowdMaster Developer Team
#
# ##### BEGIN GPL LICENSE BLOCK ######
# This file is part of CrowdMaster.
#
# CrowdMaster is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CrowdMaster is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CrowdMaster.  If not, see <http://www.gnu.org/licenses/>.
# ##### END GPL LICENSE BLOCK #####

from .cm_noiseChannels import Noise
from .cm_soundChannels import Sound
from .cm_stateChannels import State
from .cm_worldChannels import World
from .cm_crowdChannels import Crowd
from .cm_groundChannels import Ground
from .cm_formationChannels import Formation
from .cm_pathChannels import Path
from . import cm_pathChannels
Path = cm_pathChannels.Path


def register():
    cm_pathChannels.register()


def unregister():
    cm_pathChannels.unregister()
