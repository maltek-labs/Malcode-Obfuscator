# Malcode-Obfuscator v0.2.0
Website: https://maltek-labs.com                                   
# 

In progress code obfuscator for obfuscating malicious scripts to be used in red team operations for validating security controls. This script assists in the automation of preparing scripts for use in evading potential detections by AV and other security solutions by utilizing popular obfuscation methods used by Malicious actors. 

# Instructions:
1. Run Malcode-Obfuscator by supplying the input file switch (-i) with PATH to file and the type of script to be used. IE: ./MalCode-Obfuscator.py -i "MalCode-Obfuscator\src\test.ps1" -o "\Somefolder\Filename.ps1" -ps

# Script types Supported:
- PowerShell

# Features:
- Polymorphic obfuscation: No two runs are the same. 
- Obfuscates variables and function names with randomly generated Upper/Lower case letters & numbers of varying sizes. 
- Removes comments
- Removes console output commands and error output commands with random strings of different lengths (Supporting of only PowerShell Scripts as of this time.)
- Obfuscates IOCs (IPs & URLs) by encoding in base64 then splitting into multiple functions. 
- Adds decoy variables, functions, and base64 conversion methods to code with the "-d" switch. 

# Upcoming Features:
- Other script types: JS, VBA, Python, etc
- Other obfuscation methods unique to script types observed by malicious actors and threat groups in the wild. 
