# Copyright 2009 - 2011 Burak Sezer <burak.sezer@linux.org.tr>
# 
# This file is part of lpms
#  
# lpms is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#   
# lpms is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#   
# You should have received a copy of the GNU General Public License
# along with lpms.  If not, see <http://www.gnu.org/licenses/>.


class CommandFailed(Exception):
    pass

class DatabaseAPIError(Exception):
    pass

class NotExecutable(Exception):
    pass

class ConfKeyError(Exception):
    pass

class ConstError(TypeError):
    pass
 
class BuiltinError(Exception):
    pass

class BuildError(Exception):
    pass

class MakeError(Exception):
    pass

class NotInstalled(Exception):
    pass

class FileNotFound(Exception):
    pass

class CycleError(Exception):
    pass

class NoSize(Exception):
    pass

class UnmetDependency(Exception):
    pass

class InvalidURI(Exception):
    pass

class ItemNotFound(Exception):
    pass

class UnavailablePackage(Exception):
    pass

class MissingInternalParameter(Exception):
    pass

class LockedPackage(Exception):
    pass

class PackageNotFound(Exception):
    pass

class DependencyError(Exception):
    pass

class ConflictError(Exception):
    pass

class ConditionConflict(Exception):
    pass

class IntegrityError(Exception):
    pass

class InvalidRepository(Exception):
    pass

class AlreadyRunning(Exception):
    pass

class LpmsTerminate(Exception):
    pass
