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
from binascii import *
from ntds.dsdatabase import *
from ntds.dsrecord import *
from ntds.dsobjects import *
from ntds.dstime import *

def usage():
    print "DSComputers"
    print "Extracts information related to computer objects\n"
    print "usage: %s <datatable> [option]" % sys.argv[0]
    print "  options:"
    print "    --name <computer name>"
    print "    --passwordhashes <system hive>"
    print "    --passwordhistory <system hive>"
    print "    --bitlocker"

if len(sys.argv) < 2:
    usage()
    sys.exit(1)

name = ""
syshive = ""
pwdump = False
pwhdump = False
bitldump = False
optid = 0
for opt in sys.argv:
    if opt == "--name":
        if len(sys.argv) < 5:
            usage()
            sys.exit(1)
        name = sys.argv[optid + 1]
        print "Computer name: %s" % name
    if opt == "--passwordhashes":
        if len(sys.argv) < 4:
            usage()
            sys.exit(1)
        syshive = sys.argv[optid + 1]
        pwdump = True
        print "Extracting password hashes"
    if opt == "--passwordhistory":
        if len(sys.argv) < 4:
            usage()
            sys.exit(1)
        syshive = sys.argv[optid + 1]
        pwhdump = True
        print "Extracting password history"
    if opt == "--bitlocker":
        bitldump = True
        print "Extracting BitLocker recovery information"
    optid += 1 

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

db = dsInitDatabase(sys.argv[1])

print "\nList of computers:"
print "=================="
for recordid in dsMapLineIdByRecordId:
    if int(dsGetRecordType(db, recordid)) == dsGetTypeIdByTypeName(db, "Computer"):
        computer = dsComputer(db, recordid)
        if len(sys.argv) > 3:
            if sys.argv[2] == "--name" and computer.Name != sys.argv[3]:
                computer = None
                continue
        print "\nRecord ID: %d" % computer.RecordId
        print "Computer name: %s" % computer.Name
        print "DNS name:        %s" % computer.DNSHostName
        print "GUID: %s" % str(computer.GUID)
        print "SID:  %s" % str(computer.SID)
        print "OS name:    %s" % computer.OSName
        print "OS version: %s" % computer.OSVersion
        print "When created: %s" % dsGetDSTimeStampStr(computer.WhenCreated)
        print "When changed: %s" % dsGetDSTimeStampStr(computer.WhenChanged)
        
        if pwdump == True:
            print "Password hashes:"
            (lm, nt) = computer.getPasswordHashes()
            if nt != '':
                print "\t%s:$NT$%s:::" % (computer.Name, nt)
                if lm != '':
                    print "\t%s:%s:::" % (computer.Name, lm)
        
        if pwhdump == True:
            print "Password history:"
            lmhistory = None
            nthistory = None
            (lmhistory, nthistory) = computer.getPasswordHistory()
            if nthistory != None:
                hashid = 0
                for nthash in nthistory:
                    print "\t%s_nthistory%d:$NT$%s:::" % (computer.Name, hashid, nthash)
                    hashid += 1
                if lmhistory != None:
                    hashid = 0
                    for lmhash in lmhistory:
                        print "\t%s_lmhistory%d:%s:::" % (computer.Name, hashid, lmhash)
                        hashid += 1
        
        if bitldump == True:
            print "Recovery informations"
            for rinfo in computer.getRecoveryInformations(db):
                print "\t" + rinfo.Name
                print "\tRecovery GUID: " + str(rinfo.RecoveryGUID)
                print "\tVolume GUID:   " + str(rinfo.VolumeGUID)
                print "\tWhen created: " + dsGetDSTimeStampStr(rinfo.WhenCreated)
                print "\tWhen changed: " + dsGetDSTimeStampStr(rinfo.WhenChanged)
                print "\tRecovery password: " + rinfo.RecoveryPassword
                print "\tFVE Key package:\n" + dump(unhexlify(rinfo.FVEKeyPackage),16, 16)
                print "\n"
        computer = None