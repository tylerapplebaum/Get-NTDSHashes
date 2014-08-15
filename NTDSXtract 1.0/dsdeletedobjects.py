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

import sys
import ntds.dsfielddictionary
from ntds.dsdatabase import *
from ntds.dsobjects import *
from ntds.dsrecord import *
from ntds.dstime import *

if len(sys.argv) < 2 or len(sys.argv) > 4:
    print "DSDeletedObjects"
    print "Extracts information related to deleted objects\n"
    print "usage: %s <datatable> [option]" % sys.argv[0]
    print "  options:"
    print "    --output <output file name>"
    print "        The record containing the object and the preserved attributes will be"
    print "        written to this file"
    print "    --useIsDeleted"
    print "        Extract deleted objects based on the IsDeleted flag"
    print "\nFields of the main output"
    print "    Rec. ID|Cr. time|Mod. time|Obj. name|Orig. container name\n"
    sys.exit(1)

of = ""
useID = False

optid = 0
for opt in sys.argv:
    if opt == "--output":
        if len(sys.argv) < 4:
            usage()
            sys.exit(1)
        of = int(sys.argv[optid + 1])
    if opt == "--useIsDeleted":
        useID = True
    optid += 1

print "Running with options:"
if useID == true:
    print "\tUsing IsDeleted flag"
else:
    print "\tUsing Deleted Objects containers"
if of != "":
    print "\tOutput file: %s" % of
    

delobjconts = []
delobjs = []

db = dsInitDatabase(sys.argv[1])
ctypeid = dsGetTypeIdByTypeName(db, "Container")

l = len(dsMapLineIdByRecordId)
i = 0
if useID == False:
    for recid in dsMapLineIdByRecordId:
        sys.stderr.write("\rExtracting deleted objects - %d%%" % (i*100/l))
        sys.stderr.flush()
        
        rec = dsGetRecordByLineId(db, dsMapLineIdByRecordId[recid])
        try:
            if (int(rec[ntds.dsfielddictionary.dsObjectTypeIdIndex]) == ctypeid and
                rec[ntds.dsfielddictionary.dsObjectName2Index] == "Deleted Objects"):
                
                delobjconts.append(recid)
        except:
            pass
        i += 1
    sys.stderr.write("\n")
    
    if of != "":
        fdelobjs = open(of, 'w')
        fdelobjs.writelines('\t'.join(ntds.dsfielddictionary.dsFieldNameRecord))
    
    for crecid in delobjconts:
        container = dsObject(db, crecid)
        childs = container.getChilds()
        for did in childs:
            dobj = dsObject(db, did)
            
            origcname = ""
            if ntds.dsrecord.dsGetRecordByRecordId(
                    db,
                    dobj.Record[ntds.dsfielddictionary.dsOrigContainerIdIndex]
                    ) != None:
                
                origcname = ntds.dsrecord.dsGetRecordByRecordId(
                                db,
                                dobj.Record[ntds.dsfielddictionary.dsOrigContainerIdIndex]
                                )[ntds.dsfielddictionary.dsObjectName2Index]
            
            sys.stdout.write(
                             "%d|%s|%s|%s|%s\n" % (
                                           dobj.RecordId,
                                           dsGetDSTimeStampStr(dobj.WhenCreated),
                                           dsGetDSTimeStampStr(dobj.WhenChanged),
                                           dobj.Name,
                                           origcname
                                           )
                             )
            if of != "":
                fdelobjs.writelines('\t'.join(dobj.Record))
                
if useID == True:
    for recid in dsMapLineIdByRecordId:
        sys.stderr.write("\rExtracting deleted objects - %d%%" % (i*100/l))
        sys.stderr.flush()
        
        rec = dsGetRecordByLineId(db, dsMapLineIdByRecordId[recid])
        try:
            if int(rec[ntds.dsfielddictionary.dsIsDeletedIndex]) == 1: 
                delobjs.append(recid)
        except:
            pass
        i += 1
    sys.stderr.write("\n")
    
    for did in delobjs:
        dobj = dsObject(db, did)
        
        origcname = ""
        if ntds.dsrecord.dsGetRecordByRecordId(
                db,
                dobj.Record[ntds.dsfielddictionary.dsOrigContainerIdIndex]
                ) != None:
            
            origcname = ntds.dsrecord.dsGetRecordByRecordId(
                            db,
                            dobj.Record[ntds.dsfielddictionary.dsOrigContainerIdIndex]
                            )[ntds.dsfielddictionary.dsObjectName2Index]
        
        sys.stdout.write(
                         "%d|%s|%s|%s|%s\n" % (
                                       dobj.RecordId,
                                       dsGetDSTimeStampStr(dobj.WhenCreated),
                                       dsGetDSTimeStampStr(dobj.WhenChanged),
                                       dobj.Name,
                                       origcname
                                       )
                         )
        if of != "":
            fdelobjs.writelines('\t'.join(dobj.Record))

if of != "":
    fdelobjs.close()