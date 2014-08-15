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
import ntds.dsfielddictionary
from ntds.dstime import *
import sys

dsMapLinks         = {}
dsMapBackwardLinks = {}

def dsInitLinks(dsESEFile):
    dl = open(dsESEFile , 'rb', 0)
    dl.seek(0)
    line = dl.readline()
    if line == "":
        print "Warning! Error processing the first line!\n"
        sys.exit()
    else:
        ntds.dsfielddictionary.dsFieldNameRecord = line.split('\t')
        record = line.split('\t')
        for cid in range(0, len(record)-1):
#------------------------------------------------------------------------------ 
# filling indexes for membership attributes
#------------------------------------------------------------------------------ 
            if (record[cid] == "link_DNT"):
                ntds.dsfielddictionary.dsTargetRecordIdIndex = cid
            if (record[cid] == "backlink_DNT"):
                ntds.dsfielddictionary.dsSourceRecordIdIndex = cid
            if (record[cid] == "link_deltime"):
                ntds.dsfielddictionary.dsLinkDeleteTimeIndex = cid
    dl.seek(0)
    dsBuildLinkMaps(dl)

def dsBuildLinkMaps(dsLinks):
    global dsMapLinks
    sys.stderr.write("Extracting object links...\n")
    sys.stderr.flush()
    lineid = 0
    while True:
        line = dsLinks.readline()
        if line == "":
            break
        record = line.split('\t')
        if lineid != 0:
            source = int(record[ntds.dsfielddictionary.dsSourceRecordIdIndex])
            target = int(record[ntds.dsfielddictionary.dsTargetRecordIdIndex])
            
            deltime = -1
            if record[ntds.dsfielddictionary.dsLinkDeleteTimeIndex] != "":
                deltime = dsVerifyDSTime(record[ntds.dsfielddictionary.dsLinkDeleteTimeIndex])
                
            try: 
                tmp = dsMapLinks[target]
            except KeyError:
                dsMapLinks[target] = []
                pass
            
            try:
                dsMapLinks[target].append((source, deltime))
            except KeyError:
                dsMapLinks[target] = []
                dsMapLinks[target].append((source, deltime))
           
            
            try: 
                tmp = dsMapBackwardLinks[source]
            except KeyError:
                dsMapBackwardLinks[source] = []
                pass
            
            try:
                dsMapBackwardLinks[source].append((target, deltime))
            except KeyError:
                dsMapBackwardLinks[source] = []
                dsMapBackwardLinks[source].append((target, deltime))
        lineid += 1