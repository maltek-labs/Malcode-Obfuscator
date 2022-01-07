# Malcode-Obfuscator v0.1.0
Website: https://maltek-labs.com                                   
# 

In progress code obfuscator for obfuscating malicious scripts to be used in red team operations for validating security controls. This script assists in the automation of preparing scripts for use in evading potential detections by AV and other security solutions by utilizing popular obfuscation methods used by Malicious actors. 

# Instructions:
1. Run Malcode-Obfuscator by supplying the input file switch (-i) with PATH to file and the type of script to be used. IE: ./MalCode-Obfuscator.py -i "MalCode-Obfuscator\src\test.file" -ps

# Script types Supported:
- PowerShell

# Features:
- Polymorphic obfuscation: No two runs are the same. 
- Obfuscates variables and function names with randomly generated Upper/Lower case letters of varying sizes. 
- Removes comments
- Removes console output commands and error output commands with random strings of different lengths (Supporting of only PowerShell Scripts as of this time.)

# Upcoming Features:
- Other script types: JS, VBA, Python, etc
- Other obfuscation methods unique to script types. 
