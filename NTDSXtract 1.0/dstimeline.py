# This file is part of ntdsxtract.
#
# ntdsxtract is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ntdsdump is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ntdsdump.  If not, see <http://www.gnu.org/licenses/>.

'''
@author:        Csaba Barta
@license:       GNU General Public License 2.0 or later
@contact:       csaba.barta@gmail.com
'''
import sys
from ntds.dsdatabase import *
from ntds.dsobjects import *
from ntds.dstime import *
from operator import *
import time

times = []
timeline = []

if len(sys.argv) < 2:
    print "DSTimeline"
    print "Constructs timeline\n"
    print "usage: %s <datatable> [option]" % sys.argv[0]
    print "  options:"
    print "    --b"
    print "       mactime body format"
    print "\nFields of the default output"
    print "    Timestamp|Action|Record ID|Obj. name|Obj. type"
    sys.exit(1)

db = dsInitDatabase(sys.argv[1])
i = 0
l = len(dsMapLineIdByRecordId)
for recordid in dsMapLineIdByRecordId:
    sys.stderr.write("\rBuilding timeline - %d%% -> %d records processed" % (
                                                                           i*100/l,
                                                                           i
                                                                           ))
    sys.stderr.flush()
    tmp = dsObject(db, recordid)
    
    if len(sys.argv) == 3 and sys.argv[2] == "--b":
        if tmp.WhenChanged != -1 or tmp.WhenCreated != -1:
            times.append((recordid, 
                          0 if tmp.WhenCreated == -1 else tmp.WhenCreated, 
                          0 if tmp.WhenChanged == -1 else tmp.WhenChanged, 
                          tmp.Name,
                          tmp.Type,
                          ""
                          ))
        
        if tmp.Type == "Person":
            user = dsAccount(db, recordid)
            if user.LastLogon != -1:
                times.append((recordid, 
                              0, 
                              user.LastLogon, 
                              user.Name,
                              user.Type, 
                              "Logged in"
                              ))
            if user.LastLogonTimeStamp != -1:
                times.append((recordid, 
                              0, 
                              user.LastLogonTimeStamp, 
                              user.Name,
                              user.Type, 
                              "Login timestamp sync"
                              ))
            if user.PasswordLastSet != -1:
                times.append((recordid, 
                              0, 
                              user.PasswordLastSet, 
                              user.Name, 
                              user.Type,
                              "Password changed"
                              ))
            user = None
    
    else:
        if dsVerifyDSTimeStamp(tmp.WhenCreated) != -1:
            times.append((recordid, tmp.WhenCreated, "Created", tmp.Name, tmp.Type))
        if dsVerifyDSTimeStamp(tmp.WhenChanged) != -1:
            times.append((recordid, tmp.WhenChanged, "Modified", tmp.Name, tmp.Type))
        
        if tmp.Type == "Person":
            user = dsAccount(db, recordid)
            if user.LastLogon != -1 and user.LastLogon != 0:
                times.append((recordid,
                              user.LastLogon, 
                              "Logged in", 
                              user.Name, 
                              user.Type
                              ))
                
            if user.LastLogonTimeStamp != -1 and user.LastLogonTimeStamp != 0:
                times.append((recordid, 
                              user.LastLogonTimeStamp, 
                              "Login timestamp sync", 
                              user.Name, 
                              user.Type
                              ))
                
            if user.PasswordLastSet != -1 and user.PasswordLastSet != 0:
                times.append((recordid, 
                              user.PasswordLastSet, 
                              "Password changed", 
                              user.Name, 
                              user.Type
                              ))
            user = None
    i += 1
sys.stderr.write("\n")
        
timeline = sorted(times, key=itemgetter(1))
for item in timeline:
    if len(sys.argv) == 3 and sys.argv[2] == "--b":
        (id, ctimestamp, mtimestamp, name, type, actiontype) = item
        if actiontype != "":
            print "0|%s (%s) - (%s)|%d||0|0|0|0|%d|0|%d" % (
                                                     name, 
                                                     type,
                                                     actiontype, 
                                                     id,
                                                     dsGetPOSIXTimeStamp(mtimestamp),
                                                     dsGetPOSIXTimeStamp(ctimestamp)
                                                     )
        else:
            print "0|%s (%s)|%d||0|0|0|0|%d|0|%d" % (
                                                     name, 
                                                     type, 
                                                     id,
                                                     dsGetPOSIXTimeStamp(mtimestamp),
                                                     dsGetPOSIXTimeStamp(ctimestamp)
                                                     )
    else:
        (id, timestamp, action, name, type) = item
        print "%s|%s|%d|%s (%s)" % (
                                       dsGetDSTimeStampStr(timestamp),
                                       action,
                                       id,
                                       name,
                                       type
                                       )