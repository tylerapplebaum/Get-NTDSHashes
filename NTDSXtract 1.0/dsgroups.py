# This file is part of ntdsxtract.
#
# ntdsxtract is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ntdsxtract is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ntdsxtract.  If not, see <http://www.gnu.org/licenses/>.

'''
@author:        Csaba Barta
@license:       GNU General Public License 2.0 or later
@contact:       csaba.barta@gmail.com
'''

from ntds.dsdatabase import *
from ntds.dsrecord import *
from ntds.dsobjects import *
from ntds.dslink import *
from ntds.dstime import *

if len(sys.argv) < 3 or (len(sys.argv) == 4):
    print "DSGroups"
    print "Extracts information related to group objects\n"
    print "usage: %s <datatable> <linktable> [option]" % sys.argv[0]
    print "  options:"
    print "    --rid <group rid>"
    print "    --name <group name>"
    sys.exit(1)

db = dsInitDatabase(sys.argv[1])
dl = dsInitLinks(sys.argv[2])

gtype = dsGetTypeIdByTypeName(db, "Group")
utype = dsGetTypeIdByTypeName(db, "Person")
ctype = dsGetTypeIdByTypeName(db, "Computer")

users = []
for recordid in dsMapLineIdByRecordId:
    if (int(dsGetRecordType(db, recordid)) == utype or
        int(dsGetRecordType(db, recordid)) == ctype):
        users.append(dsUser(db, recordid))
        
print "\nList of groups:"
print "==============="
for recordid in dsMapLineIdByRecordId:
    if int(dsGetRecordType(db, recordid)) == gtype:
        group = dsGroup(db, recordid)
        if len(sys.argv) > 4:
            if sys.argv[3] == "--rid" and group.SID.RID != int(sys.argv[4]):
                group = None
                continue
            if sys.argv[3] == "--name" and group.Name != sys.argv[4]:
                group = None
                continue
        print "\nRecord ID:  %d" % group.RecordId
        print "Group Name: %s" % group.Name
        print "GUID: %s" % str(group.GUID)
        print "SID: %s" % str(group.SID)
        print "When created: " + dsGetDSTimeStampStr(group.WhenCreated)
        print "When changed: " + dsGetDSTimeStampStr(group.WhenChanged)
        print "Members:"
        for u in users:
            if u.PrimaryGroupID != -1:
                if u.PrimaryGroupID == group.SID.RID:
                    print "\t%s (%s) (%s) (P)" % (u.Name, u.GUID, u.Type)
        memberlist = group.getMembers()
        for memberdata in memberlist:
            (memberid, deltime) = memberdata
            member = dsObject(db, memberid)
            if deltime == -1:
                print "\t%s (%s) (%s)" % (member.Name, member.GUID, member.Type)
            else:
                print "\t%s (%s) (%s) - Deleted: %s" % (member.Name, member.GUID, member.Type, dsGetDSTimeStampStr(dsConvertToDSTimeStamp(deltime)))
            member = None
        group = None