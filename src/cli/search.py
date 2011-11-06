# Copyright 2009 - 2011 Burak Sezer <purak@hadronproject.org>
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
import sqlite3
import cPickle as pickle

import lpms
from lpms import out
from lpms.db import dbapi
from lpms import constants as cst

help_output = (('--only-installed', 'Shows installed packages for given keyword.'),
        ('--in-name', 'Searchs given keyword in package names.'),
        ('--in-summary', 'Searchs given keyword in package summaries.'))

class Search(object):
    def __init__(self, keyword):
        self.keyword = ""
        for key in keyword:
            if not key in ('--only-installed', '--in-name', '--in-summary'):
                self.keyword += key+" "
        self.keyword = self.keyword.strip()
        self.connection = sqlite3.connect(cst.repositorydb_path)
        self.cursor = self.connection.cursor()
        self.repodb = dbapi.RepositoryDB()
        self.instdb = dbapi.InstallDB()

    def usage(self):
        out.normal("Search given keywords in database")
        out.green("General Usage:\n")
        out.write(" $ lpms -s <keyword>\n")
        out.write("\nOther options:\n")
        for h in help_output:
            if len(h) == 2:
                out.write("%-28s: %s\n" % (out.color(h[0],"green"), h[1]))
        lpms.terminate()

    def search(self):
        if lpms.getopt("--help") or len(self.keyword) == 0:
            self.usage()

        results = []
        if not lpms.getopt("--in-summary") and not lpms.getopt("--in-name"):
            name_query = self.cursor.execute('''SELECT * FROM metadata WHERE name LIKE (?)''', ("%"+self.keyword+"%",))
            results.extend(name_query.fetchall())
            summary_query = self.cursor.execute('''SELECT * FROM metadata WHERE summary LIKE (?)''', ("%"+self.keyword+"%",))
            results.extend(summary_query.fetchall())
        elif lpms.getopt("--in-summary"):
            summary_query = self.cursor.execute('''SELECT * FROM metadata WHERE summary LIKE (?)''', ("%"+self.keyword+"%",))
            results.extend(summary_query.fetchall())
        else:
            name_query = self.cursor.execute('''SELECT * FROM metadata WHERE name LIKE (?)''', ("%"+self.keyword+"%",))
            results.extend(name_query.fetchall())

        if not results:
            # if no result, search given keyword in installed packages database
            connection = sqlite3.connect(cst.installdb_path)
            cursor = connection.cursor()
            name_query = self.cursor.execute('''SELECT * FROM metadata WHERE name LIKE (?)''', ("%"+self.keyword+"%",))
            results.extend(name_query.fetchall())
            summary_query = self.cursor.execute('''SELECT * FROM metadata WHERE summary LIKE (?)''', ("%"+self.keyword+"%",))
            results.extend(summary_query.fetchall())
            if results: out.notify("these packages are no longer available.")

        for result in results:
            repo, category, name, version_data, summary = result[:5]
            version_data = pickle.loads(str(version_data))
            version = ""
            for slot in version_data:
                if slot != "0":
                    version += slot+": "+", ".join(version_data[slot])+" "
                else:
                    version += ", ".join(version_data[slot])+" "
            version = version.strip()
            pkg_status = ""; other_repo = ""
            instdb_repo_query = self.instdb.get_repo(category, name) 
            if  instdb_repo_query == repo:
                pkg_status = "["+out.color("I", "brightgreen")+"] "
            else:
                if instdb_repo_query and isinstance(instdb_repo_query, list):
                    other_repo = "%s installed from %s" % (out.color("=>", "red"), \
                            ",".join(instdb_repo_query))

            if lpms.getopt("--only-installed") and pkg_status == "":
                continue

            out.write("%s%s/%s/%s (%s) %s\n    %s" % (pkg_status, out.color(repo, "green"),  
                out.color(category, "green"),
                out.color(name, "green"),
                version,
                other_repo,
                summary+'\n'))
