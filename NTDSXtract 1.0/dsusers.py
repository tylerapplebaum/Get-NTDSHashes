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
from ntds.dslink import *
from ntds.dstime import *
from ntds.dsobjects import *


def usage():
    print "DSUsers"
    print "Extracts information related to user objects\n"
    print "usage: %s <datatable> <linktable> [option]" % sys.argv[0]
    print "  options:"
    print "    --rid <user rid>"
    print "          List user identified by RID"
    print "    --name <user name>"
    print "          List user identified by Name"
    print "    --passwordhashes <system hive>"
    print "          Extract password hashes"
    print "    --passwordhistory <system hive>"
    print "          Extract password history"
    print "    --certificates"
    print "          Extract certificates"
    print "    --supplcreds <system hive>"
    print "          Extract kerberos keys"
    print "    --membership"
    print "          List groups of which the user is a member"

if len(sys.argv) < 3:
    usage()
    sys.exit(1)

# Original hex dump code from
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/142812
FILTER=''.join([(len(repr(chr(x)))==3) and chr(x) or '.' for x in range(256)])
def dump(src, length=8, indent=0):
    N=0; result=''
    while src:
        s,src = src[:length],src[length:]
        hexa = ' '.join(["%02X"%ord(x) for x in s])
        s = s.translate(FILTER)
        istr = ""
        if indent > 0:
            for i in range(indent):
                istr += " "
        result += istr + "%04X   %-*s   %s\n" % (N, length*3, hexa, s)
        N+=length
    return result

rid = -1
name = ""
syshive = ""
pwdump = False
pwhdump = False
certdump = False
suppcreddump = False
grpdump = False
optid = 0
print "Running with options:"
for opt in sys.argv:
    if opt == "--rid":
        if len(sys.argv) < 5:
            usage()
            sys.exit(1)
        rid = int(sys.argv[optid + 1])
        print "\tUser RID: %d" % rid
    if opt == "--name":
        if len(sys.argv) < 5:
            usage()
            sys.exit(1)
        name = sys.argv[optid + 1]
        print "\tUser name: %s" % name
    if opt == "--passwordhashes":
        if len(sys.argv) < 5:
            usage()
            sys.exit(1)
        syshive = sys.argv[optid + 1]
        pwdump = True
        print "\tExtracting password hashes"
    if opt == "--passwordhistory":
        if len(sys.argv) < 5:
            usage()
            sys.exit(1)
        syshive = sys.argv[optid + 1]
        pwhdump = True
        print "\tExtracting password history"
    if opt == "--certificates":
        certdump = True
        print "\tExtracting certificates"
    if opt == "--supplcreds":
        if len(sys.argv) < 5:
            usage()
            sys.exit(1)
        syshive = sys.argv[optid + 1]
        suppcreddump = True
        print "\tExtracting supplemental credentials"
    if opt == "--membership":
        grpdump = True
        print "\tExtracting memberships"
    optid += 1 

db = dsInitDatabase(sys.argv[1])
dl = dsInitLinks(sys.argv[2])

if pwdump or pwhdump or suppcreddump:
    dsInitEncryption(syshive)

utype = -1
utype = dsGetTypeIdByTypeName(db, "Person")
if utype == -1:
    print "Unable to get type id for Person"
    sys.exit()

gtype = -1
gtype = dsGetTypeIdByTypeName(db, "Group")
if gtype == -1:
    print "Unable to get type id for Group"
    sys.exit()

groups = []
for recordid in dsMapLineIdByRecordId:
    if int(dsGetRecordType(db, recordid)) == gtype:
        groups.append(dsGroup(db, recordid))

print "\nList of users:"
print "=============="
for recordid in dsMapLineIdByRecordId:
    if int(dsGetRecordType(db, recordid)) == utype:
        user = dsUser(db, recordid)
        if rid != -1 and user.SID.RID != rid:
            continue
        if name != "" and user.Name != name:
            continue

        print "\nRecord ID:           %d" % user.RecordId
        print "User name:           %s" % user.Name
        print "User principal name: %s" % user.PrincipalName
        print "SAM Account name:    %s" % user.SAMAccountName
        print "SAM Account type:    %s" % user.getSAMAccountType()
        print "GUID: %s" % str(user.GUID)
        print "SID:  %s" % str(user.SID)
        print "When created:         %s" % dsGetDSTimeStampStr(user.WhenCreated)
        print "When changed:         %s" % dsGetDSTimeStampStr(user.WhenChanged)
        print "Account expires:      %s" % dsGetDSTimeStampStr(user.AccountExpires)
        print "Password last set:    %s" % dsGetDSTimeStampStr(user.PasswordLastSet)
        print "Last logon:           %s" % dsGetDSTimeStampStr(user.LastLogon)
        print "Last logon timestamp: %s" % dsGetDSTimeStampStr(user.LastLogonTimeStamp)
        print "Bad password time     %s" % dsGetDSTimeStampStr(user.BadPwdTime)
        print "Logon count:          %d" % user.LogonCount
        print "Bad password count:   %d" % user.BadPwdCount
        print "User Account Control:"
        for uac in user.getUserAccountControl():
            print "\t%s" % uac
        print "Ancestors:"
        ancestorlist = user.getAncestors(db)
        sys.stdout.write("\t")
        for ancestor in ancestorlist:
            sys.stdout.write("%s " % ancestor.Name)
        sys.stdout.write("\n")
        sys.stdout.flush()

        if pwdump == True:
            print "Password hashes:"
            (lm, nt) = user.getPasswordHashes()
            if nt != '':
                print "\t%s:$NT$%s:::" % (user.Name, nt)
                if lm != '':
                    print "\t%s:%s:::" % (user.Name, lm)
        
        if pwhdump == True:
            print "Password history:"
            lmhistory = None
            nthistory = None
            (lmhistory, nthistory) = user.getPasswordHistory()
            if nthistory != None:
                hashid = 0
                for nthash in nthistory:
                    print "\t%s_nthistory%d:$NT$%s:::" % (user.Name, hashid, nthash)
                    hashid += 1
                if lmhistory != None:
                    hashid = 0
                    for lmhash in lmhistory:
                        print "\t%s_lmhistory%d:%s:::" % (user.Name, hashid, lmhash)
                        hashid += 1
        
        if certdump == True and user.Certificate != "":
            print "Certificate:"
            print dump(user.Certificate,16,16)
            
        if suppcreddump == True:
            creds = ""
            creds = user.getSupplementalCredentials()
            if creds != "":
                print "Supplemental credentials:\n"
                print dump(creds, 16, 16)
        
        
        if grpdump == True:
            print "Member of:"
            if user.PrimaryGroupID != -1:
                for g in groups:
                    if g.SID.RID == user.PrimaryGroupID:
                        print "\t%s (%s) (P)" % (g.Name, str(g.SID))
            grouplist = user.getMemberOf()
            for groupdata in grouplist:
                (groupid, deltime) = groupdata
                group = None
                group = dsGroup(db, groupid)
                if deltime == -1:
                    print "\t%s (%s)" % (group.Name, group.SID)
                else:
                    print "\t%s (%s) - Deleted: %s" % (group.Name, group.SID, 
                                dsGetDSTimeStampStr(dsConvertToDSTimeStamp(deltime)))