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

dsFieldNameRecord       = []
dsEncryptedPEK          = ""
dsPEK                   = ""

#===============================================================================
# Attributes related to AD encryption
#===============================================================================
dsPEKIndex         = -1 #ATTk590689

#===============================================================================
# Attributes related to all objects
#===============================================================================
'''
dsfRecordId         = [-1, 'DNT_col',    'I']
dsfParentRecordId   = [-1, 'PDNT_col',   'I']
dsfRecordTimeIndex  = [-1, 'time_col',   'I']
dsfObjectName       = [-1, 'ATTm3',      's']
dsfObjectName2      = [-1, 'ATTm589825', 's']
dsfObjectTypeId     = [-1, 'ATTb590606', 'I']
dsfObjectGUID       = [-1, 'ATTk589826', 's']
dsfWhenCreated      = [-1, 'ATTl131074', 'Q']
dsfWhenChanged      = [-1, 'ATTl131075', 'Q']
dsfUSNCreated       = [-1, 'ATTq131091', 'I']
dsfUSNChanged       = [-1, 'ATTq131192', 'I']
'''
dsRecordIdIndex         = -1 #DNT_col
dsParentRecordIdIndex   = -1 #PDNT_col
dsRecordTimeIndex       = -1 #time_col
dsAncestorsIndex        = -1 #Ancestors_col
dsObjectNameIndex       = -1 #ATTm3
dsObjectName2Index      = -1 #ATTm589825
dsObjectTypeIdIndex     = -1 #ATTb590606
dsObjectGUIDIndex       = -1 #ATTk589826
dsWhenCreatedIndex      = -1 #ATTl131074
dsWhenChangedIndex      = -1 #ATTl131075
dsUSNCreatedIndex       = -1 #ATTq131091
dsUSNChangedIndex       = -1 #ATTq131192
dsObjectColIndex        = -1 #OBJ_col
dsIsDeletedIndex        = -1 #ATTi131120

#===============================================================================
# Attributes related to deleted objects
#===============================================================================
dsOrigContainerId  = [-1, 'ATTb590605', 'I']

dsOrigContainerIdIndex  = -1 #ATTb590605

#===============================================================================
# Attributes related to all account objects
#===============================================================================
'''
dsfSID                = [-1, 'ATTr589970', 's']
dsfSAMAccountName     = [-1, 'ATTm590045', 's']
dsfSAMAccountType     = [-1, 'ATTj590126', 'I']
dsfUserAccountControl = [-1, 'ATTj589832', 'I']
dsfLastLogon          = [-1, 'ATTq589876', 'Q']
dsfLastLogonTimeStamp = [-1, 'ATTq591520', 'Q'] 
dsfAccountExpires     = [-1, 'ATTq589983', 'Q'] 
dsfPasswordLastSet    = [-1, 'ATTq589920', 'Q']
dsfLogonCount         = [-1, 'ATTj589993', 'I']
dsfBadPwdCount        = [-1, 'ATTj589836', 'I']
dsfPrimaryGroupId     = [-1, 'ATTj589922', 'I']
'''
dsSIDIndex                = -1 #ATTr589970
dsSAMAccountNameIndex     = -1 #ATTm590045
dsSAMAccountTypeIndex     = -1 #ATTj590126
dsUserPrincipalNameIndex  = -1 #ATTm590480
dsUserAccountControlIndex = -1 #ATTj589832
dsLastLogonIndex          = -1 #ATTq589876
dsLastLogonTimeStampIndex = -1 #ATTq591520 
dsAccountExpiresIndex     = -1 #ATTq589983 
dsPasswordLastSetIndex    = -1 #ATTq589920
dsBadPwdTimeIndex         = -1 #ATTq589873
dsLogonCountIndex         = -1 #ATTj589993
dsBadPwdCountIndex        = -1 #ATTj589836
dsPrimaryGroupIdIndex     = -1 #ATTj589922
dsNTHashIndex             = -1 #ATTk589914
dsLMHashIndex             = -1 #ATTk589879
dsNTHashHistoryIndex      = -1 #ATTk589918
dsLMHashHistoryIndex      = -1 #ATTk589984
dsUnixPasswordIndex       = -1 #ATTk591734
dsADUserObjectsIndex      = -1 #ATTk36
dsSupplementalCredentialsIndex = -1 #ATTk589949

#===============================================================================
# Attributes related to computer accounts
#===============================================================================
'''
dsfDNSHostName      = [-1, 'ATTm590443', 's']
dsfOSName           = [-1, 'ATTm590187', 's']
dsfOSVersion        = [-1, 'ATTm590188', 's']
'''
dsDNSHostNameIndex      = -1 #ATTm590443
dsOSNameIndex           = -1 #ATTm590187
dsOSVersionIndex        = -1 #ATTm590188

#===============================================================================
# Attributes related to bitlocker
#===============================================================================
'''
dsfRecoveryPassword = [-1, 'ATTm591788', 's']
dsfFVEKeyPackage    = [-1, 'ATTk591823', 's']
dsfVolumeGUID       = [-1, 'ATTk591822', 's']
dsfRecoveryGUID     = [-1, 'ATTk591789', 's']
'''
dsRecoveryPasswordIndex = -1 #ATTm591788
dsFVEKeyPackageIndex    = -1 #ATTk591823
dsVolumeGUIDIndex       = -1 #ATTk591822
dsRecoveryGUIDIndex     = -1 #ATTk591789

#===============================================================================
# Attributes related to group memberships in Link_table
#===============================================================================
'''
dsfTargetRecordIdIndex = [-1, 'link_DNT', 'I']
dsfSourceRecordIdIndex = [-1, 'backlink_DNT', 'I']
'''
dsTargetRecordIdIndex = -1 #link_DNT
dsSourceRecordIdIndex = -1 #backlink_DNT
dsLinkDeleteTimeIndex = -1 #link_deltime