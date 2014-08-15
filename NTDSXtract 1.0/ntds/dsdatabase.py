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
from stat import *
from os import stat
import time
import ntds.dsfielddictionary
from ntds.dsencryption import *

dsMapOffsetByLineId   = {} #Map that can be used to find the offset for line
dsMapLineIdByRecordId = {} #Map that can be used to find the line for record
dsMapTypeByRecordId   = {} #Map that can be used to find the type for record
dsMapRecordIdByName   = {} #Map that can be used to find the record for name
dsMapChildsByRecordId = {} #Map that can be used to find child objects
dsMapTypeIdByTypeName = {} #Map that can be used to find child objects

dsDatabaseSize = -1

def dsInitDatabase(dsESEFile):
    global dsDatabaseSize
    dsDatabaseSize = stat(dsESEFile).st_size
#    sys.stderr.write("Database size: %d bytes\n" % dsDatabaseSize)
    sys.stderr.write("Initialising engine...\n")  
    db = open(dsESEFile , 'rb', 0)
    db.seek(0)
    line = db.readline()
    if line == "":
        sys.stderr.write("Warning! Error processing the first line!\n")
        sys.exit()
    else:
        dsFieldNameRecord = line.split('\t')
        record = line.split('\t')
        for cid in range(0, len(record)-1):
#------------------------------------------------------------------------------ 
# filling indexes for object attributes
#------------------------------------------------------------------------------ 
            if (record[cid] == "DNT_col"):
                ntds.dsfielddictionary.dsRecordIdIndex = cid
            if (record[cid] == "PDNT_col"):
                ntds.dsfielddictionary.dsParentRecordIdIndex = cid
            if (record[cid] == "time_col"):
                ntds.dsfielddictionary.dsRecordTimeIndex = cid
            if (record[cid] == "Ancestors_col"):
                ntds.dsfielddictionary.dsAncestorsIndex = cid
            if (record[cid] == "ATTb590606"):
                ntds.dsfielddictionary.dsObjectTypeIdIndex = cid
            if (record[cid] == "ATTm3"):
                ntds.dsfielddictionary.dsObjectNameIndex = cid
            if (record[cid] == "ATTm589825"):
                ntds.dsfielddictionary.dsObjectName2Index = cid
            if (record[cid] == "ATTk589826"):
                ntds.dsfielddictionary.dsObjectGUIDIndex = cid
            if (record[cid] == "ATTl131074"):
                ntds.dsfielddictionary.dsWhenCreatedIndex = cid
            if (record[cid] == "ATTl131075"):
                ntds.dsfielddictionary.dsWhenChangedIndex = cid
            if (record[cid] == "ATTq131091"):
                ntds.dsfielddictionary.dsUSNCreatedIndex = cid
            if (record[cid] == "ATTq131192"):
                ntds.dsfielddictionary.dsUSNChangedIndex = cid
            if (record[cid] == "OBJ_col"):
                ntds.dsfielddictionary.dsObjectColIndex = cid
            if (record[cid] == "ATTi131120"):
                ntds.dsfielddictionary.dsIsDeletedIndex = cid
#------------------------------------------------------------------------------ 
# Filling indexes for deleted object attributes
#------------------------------------------------------------------------------ 
            if (record[cid] == "ATTb590605"):
                ntds.dsfielddictionary.dsOrigContainerIdIndex = cid
#------------------------------------------------------------------------------ 
# Filling indexes for account object attributes
#------------------------------------------------------------------------------ 
            if (record[cid] == "ATTr589970"):
                ntds.dsfielddictionary.dsSIDIndex = cid
            if (record[cid] == "ATTm590045"):
                ntds.dsfielddictionary.dsSAMAccountNameIndex = cid
            if (record[cid] == "ATTm590480"):
                ntds.dsfielddictionary.dsUserPrincipalNameIndex = cid
            if (record[cid] == "ATTj590126"):
                ntds.dsfielddictionary.dsSAMAccountTypeIndex = cid
            if (record[cid] == "ATTj589832"):
                ntds.dsfielddictionary.dsUserAccountControlIndex = cid
            if (record[cid] == "ATTq589876"):
                ntds.dsfielddictionary.dsLastLogonIndex = cid
            if (record[cid] == "ATTq591520"):
                ntds.dsfielddictionary.dsLastLogonTimeStampIndex = cid
            if (record[cid] == "ATTq589983"):
                ntds.dsfielddictionary.dsAccountExpiresIndex = cid
            if (record[cid] == "ATTq589920"):
                ntds.dsfielddictionary.dsPasswordLastSetIndex = cid
            if (record[cid] == "ATTq589873"):
                ntds.dsfielddictionary.dsBadPwdTimeIndex = cid
            if (record[cid] == "ATTj589993"):
                ntds.dsfielddictionary.dsLogonCountIndex = cid
            if (record[cid] == "ATTj589836"):
                ntds.dsfielddictionary.dsBadPwdCountIndex = cid
            if (record[cid] == "ATTj589922"):
                ntds.dsfielddictionary.dsPrimaryGroupIdIndex = cid
            if (record[cid] == "ATTk589914"):    
                ntds.dsfielddictionary.dsNTHashIndex = cid
            if (record[cid] == "ATTk589879"):
                ntds.dsfielddictionary.dsLMHashIndex = cid
            if (record[cid] == "ATTk589918"):
                ntds.dsfielddictionary.dsNTHashHistoryIndex = cid
            if (record[cid] == "ATTk589984"):
                ntds.dsfielddictionary.dsLMHashHistoryIndex = cid
            if (record[cid] == "ATTk591734"):
                ntds.dsfielddictionary.dsUnixPasswordIndex = cid
            if (record[cid] == "ATTk36"):
                ntds.dsfielddictionary.dsADUserObjectsIndex = cid
            if (record[cid] == "ATTk589949"):
                ntds.dsfielddictionary.dsSupplementalCredentialsIndex = cid
#------------------------------------------------------------------------------
# Filling indexes for computer objects attributes
#------------------------------------------------------------------------------
            if (record[cid] == "ATTj589993"):
                ntds.dsfielddictionary.dsLogonCountIndex = cid
            if (record[cid] == "ATTm590443"):
                ntds.dsfielddictionary.dsDNSHostNameIndex = cid
            if (record[cid] == "ATTm590187"):
                ntds.dsfielddictionary.dsOSNameIndex = cid
            if (record[cid] == "ATTm590188"):
                ntds.dsfielddictionary.dsOSVersionIndex = cid
#------------------------------------------------------------------------------ 
# Filling indexes for bitlocker objects
#------------------------------------------------------------------------------ 
            if (record[cid] == "ATTm591788"):
                ntds.dsfielddictionary.dsRecoveryPasswordIndex = cid
            if (record[cid] == "ATTk591823"):
                ntds.dsfielddictionary.dsFVEKeyPackageIndex = cid
            if (record[cid] == "ATTk591822"):
                ntds.dsfielddictionary.dsVolumeGUIDIndex = cid
            if (record[cid] == "ATTk591789"):
                ntds.dsfielddictionary.dsRecoveryGUIDIndex = cid
#===============================================================================
# Filling indexes for AD encryption
#===============================================================================
            if (record[cid] == "ATTk590689"):
                ntds.dsfielddictionary.dsPEKIndex = cid
    db.seek(0)
    dsBuildMaps(db)
    return db
    
def dsBuildMaps(dsDatabase):
    
    global dsMapOffsetByLineId
    global dsMapLineIdByRecordId
    global dsMapRecordIdByName
    global dsMapTypeByRecordId
    global dsMapChildsByRecordId
    
    lineid = 0
    while True:
        sys.stderr.write("\rScanning database - %d%% -> %d records processed" % (
                                            dsDatabase.tell()*100/dsDatabaseSize,
                                            lineid+1
                                            ))
        sys.stderr.flush()
        try:
            dsMapOffsetByLineId[lineid] = dsDatabase.tell()
        except:
            sys.stderr.write("\nWarning! Error at dsMapOffsetByLineId!\n")
            pass
        line = dsDatabase.readline()
        if line == "":
            break
        record = line.split('\t')
        if lineid != 0:
            #===================================================================
            # This record will always be the record representing the domain
            # object
            #===================================================================
            if record[ntds.dsfielddictionary.dsPEKIndex] != "":
                ntds.dsfielddictionary.dsEncryptedPEK = record[ntds.dsfielddictionary.dsPEKIndex]
                
            try:
                dsMapLineIdByRecordId[int(record[ntds.dsfielddictionary.dsRecordIdIndex])] = lineid
            except:
                sys.stderr.write("\nWarning! Error at dsMapLineIdByRecordId!\n")
                pass
            
            try:
                tmp = dsMapRecordIdByName[record[ntds.dsfielddictionary.dsObjectName2Index]]
            except:
                dsMapRecordIdByName[record[ntds.dsfielddictionary.dsObjectName2Index]] = int(record[ntds.dsfielddictionary.dsRecordIdIndex])
                pass
            
            try:
                dsMapTypeByRecordId[int(record[ntds.dsfielddictionary.dsRecordIdIndex])] = record[ntds.dsfielddictionary.dsObjectTypeIdIndex]
            except:
                sys.stderr.write("\nWarning! Error at dsMapTypeByRecordId!\n")
                pass
            
            try:
                tmp = dsMapChildsByRecordId[int(record[ntds.dsfielddictionary.dsRecordIdIndex])]
            except KeyError:
                dsMapChildsByRecordId[int(record[ntds.dsfielddictionary.dsRecordIdIndex])] = []
                pass
            
            try:
                dsMapChildsByRecordId[int(record[ntds.dsfielddictionary.dsParentRecordIdIndex])].append(int(record[ntds.dsfielddictionary.dsRecordIdIndex]))
            except KeyError:
                dsMapChildsByRecordId[int(record[ntds.dsfielddictionary.dsParentRecordIdIndex])] = []
                dsMapChildsByRecordId[int(record[ntds.dsfielddictionary.dsParentRecordIdIndex])].append(int(record[ntds.dsfielddictionary.dsRecordIdIndex]))
                
        lineid += 1
    sys.stderr.write("\n")
    dsBuildTypeMap(dsDatabase)

def dsBuildTypeMap(dsDatabase):
    global dsMapTypeIdByTypeName

    schemarecid  = -1
    try:
        schemarecid = dsMapRecordIdByName["Schema"]
    except:
        pass
    
    lineid = int(dsMapLineIdByRecordId[schemarecid])
    offset = int(dsMapOffsetByLineId[lineid])
    dsDatabase.seek(offset)
    line = ""
    record = ""
    line = dsDatabase.readline()
    record = line.split('\t')
    oc = record[ntds.dsfielddictionary.dsObjectColIndex]
    if oc != "1":
        i = 0
        l = len(dsMapLineIdByRecordId)
        for recordid in dsMapLineIdByRecordId:
            sys.stderr.write("\rSearching for Schema object - %d%% -> %d records processed" % (
                                                i*100/l,
                                                i+1
                                                ))
            lineid = int(dsMapLineIdByRecordId[recordid])
            offset = int(dsMapOffsetByLineId[lineid])
            dsDatabase.seek(offset)
            line = ""
            record = ""
            line = dsDatabase.readline()
            record = line.split('\t')
            name = record[ntds.dsfielddictionary.dsObjectName2Index]
            oc = record[ntds.dsfielddictionary.dsObjectColIndex]
            if name == "Schema" and oc == "1":
                schemarecid = recordid
                break
            i += 1
    
        sys.stderr.write("\rSearching for Schema object - %d%% -> %d records processed" % (
                                                100,
                                                i
                                                ))
        sys.stderr.write("\n")
        sys.stderr.flush()

    schemachilds = dsMapChildsByRecordId[schemarecid]
    i = 0
    l = len(schemachilds)
    for child in schemachilds:
        sys.stderr.write("\rExtracting schema information - %d%% -> %d records processed" % (
                                            i*100/l,
                                            i+1
                                            ))
        sys.stderr.flush()
        lineid = int(dsMapLineIdByRecordId[int(child)])
        offset = int(dsMapOffsetByLineId[int(lineid)])
        dsDatabase.seek(offset)
        
        record = ""
        line = ""
        line = dsDatabase.readline()
        if line != "":
            record = line.split('\t')
            name = record[ntds.dsfielddictionary.dsObjectName2Index]
            dsMapTypeIdByTypeName[name] = child
        i += 1
    sys.stderr.write("\rExtracting schema information - %d%% -> %d records processed" % (
                                            100,
                                            i
                                            ))
    sys.stderr.write("\n")
    sys.stderr.flush()

def dsInitEncryption(syshive_fname):
    bootkey = get_syskey(syshive_fname)
    enc_pek = unhexlify(ntds.dsfielddictionary.dsEncryptedPEK[16:])
    ntds.dsfielddictionary.dsPEK=dsDecryptPEK(bootkey, enc_pek)
    