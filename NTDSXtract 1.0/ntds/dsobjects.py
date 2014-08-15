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
from ntds.dsdatabase import *
from ntds.dslink import *
from ntds.dsrecord import *
from ntds.dstime import *
from ntds.dsencryption import *

from ntds.lib.guid import *
from ntds.lib.sid import *

class dsObject:
    '''
    The main AD object
    '''
    Record      = None
    Name        = ""
    RecordId    = -1
    TypeId      = -1
    Type        = ""
    GUID        = None
    WhenCreated = -1
    WhenChanged = -1
    USNCreated  = -1
    USNChanged  = -1
    IsDeleted   = False
    
    def __init__(self, dsDatabase, dsRecordId):
        '''
        Constructor
        '''
        self.RecordId = dsRecordId
        self.Record = dsGetRecordByRecordId(dsDatabase, self.RecordId)
        self.Name   = self.Record[ntds.dsfielddictionary.dsObjectName2Index]
        self.TypeId = dsGetRecordType(dsDatabase, self.RecordId)
        self.Type   = dsGetTypeName(dsDatabase, self.TypeId)

        if self.Record[ntds.dsfielddictionary.dsObjectGUIDIndex] != "":
            self.GUID = GUID(self.Record[ntds.dsfielddictionary.dsObjectGUIDIndex])
        
        if self.Record[ntds.dsfielddictionary.dsWhenCreatedIndex] != "":
            self.WhenCreated = dsConvertToDSTimeStamp(
                                self.Record[ntds.dsfielddictionary.dsWhenCreatedIndex]
                                                      )
        else:
            self.WhenCreated = dsConvertToDSTimeStamp(
                                self.Record[ntds.dsfielddictionary.dsRecordTimeIndex]
                                                      )
        
        if self.Record[ntds.dsfielddictionary.dsWhenChangedIndex] != "":
            self.WhenChanged = dsConvertToDSTimeStamp(
                                self.Record[ntds.dsfielddictionary.dsWhenChangedIndex]
                                                      )

        if self.Record[ntds.dsfielddictionary.dsUSNCreatedIndex] != "":
            self.USNCreated = int(self.Record[ntds.dsfielddictionary.dsUSNCreatedIndex])
        
        if self.Record[ntds.dsfielddictionary.dsUSNChangedIndex] != "":
            self.USNChanged = int(self.Record[ntds.dsfielddictionary.dsUSNChangedIndex])
            
        if self.Record[ntds.dsfielddictionary.dsIsDeletedIndex] != "":
            self.IsDeleted = True
            
    def getChilds(self):
        childlist = None
        try:
            childlist = dsMapChildsByRecordId[self.RecordId]
        except:
            pass
        return childlist
    
    def getAncestors(self, dsDatabase):
        ancestorlist = []
        ancestorvalue = self.Record[ntds.dsfielddictionary.dsAncestorsIndex] 
        if ancestorvalue != "":
            l = len(ancestorvalue) / 8
            for aid in range(0, l):
                (ancestorid,) = unpack('I', unhexlify(ancestorvalue[aid * 8:aid * 8 + 8]))
                ancestor = dsObject(dsDatabase, ancestorid)
                ancestorlist.append(ancestor)
        return ancestorlist
            
class dsFVERecoveryInformation(dsObject):
    '''
    The class used for representing BitLocker recovery information stored in AD
    '''
    
    RecoveryGUID = None
    VolumeGUID = None
    RecoveryPassword = ""
    FVEKeyPackage = ""
    
    def __init__(self, dsDatabase, dsRecordId):
        '''
        Constructor
        '''
        dsObject.__init__(self, dsDatabase, dsRecordId)
        if self.Record[ntds.dsfielddictionary.dsRecoveryGUIDIndex] != "":
            self.RecoveryGUID = GUID(self.Record[ntds.dsfielddictionary.dsRecoveryGUIDIndex])
        if self.Record[ntds.dsfielddictionary.dsVolumeGUIDIndex] != "":
            self.VolumeGUID = GUID(self.Record[ntds.dsfielddictionary.dsVolumeGUIDIndex])
        self.RecoveryPassword = self.Record[ntds.dsfielddictionary.dsRecoveryPasswordIndex]
        self.FVEKeyPackage = self.Record[ntds.dsfielddictionary.dsFVEKeyPackageIndex]
        
        
                
class dsAccount(dsObject):
    '''
    The main account class
    '''
    SID                = None
    SAMAccountName     = ""
    PrincipalName  = ""
    SAMAccountType     = -1
    UserAccountControl = -1
    LogonCount         = -1
    LastLogon          = -1
    LastLogonTimeStamp = -1
    PasswordLastSet    = -1
    AccountExpires     = -1
    BadPwdTime         = -1
    SupplementalCredentials = ""
    PrimaryGroupID     = -1
    BadPwdCount        = -1
    
    def __init__(self, dsDatabase, dsRecordId):
        '''
        Constructor
        '''
        dsObject.__init__(self, dsDatabase, dsRecordId)
        
        self.SID = SID(self.Record[ntds.dsfielddictionary.dsSIDIndex])
        self.SAMAccountName = self.Record[ntds.dsfielddictionary.dsSAMAccountNameIndex]
        self.PrincipalName = self.Record[ntds.dsfielddictionary.dsUserPrincipalNameIndex]
        if self.Record[ntds.dsfielddictionary.dsSAMAccountTypeIndex] != "":
            self.SAMAccountType = int(self.Record[ntds.dsfielddictionary.dsSAMAccountTypeIndex])
        if self.Record[ntds.dsfielddictionary.dsUserAccountControlIndex] != "":
            self.UserAccountControl = int(self.Record[ntds.dsfielddictionary.dsUserAccountControlIndex])
        if self.Record[ntds.dsfielddictionary.dsPrimaryGroupIdIndex] != "":
            self.PrimaryGroupID = int(self.Record[ntds.dsfielddictionary.dsPrimaryGroupIdIndex])
        if self.Record[ntds.dsfielddictionary.dsLogonCountIndex] != "":
            self.LogonCount = int(self.Record[ntds.dsfielddictionary.dsLogonCountIndex])
        else:
            self.BadPwdCount = -1
        if self.Record[ntds.dsfielddictionary.dsBadPwdCountIndex] != "":
            self.BadPwdCount = int(self.Record[ntds.dsfielddictionary.dsBadPwdCountIndex])
        else:
            self.BadPwdCount = -1
                        
        self.LastLogon = dsVerifyDSTimeStamp(self.Record[ntds.dsfielddictionary.dsLastLogonIndex])
        
        self.LastLogonTimeStamp = dsVerifyDSTimeStamp(self.Record[ntds.dsfielddictionary.dsLastLogonTimeStampIndex])
        
        self.PasswordLastSet = dsVerifyDSTimeStamp(self.Record[ntds.dsfielddictionary.dsPasswordLastSetIndex])
        
        self.AccountExpires = dsVerifyDSTimeStamp(self.Record[ntds.dsfielddictionary.dsAccountExpiresIndex])
        
        self.BadPwdTime = dsVerifyDSTimeStamp(self.Record[ntds.dsfielddictionary.dsBadPwdTimeIndex])
    
    def getPasswordHashes(self):
        lmhash = ""
        nthash = ""
        enclmhash = unhexlify(self.Record[ntds.dsfielddictionary.dsLMHashIndex][16:])
        encnthash = unhexlify(self.Record[ntds.dsfielddictionary.dsNTHashIndex][16:])
        if enclmhash != '':
            lmhash = dsDecryptWithPEK(ntds.dsfielddictionary.dsPEK, enclmhash)
            lmhash = hexlify(dsDecryptSingleHash(self.SID.RID, lmhash))
            if lmhash == '':
                lmhash = "NO PASSWORD"
        if encnthash != '':
            nthash = dsDecryptWithPEK(ntds.dsfielddictionary.dsPEK, encnthash)
            nthash = hexlify(dsDecryptSingleHash(self.SID.RID, nthash))
            if nthash == '':
                nthash = "NO PASSWORD"
        return (lmhash, nthash)
    
    def getPasswordHistory(self):
        lmhistory = []
        nthistory = []
        enclmhistory = unhexlify(self.Record[ntds.dsfielddictionary.dsLMHashHistoryIndex][16:])
        encnthistory = unhexlify(self.Record[ntds.dsfielddictionary.dsNTHashHistoryIndex][16:])
        slmhistory = dsDecryptWithPEK(ntds.dsfielddictionary.dsPEK, enclmhistory)
        snthistory = dsDecryptWithPEK(ntds.dsfielddictionary.dsPEK, encnthistory)
        if slmhistory != "":
            for hindex in range(0,len(slmhistory)/16):
                lmhash   = dsDecryptSingleHash(self.SID.RID, slmhistory[hindex*16:(hindex+1)*16])
                if lmhash == '':
                    lmhistory.append('NO PASSWORD')
                else:
                    lmhistory.append(hexlify(lmhash))
        if snthistory != "":
            for hindex in range(0,len(snthistory)/16):
                nthash = dsDecryptSingleHash(self.SID.RID, snthistory[hindex*16:(hindex+1)*16])
                if nthash == '':
                    nthistory.append('NO PASSWORD')
                else:
                    nthistory.append(hexlify(nthash))
        return (lmhistory, nthistory)
    
    def getSupplementalCredentials(self):
        self.SupplementalCredentials = self.Record[ntds.dsfielddictionary.dsSupplementalCredentialsIndex]
        if self.SupplementalCredentials != "":
            tmp = unhexlify(self.SupplementalCredentials[16:])
            tmpdec = dsDecryptWithPEK(ntds.dsfielddictionary.dsPEK, tmp)
            return tmpdec
        else:
            return ""
    
    def getSAMAccountType(self):
        if self.SAMAccountType != -1:
            if self.SAMAccountType & int("0x30000001", 16) == int("0x30000001", 16):
                return "SAM_MACHINE_ACCOUNT"
            if self.SAMAccountType & int("0x30000002", 16) == int("0x30000002", 16):
                return "SAM_TRUST_ACCOUNT"
            if self.SAMAccountType & int("0x30000000", 16) == int("0x30000000", 16):
                return "SAM_NORMAL_USER_ACCOUNT"
            if self.SAMAccountType & int("0x10000001", 16) == int("0x10000001", 16):
                return "SAM_NON_SECURITY_GROUP_OBJECT"
            if self.SAMAccountType & int("0x10000000", 16) == int("0x10000000", 16):
                return "SAM_GROUP_OBJECT"
            if self.SAMAccountType & int("0x20000001", 16) == int("0x20000001", 16):
                return "SAM_NON_SECURITY_ALIAS_OBJECT"
            if self.SAMAccountType & int("0x20000000", 16) == int("0x20000000", 16):
                return "SAM_ALIAS_OBJECT"
            if self.SAMAccountType & int("0x40000001", 16) == int("0x40000001", 16):
                return "SAM_APP_QUERY_GROUP"
            if self.SAMAccountType & int("0x40000000", 16) == int("0x40000000", 16):
                return "SAM_APP_BASIC_GROUP"
        else:
            return ""

    def getUserAccountControl(self):
        uac = []
        if self.UserAccountControl != -1:
            if self.UserAccountControl & int("0x2", 16) == int("0x2", 16):
                uac.append("Disabled")
            if self.UserAccountControl & int("0x10", 16) == int("0x10", 16):
                uac.append("Locked")
            if self.UserAccountControl & int("0x20", 16) == int("0x20", 16):
                uac.append("PWD Not Required")
            if self.UserAccountControl & int("0x40", 16) == int("0x40", 16):
                uac.append("User cannot change PWD")
            if self.UserAccountControl & int("0x80", 16)== int("0x80", 16):
                uac.append("Encrypted clear text PWD allowed")
            if self.UserAccountControl & int("0x200", 16) == int("0x200", 16):
                uac.append("NORMAL_ACCOUNT")
            if self.UserAccountControl & int("0x800", 16) == int("0x800", 16) :
                uac.append("INTERDOMAIN_TRUST_ACCOUNT")
            if self.UserAccountControl & int("0x1000", 16) == int("0x1000", 16):
                uac.append("WORKSTATION_TRUST_ACCOUNT")
            if self.UserAccountControl & int("0x2000", 16) == int("0x2000", 16):
                uac.append("SERVER_TRUST_ACCOUNT")
            if self.UserAccountControl & int("0x10000", 16) == int("0x10000", 16):
                uac.append("PWD Never Expires")
            if self.UserAccountControl & int("0x40000", 16) == int("0x40000", 16):
                uac.append("Smartcard Required")
            if self.UserAccountControl & int("0x800000", 16) == int("0x800000", 16):
                uac.append("PWD Expired")
        return uac
    
    def getMemberOf(self):
        grouplist = []
        try:
            grouplist = dsMapBackwardLinks[self.RecordId]
        except KeyError:
            pass
        return grouplist

class dsUser(dsAccount):
    '''
    The class used for representing User objects stored in AD
    '''
    Certificate = ""
    
    def __init__(self, dsDatabase, dsRecordId):
        '''
        Constructor
        '''
        dsAccount.__init__(self, dsDatabase, dsRecordId)
        if self.Record[ntds.dsfielddictionary.dsADUserObjectsIndex] != "":
            self.Certificate = unhexlify(self.Record[ntds.dsfielddictionary.dsADUserObjectsIndex])
        
class dsComputer(dsAccount):
    '''
    The class used for representing Computer objects stored in AD
    '''
    DNSHostName = ""
    OSName = ""
    OSVersion = ""

    def __init__(self, dsDatabase, dsRecordId):
        '''
        Constructor
        '''
        dsAccount.__init__(self, dsDatabase, dsRecordId)
        self.DNSHostName = self.Record[ntds.dsfielddictionary.dsDNSHostNameIndex]
        self.OSName = self.Record[ntds.dsfielddictionary.dsOSNameIndex]
        self.OSVersion = self.Record[ntds.dsfielddictionary.dsOSVersionIndex]
    
    def getRecoveryInformations(self, dsDatabase):
        rinfos = []
        childlist = self.getChilds()
        for child in childlist:
            if dsGetRecordType(dsDatabase, child) == dsGetTypeIdByTypeName(dsDatabase, "ms-FVE-RecoveryInformation"):
                rinfos.append(dsFVERecoveryInformation(dsDatabase, child))
        return rinfos
    
class dsGroup(dsObject):
    '''
    The class used for representing Group objects stored in AD
    '''
    SID     = None
    
    def __init__(self, dsDatabase, dsRecordId):
        '''
        Constructor
        '''
        dsObject.__init__(self, dsDatabase, dsRecordId)
        self.SID = SID(self.Record[ntds.dsfielddictionary.dsSIDIndex])
    
    def getMembers(self):
        memberlist = []
        try:
            memberlist = dsMapLinks[self.RecordId]
        except KeyError:
            pass
        return memberlist