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

import re

import lpms
from lpms import out
from lpms.db import dbapi

class Info(object):
    def __init__(self, params):
        self.repo_db = dbapi.RepositoryDB()
        self.params = params

    def usage(self):
        out.normal("Get information about given package")
        out.green("General Usage:\n")
        out.write(" $ lpms -i repo/category/pkgname\n")
        out.write("\nrepo and category keywords are optional.\n")
        lpms.terminate()

    def get_info(self, pkg):
        repo, category, name, version = pkg
        out.write('%s/%s' % (category, out.color(name, 'brightgreen')+'\n'))
        out.write('    %-20s %s' % (out.color("available versions:", 'green'), version+'\n'))
        for tag in ('summary', 'homepage', 'license', 'options'):
            data = getattr(self.repo_db, "get_"+tag)(name, repo, category)[0]
            if data is not None:
                out.write('    %s %s' % (out.color(tag+":", 'green'), data+'\n'))
        out.write('    %s %s' % (out.color("repo:", 'green'), repo+'\n'))


    def run(self):
        if lpms.getopt("--help") or len(self.params) == 0:
            self.usage()

        for param in self.params:
            param = param.split("/")
            if len(param) == 3:
                myrepo, mycategory, myname = param
                data = self.repo_db.find_pkg(myname, myrepo, mycategory)
            elif len(param) == 2:
                mycategory, myname = param
                data = self.repo_db.find_pkg(myname, pkg_category=mycategory)
            elif len(param) == 1:
                data = self.repo_db.find_pkg(param[0])
            else:
                lpms.catch_error("%s seems invalid." % out.color("/".join(param), "brightred"))

            if not data:
                lpms.catch_error("%s not found!" % out.color("/".join(param), "brightred"))

            if type(data).__name__ == 'tuple':
                self.get_info(data)
            else:
                for pkg in data:
                    self.get_info(pkg)
