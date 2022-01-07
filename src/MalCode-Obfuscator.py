#!/usr/bin/env python

import sys, argparse, re, pathlib, os, random, string

parser = argparse.ArgumentParser(description='Malicious Code Obfuscator', prog='MalCode-Obfuscator', add_help=False)

# CMDLine arguments to be passed
parser.add_argument('-h','--help', action='store_true')
parser.add_argument("-i", '--input', help="PATH to malicious script.", type=str)
parser.add_argument("-ps", '--PowerShell', help="Switch for PowerShell Obfuscation", action='store_true')
parser.add_argument('--version', action='version', version='%(prog)s 0.1.0')

# Set up arguments
args = vars(parser.parse_args())
ifile = args['input']
helpme = args['help']
ArgPS = args['PowerShell']


os.chdir(sys.path[0])

def Help(helpme):
    if helpme:

        ###############################################################################################################
        print( 
                        '''
                        #######################################################################################
                        #███╗   ███╗ █████╗ ██╗  ████████╗███████╗██╗  ██╗    ██╗      █████╗ ██████╗ ███████╗#
                        #████╗ ████║██╔══██╗██║  ╚══██╔══╝██╔════╝██║ ██╔╝    ██║     ██╔══██╗██╔══██╗██╔════╝#
                        #██╔████╔██║███████║██║     ██║   █████╗  █████╔╝     ██║     ███████║██████╔╝███████╗#
                        #██║╚██╔╝██║██╔══██║██║     ██║   ██╔══╝  ██╔═██╗     ██║     ██╔══██║██╔══██╗╚════██║#
                        #██║ ╚═╝ ██║██║  ██║███████╗██║   ███████╗██║  ██╗    ███████╗██║  ██║██████╔╝███████║#
                        #╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚═╝   ╚══════╝╚═╝  ╚═╝    ╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝#
                        #######################################################################################
                        #                           https://maltek-labs.com                                   #
                        #                       -Protection begins with analysis-                             #
                        #                                                                                     #
                        #                     Maltek Labs Malicious Code Obfuscator                           #
                        #######################################################################################
                        # optional arguments:                                                                 #
                        #   -h, --help            Show this help message and exit                             #
                        #   --version             Show program's version number and exit.                     #      
                        #                                                                                     #
                        # required arguments:                                                                 #
                        #   -i INPUT, --input INPUT                                                           #
                        #                            PATH to malicious script.                                #
                        #                                                                                     #
                        #######################################################################################
                        '''
                        )
        ###############################################################################################################
        exit()
    elif not ifile:
        print('\n-i is required to run script. Please input -i proceeded by the path to the script.\n')
        exit()

def PS(ifile):

    with open(ifile, 'r') as r:
        data = r.read()

    DataArray = data.splitlines()

    try:
        OldData = data
        
        # Regex for multiline comments
        StartCommentRegex = r'(^\s*<#)'
        EndCommentRegex = r'(^\s*#>)'
        SingleLineRegex = r'^\s*#.*'
        
        if (re.search(StartCommentRegex, data) and re.search(EndCommentRegex, data)) or re.search(SingleLineRegex, data):
            print('\nAttempting to remove comments:')
            
            if re.search(StartCommentRegex, data) and re.search(EndCommentRegex, data):

                # Array to handle data to be removed
                NewArray = []

                # Multiline comment removal section
                MultiComment = False
                for item in DataArray:
                    if re.search(StartCommentRegex, item):
                        NewArray.append(item)
                        MultiComment = True
            
                    elif re.match(EndCommentRegex, item):
                        
                        NewArray.append(item)
                        MultiComment = False
                        break

                    elif MultiComment == True:
                        NewArray.append(item)

                for item in NewArray:
                    DataArray.remove(item)
                
                NewArray.clear()
                Multi = True

            # Single line comment removal section
            if re.search(SingleLineRegex, data):
                for item in DataArray:
                    if re.search(SingleLineRegex, item):
                        DataArray.remove(item)
                Single = True
            
            # Join data together
            data = "\n".join(DataArray)
            if Multi or Single:
                print('Comments have been removed successfully.')
                print('\n####################################################\n')
        else: 
            print('\nNo comments detected.')
            print('\n####################################################\n')
    except:
        print('\nThere was an error during removing comments. Restoring data before continuing.')
        print('####################################################\n')
        data = OldData

    
    
    try:
        OldData = data
        print('Attempting to replace variables with random names')

        # Rename variables to randomly generated names
        UpperLetters = string.ascii_uppercase
        LowerLetters = string.ascii_lowercase
        
        
        PS_Defined_Var = ['$$', '$?', '$^','$_', '$args', '$ConsoleFileName', '$Error', '$Event', '$EventArgs', '$EventSubscriber', '$ExecutionContext', '$false', '$foreach', '$HOME', '$Host', '$input', '$IsCoreCLR', '$IsLinux', '$IsMacOS', '$IsWindows', '$LastExitCode', '$Matches', '$MyInvocation', '$NestedPromptLevel', '$null', '$PID', '$PROFILE', '$PSBoundParameters', '$PSCmdlet', '$PSCommandPath', '$PSCulture', '$PSDebugContext', '$PSHOME', '$PSItem', '$PSScriptRoot', '$PSSenderInfo', '$PSUICulture', '$PSVersionTable', '$PWD', '$Sender', '$ShellId', '$StackTrace', '$switch', '$this', '$true', '$ErrorActionPreference', '$IMAGE_FILE_MACHINE']

        NewArray = re.findall(r'\$\b\w{1,}\b', data)
        DupeData = []
        RandomArray = []

        for item in NewArray:
            if item in PS_Defined_Var:
                pass
            else:
                if item not in DupeData:
                    VariableName = re.match(r'\$\b(\w{1,})\b', item).group(1)
                    DupeData.append(item)
                    NameLength = random.randint(4,16)
                    RandomVariableName = ''.join(random.choice(UpperLetters + LowerLetters) for i in range(NameLength))
                    
                    
                    while RandomVariableName not in RandomArray:                 
                        if RandomVariableName not in RandomArray:
                            RandomArray.append(RandomVariableName)
                            data = re.sub(rf'\$\b{VariableName}\b', f'${RandomVariableName}', data)
                        else:
                            NameLength = random.randint(4,16)
                            RandomVariableName = ''.join(random.choice(UpperLetters + LowerLetters) for i in range(NameLength))
        DupeData.clear()
        print('Variables have been replaced with random names successfully')
        print('\n####################################################\n')
    except:
        print('\nThere was an error during replacing variables with random names. Restoring data before continuing.')
        print('\n####################################################\n')
        data = OldData

    try:
        OldData = data
        
        if re.search(r'function (?:\w{1,}:)?\b(.*)\b\s', data):
            print('Attempting to replace function names with random names.')

            # Renames Functions to Random names
            NewArray = re.findall(r'function (?:\w{1,}:)?\b(.*)\b\s', data)
            DupeData = []
            RandomArray = []

            for item in NewArray:
                if item not in DupeData:
                    DupeData.append(item)
                    NameLength = random.randint(4,16)
                    RandomFunctionName = ''.join(random.choice(UpperLetters + LowerLetters) for i in range(NameLength))

                    while RandomFunctionName not in RandomArray:                 
                        if RandomFunctionName not in RandomArray:
                            RandomArray.append(RandomFunctionName)
                            data = re.sub(item, RandomFunctionName, data)
                        else:
                            NameLength = random.randint(4,16)
                            RandomFunctionName = ''.join(random.choice(UpperLetters + LowerLetters) for i in range(NameLength))
            DupeData.clear()

            print('Functions have been replaced with random names successfully')
            print('\n####################################################\n')
        else: 
            print('No functions detected.')
            print('\n####################################################\n')
    except:
        print('\nThere was an error during replacing functions with random names. Restoring data before continuing.')
        print('####################################################\n')
        data = OldData


    try:
        OldData = data
        if re.search(r'(?:Throw|Write-Verbose)\s[\'\"](.*)[\'\"]', data):
        
            print('Attempting to replace error & verbose strings with random content.')

            # Removes error & verbose strings and replaces with random content that do not contain '$' within string.
            NewArray = re.findall(r'(?:Throw|Write-Verbose)\s[\'\"](.*)[\'\"]', data)
            DupeData = []
            RandomArray = []

            for item in NewArray:
                if item not in DupeData:
                    DupeData.append(item)
                    NameLength = random.randint(20,32)
                    RandomString = ''.join(random.choice(UpperLetters + LowerLetters) for i in range(NameLength))
                    
                    
                    while RandomString not in RandomArray:                 
                        if RandomString not in RandomArray:
                            RandomArray.append(RandomString)
                            data = re.sub(item, RandomString, data)
                        else:
                            NameLength = random.randint(20,32)
                            RandomString = ''.join(random.choice(UpperLetters + LowerLetters) for i in range(NameLength))
            DupeData.clear()
            print('Throw or write-output strings have been replaced successfully')
            print('\n####################################################\n')
        else:
            print('No Throw Commands or write-output strings detected.')
            print('\n####################################################\n')
    except:
        print('\nThere was an error during replacing strings with random names. Restoring data before continuing.')
        print('\n####################################################\n')
        data = OldData

    return data

if __name__ == "__main__":
    
    # Writes help document if -h is provided in arguments.
    Help(helpme)

    if ArgPS:
        data = PS(ifile)

        with open('result.file', 'w+') as w:
            w.write(data)

        print('Script Completed successfully. Press enter to exit.')
        input()
    else:
        print('No script type selected in arguments. Please provide the script type to be processed. Use -h for help on proper usage.')
    