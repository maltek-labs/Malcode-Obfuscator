#!/usr/bin/env python
import sys, argparse, re, os, random, string, base64


parser = argparse.ArgumentParser(description='Malicious Code Obfuscator', prog='MalCode-Obfuscator', add_help=False)

# CMDLine arguments to be passed
parser.add_argument('-h','--help', action='store_true')
parser.add_argument("-i", '--input', help="Input PATH to script to read in.", type=str)
parser.add_argument("-o", '--output', help="Output PATH with file name + extension.", type=str)
parser.add_argument("-ps", '--PowerShell', help="Switch for PowerShell Obfuscation", action='store_true')
parser.add_argument("-d", '--Decoy', help="Switch creating decoys in script", action='store_true')
parser.add_argument('--version', action='version', version='%(prog)s 0.2.0')

# Set up arguments
args = vars(parser.parse_args())
ifile = args['input']
ofile = args['output']
helpme = args['help']
ArgPS = args['PowerShell']
Decoy = args['Decoy']


os.chdir(sys.path[0])

def Help():
    
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
                    #   -h, --help            Show this help message and exit.                            #
                    #   --version             Show program's version number and exit.                     #      
                    #   -ps --PowerShell      Switch for obfuscating PowerShell scripts.                  #
                    #   -d -Decoy             Switch to add various types of decoys                       #
                    #                                                                                     #
                    # required arguments:                                                                 #
                    #   -i INPUT, --input Input PATH to script to read in.                                #
                    #   -o INPUT, --output Output PATH with file name + extension.                        #
                    #                                                                                     #
                    #                                                                                     #
                    #######################################################################################
                    '''
                    )
    ###############################################################################################################
        
    print('\n Example use:  .\MalCode-Obfuscator.py -i PATH -o PATH -ps\n Press ENTER to exit.')

class PowerShell:

    def RemoveComments(data):

        # Attempts to remove Comments
        try:
            OldData = data
            
            # Regex for comments
            BlockCommentRegex = r'(<#[\s\w\W]{1,}#>)'
            SingleLineRegex = r'#.*\n'

            if (re.search(BlockCommentRegex, data) or re.search(SingleLineRegex, data)):
                
                # Block Comment removal section
                if re.search(BlockCommentRegex, data):
                    BlockComment = re.search(BlockCommentRegex, data).group(1)
                    BlockComment = BlockComment.splitlines()
                    
                    for item in BlockComment:
                        item = re.escape(item)
                        newdata = re.sub(rf'{item}','', data)
                        data = newdata
                        
                
                # Single line comment removal section
                CommentArray = re.findall(SingleLineRegex, data)
                
                for item in CommentArray:
                    EscapedString = re.escape(item)
                    newdata = re.sub(rf'{EscapedString}','\n', data)
                    data = newdata
                    
                # Data clean up
                data = re.sub(r'\n{2,}', '\n', data)

                print('Comments have been removed successfully.')
                print('\n####################################################\n')
            else: 
                print('\nNo comments detected.')
                print('\n####################################################\n')
        except Exception as Error:
            print('\nThere was an error during removing comments. Restoring data before continuing.')
            print('####################################################\n')
            data = OldData

            print(Error)

        return data

    def IOC_Obfuscator(data):
        try: 
            UrlVarRegex = r'https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)'
            IPAddressVarRegex = r'(?:\$\w{1,} ?= ?)?[\"\']((?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))[\"\']'
            
            if re.search(UrlVarRegex, data) or re.search(IPAddressVarRegex, data):
                if re.search(UrlVarRegex, data):
                    UrlList = re.findall(UrlVarRegex, data)
                    VarNameArray = []
                    FunctionValueArray = []
                    VarValueArray = []
                    NameArray = []
                    TotalIndex = 0
                    IndexValue = 0
                    UpperLetters = string.ascii_uppercase
                    LowerLetters = string.ascii_lowercase
                    
                    for URLValue in UrlList: 
                        data = data.splitlines()
                        URLEncoded = URLValue.encode('ascii')
                        URLEncoded = str(base64.b64encode(URLEncoded))
                        URLEncoded = re.sub(r'b\'', '', URLEncoded)
                        URLEncoded = re.sub(r'\'', '', URLEncoded)
                        
                        # Sets up list of base64 encoded URL
                        Base64_Array = [char for char in URLEncoded]
                        
                        # Generates functions, Varable names, and values. 
                        for item in Base64_Array:
                            #Random Function generion for IOCs
                            NameLength = random.randint(1,2)
                            IndexMax = random.randint(4,16)
                            i = 0
                            while i <= IndexMax:
                                FirstSection = (random.choice(UpperLetters + LowerLetters) for i in range(NameLength))
                                SecondSection = random.randint(0,9)
                                
                                UpdatedName = ''.join(FirstSection)
                                UpdatedName = UpdatedName + str(SecondSection)
                                
                                NameArray.append(UpdatedName)
                                i += 1
                                if i == IndexMax:
                                    RandomFunctName = ''.join(NameArray)
                                    NameArray.clear()
                                    FunctionValueArray.append(f'function {RandomFunctName} {{ return \'{item}\' }};')
                            
                            
                            #Random Variable names for IOCs
                            NameLength = random.randint(1,2)
                            IndexMax = random.randint(4,16)
                            i = 0
                            while i <= IndexMax:
                                FirstSection = (random.choice(UpperLetters + LowerLetters) for i in range(NameLength))
                                SecondSection = random.randint(0,9)
                                
                                UpdatedName = ''.join(FirstSection)
                                UpdatedName = UpdatedName + str(SecondSection)
                                
                                NameArray.append(UpdatedName)
                                i += 1
                                if i == IndexMax:
                                    RandomVarName = ''.join(NameArray)
                                    NameArray.clear()
                                    VarValueArray.append(f'${RandomVarName} = {RandomFunctName}')
                                    VarNameArray.append(f'${RandomVarName}')
                            
                            IndexValue += 1

                        # Inserts Generated functions into beggining of file. 
                        for item in FunctionValueArray:
                            Value = FunctionValueArray.index(item)
                            data.insert(Value, item)
                            TotalIndex += 1

                        for item in VarValueArray:
                            data.insert(TotalIndex, item)
                            TotalIndex += 1

                        VarNameCombined = " + ".join(VarNameArray)

                        # Generates the random name for storing the combined data.
                        NameLength = random.randint(1,2)
                        IndexMax = random.randint(4,16)
                        i = 0
                        while i <= IndexMax:
                            FirstSection = (random.choice(UpperLetters + LowerLetters) for i in range(NameLength))
                            SecondSection = random.randint(0,9)
                            
                            UpdatedName = ''.join(FirstSection)
                            UpdatedName = UpdatedName + str(SecondSection)
                            
                            NameArray.append(UpdatedName)
                            i += 1
                            if i == IndexMax:
                                RandomVarName = ''.join(NameArray)
                                NameArray.clear()
                                data.insert(TotalIndex, f'\n${RandomVarName} = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String({VarNameCombined}));')

                        # Clean up.
                        Base64_Array.clear()
                        VarNameArray.clear()
                        data = '\n'.join(data)
                        data = re.sub(rf'[\"\']{URLValue}[\"\']', rf'${RandomVarName}', data)

                # IP Address section
                if re.search(IPAddressVarRegex, data):
                    IPList = re.findall(IPAddressVarRegex, data)
                    VarNameArray = []
                    FunctionValueArray = []
                    VarValueArray = []
                    NameArray = []
                    TotalIndex = 0
                    IndexValue = 0
                    UpperLetters = string.ascii_uppercase
                    LowerLetters = string.ascii_lowercase
                    
                    for IPValue in IPList: 
                        data = data.splitlines()
                        IPAddressEncoded = IPValue.encode('ascii')
                        IPAddressEncoded = str(base64.b64encode(IPAddressEncoded))
                        IPAddressEncoded = re.sub(r'b\'', '', IPAddressEncoded)
                        IPAddressEncoded = re.sub(r'\'', '', IPAddressEncoded)
                        
                        # Sets up list of base64 encoded URL
                        Base64_Array = [char for char in IPAddressEncoded]
                        
                        # Generates functions, Varable names, and values. 
                        for item in Base64_Array:
                            #Random Function generion for IOCs
                            NameLength = random.randint(1,2)
                            IndexMax = random.randint(4,16)
                            i = 0
                            while i <= IndexMax:
                                FirstSection = (random.choice(UpperLetters + LowerLetters) for i in range(NameLength))
                                SecondSection = random.randint(0,9)
                                
                                UpdatedName = ''.join(FirstSection)
                                UpdatedName = UpdatedName + str(SecondSection)
                                
                                NameArray.append(UpdatedName)
                                i += 1
                                if i == IndexMax:
                                    RandomFunctName = ''.join(NameArray)
                                    NameArray.clear()
                                    FunctionValueArray.append(f'function {RandomFunctName} {{ return \'{item}\' }};')
                            
                            
                            #Random Variable names for IOCs
                            NameLength = random.randint(1,2)
                            IndexMax = random.randint(4,16)
                            i = 0
                            while i <= IndexMax:
                                FirstSection = (random.choice(UpperLetters + LowerLetters) for i in range(NameLength))
                                SecondSection = random.randint(0,9)
                                
                                UpdatedName = ''.join(FirstSection)
                                UpdatedName = UpdatedName + str(SecondSection)
                                
                                NameArray.append(UpdatedName)
                                i += 1
                                if i == IndexMax:
                                    RandomVarName = ''.join(NameArray)
                                    NameArray.clear()
                                    VarValueArray.append(f'${RandomVarName} = {RandomFunctName}')
                                    VarNameArray.append(f'${RandomVarName}')
                            
                            IndexValue += 1

                        # Inserts Generated functions into beggining of file. 
                        for item in FunctionValueArray:
                            Value = FunctionValueArray.index(item)
                            data.insert(Value, item)
                            TotalIndex += 1

                        for item in VarValueArray:
                            data.insert(TotalIndex, item)
                            TotalIndex += 1

                        VarNameCombined = " + ".join(VarNameArray)

                        # Generates the random name for storing the combined data.
                        NameLength = random.randint(1,2)
                        IndexMax = random.randint(4,16)
                        i = 0
                        while i <= IndexMax:
                            FirstSection = (random.choice(UpperLetters + LowerLetters) for i in range(NameLength))
                            SecondSection = random.randint(0,9)
                            
                            UpdatedName = ''.join(FirstSection)
                            UpdatedName = UpdatedName + str(SecondSection)
                            
                            NameArray.append(UpdatedName)
                            i += 1
                            if i == IndexMax:
                                RandomVarName = ''.join(NameArray)
                                NameArray.clear()
                                data.insert(TotalIndex, f'\n${RandomVarName} = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String({VarNameCombined}));')

                        # Clean up. 
                        Base64_Array.clear()
                        VarNameArray.clear()
                        data = "\n".join(data)
                        data = re.sub(rf'[\"\']{IPValue}[\"\']', rf'${RandomVarName}', data)
                    
        except Exception as Error:
            print('An unexpected error has occured: ' + Error)
            print('Press enter to exit script.')
            input()
        
        return data

    def VariableObfuscate(data):    
        # Rename variables to randomly generated names
        try:
            OldData = data

            UpperLetters = string.ascii_uppercase
            LowerLetters = string.ascii_lowercase

            PS_Defined_Var = ['$$', '$?', '$^','$_', '$args', '$ConsoleFileName', '$Error', '$Event', '$EventArgs', '$EventSubscriber', '$ExecutionContext', '$false', '$foreach', '$HOME', '$Host', '$input', '$IsCoreCLR', '$IsLinux', '$IsMacOS', '$IsWindows', '$LastExitCode', '$Matches', '$MyInvocation', '$NestedPromptLevel', '$null', '$PID', '$PROFILE', '$PSBoundParameters', '$PSCmdlet', '$PSCommandPath', '$PSCulture', '$PSDebugContext', '$PSHOME', '$PSItem', '$PSScriptRoot', '$PSSenderInfo', '$PSUICulture', '$PSVersionTable', '$PWD', '$Sender', '$ShellId', '$StackTrace', '$switch', '$this', '$true', '$ErrorActionPreference', '$IMAGE_FILE_MACHINE', '$global']

            VarArray = re.findall(r'\$\b\w{1,}\b', data)
            NameArray = []

            for item in VarArray:
                if item not in PS_Defined_Var:
                    i = 0
                    NameLength = random.randint(1,2)
                    IndexMax = random.randint(4,16)
                    while i <= IndexMax:
                        FirstSection = (random.choice(UpperLetters + LowerLetters) for i in range(NameLength))
                        SecondSection = random.randint(0,9)
                        
                        UpdatedName = ''.join(FirstSection)
                        UpdatedName = UpdatedName + str(SecondSection)
                        
                        NameArray.append(UpdatedName)
                        i += 1
                        if i == IndexMax:
                            RandomVarName = ''.join(NameArray)
                            data = re.sub(rf'\{item}\b', f'${RandomVarName}', data)
                    NameArray.clear()
            data = re.sub(r'^\n{2}', '', data)
            print('Variables have been replaced with random names successfully')
            print('\n####################################################\n')
        except Exception as Error:
            print('An unexpected error has occured: ' + Error)
            print('\nThere was an error during replacing variables with random names. Restoring data before continuing.')
            print('\n####################################################\n')
            data = OldData

        return data

    def FunctionObfuscate(data):
        # Replaces functon names with random values
        try:
            OldData = data
            UpperLetters = string.ascii_uppercase
            LowerLetters = string.ascii_lowercase

            if re.search(r'function \b(.*?)\b[ {(]', data):

                # Renames Functions to Random names
                FunctionArray = re.findall(r'function \b(.*?)\b[ {(]', data)
                NameArray = []

                for item in FunctionArray:
                    i = 0
                    NameLength = random.randint(1,2)
                    IndexMax = random.randint(4,16)
                    while i <= IndexMax:
                        FirstSection = (random.choice(UpperLetters + LowerLetters) for i in range(NameLength))
                        SecondSection = random.randint(0,9)
                        
                        UpdatedName = ''.join(FirstSection)
                        UpdatedName = UpdatedName + str(SecondSection)
                        
                        NameArray.append(UpdatedName)
                        i += 1
                        if i == IndexMax:
                            RandomFunctionName = ''.join(NameArray)
                            data = re.sub(rf'{item}\b', RandomFunctionName, data)
                    NameArray.clear()
                
                data = re.sub(r'^\n{2}', '', data)
                print('Functions have been replaced with random names successfully')
                print('\n####################################################\n')
            else: 
                print('No functions detected.')
                print('\n####################################################\n')
        except Exception as Error:
            print('An unexpected error has occured: ' + Error)
            print('\nThere was an error during replacing functions with random names. Restoring data before continuing.')
            print('####################################################\n')
            data = OldData

        return data

    def OutputMessagesObfuscate(data):
        try:
            OldData = data
            UpperLetters = string.ascii_uppercase
            LowerLetters = string.ascii_lowercase
            
            if re.search(r'(?:Throw|Write-Verbose)\s[\'\"](.*)[\'\"]', data):
            

                # Removes error & verbose strings and replaces with random content that do not contain '$' within string.
                NewArray = re.findall(r'(?:Throw|Write-Verbose)\s[\'\"](.*)[\'\"]', data)
                DupeData = []
                RandomArray = []

                for item in NewArray:
                    if item not in DupeData:
                        DupeData.append(item)
                        NameLength = random.randint(4,32)
                        RandomString = ''.join(random.choice(UpperLetters + LowerLetters) for i in range(NameLength))
                        
                        
                        while RandomString not in RandomArray:                 
                            if RandomString not in RandomArray:
                                RandomArray.append(RandomString)
                                data = re.sub(item, RandomString, data)
                            else:
                                NameLength = random.randint(4,32)
                                RandomString = ''.join(random.choice(UpperLetters + LowerLetters) for i in range(NameLength))
                DupeData.clear()
                data = re.sub(r'^\n{2}', '', data)

                print('Throw or write-output strings have been replaced successfully')
                print('\n####################################################\n')
            else:
                print('No Throw Commands or write-output strings detected.')
                print('\n####################################################\n')
        except Exception as Error:
            print('An unexpected error has occured: ' + Error)
            print('\nThere was an error during replacing strings with random names. Restoring data before continuing.')
            print('\n####################################################\n')
            data = OldData

        return data
    
    def Decoy(data):
        data = data.splitlines()
        UpperLetters = string.ascii_uppercase
        LowerLetters = string.ascii_lowercase
        NameLength = random.randint(1,2)
        NameArray = []
        VarValueArray = []
        FunctionValueArray = []
        VarNameArray = []
        b64Array = []
       
        print('''\nPlease enter the type(s) of decoy(s) to create in space delimited format:
        
        -var      Generates variables like below: 
                    $n6D8J4Z0L = $X0t1x5F9
        
        -fun      Generates functions like below: 
                    function v6J3o4I5r4 { return 'j' };
        
        -b64      Generates false base64 string conversion methods like below: 
                    $qA4TD8cU7dU0ba = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($n6D9J4Z0 + $j1k2X9c + $Ve2UI5)
                    \n''')
        
        UserInput = input()
        UserInputList = UserInput.split(' ')

        for item in UserInputList:
            if item == '-var':
                print(f'\nPlease enter in the value for the amount of variables to create.')
                DecoyVarAmount = int(input())
            if item == '-fun':
                print(f'\nPlease enter in the value for the amount of functions to create.')
                DecoyFunAmount = int(input())
            if item == '-b64':
                print(f'\nPlease enter in the value for the amount of false b64 methods to create.')
                Decoyb64Amount = int(input())


        for item in UserInputList:
            #Random Variable names generator
            if item == '-var':
                z = 1
                
                while z <= DecoyVarAmount: 
                    IndexMax = random.randint(4,16)
                    i = 0
                    
                    while i <= IndexMax:
                        FirstSection = (random.choice(UpperLetters + LowerLetters) for i in range(NameLength))
                        SecondSection = random.randint(0,9)
                        
                        UpdatedName = ''.join(FirstSection)
                        UpdatedName = UpdatedName + str(SecondSection)
                        
                        NameArray.append(UpdatedName)
                        i += 1
                        if i == IndexMax:
                            RandomVarName = ''.join(NameArray)
                            NameArray.clear()
                            
                    IndexMax = random.randint(4,16)
                    x = 0
                    
                    while x <= IndexMax:
                        FirstSection = (random.choice(UpperLetters + LowerLetters) for i in range(NameLength))
                        SecondSection = random.randint(0,9)
                        
                        UpdatedName = ''.join(FirstSection)
                        UpdatedName = UpdatedName + str(SecondSection)
                        
                        NameArray.append(UpdatedName)
                        x += 1
                        if x == IndexMax:
                            RandomName = ''.join(NameArray)
                            NameArray.clear()
                    VarValueArray.append(f'${RandomVarName} = ${RandomName}')
                    
                    
                    z += 1
                
                
                for VarValue in VarValueArray:
                    data.insert(random.randint(0,10), VarValue)

            # Generates functions and values. 
            if item == '-fun':
                
                i = 1                                   
                while i <= DecoyFunAmount:
                    #Random Function generion
                    NameLength = random.randint(1,2)
                    IndexMax = random.randint(4,16)
                    
                    x = 0
                    while x <= IndexMax:
                        FirstSection = (random.choice(UpperLetters + LowerLetters) for i in range(NameLength))
                        SecondSection = random.randint(0,9)
                        
                        UpdatedName = ''.join(FirstSection)
                        UpdatedName = UpdatedName + str(SecondSection)
                        
                        NameArray.append(UpdatedName)
                        x += 1
                        if x == IndexMax:
                            RandomFunctName = ''.join(NameArray)
                            NameArray.clear()
                            FunctionValueArray.append(f'function {RandomFunctName} {{ return \'{random.choice(UpperLetters + LowerLetters)}\' }};')
                    i += 1
                
                for FunValue in FunctionValueArray:
                    data.insert(random.randint(0,10), FunValue)
            
            if item == '-b64':    
                z = 1
                while z <= Decoyb64Amount: 
                    IndexMax = random.randint(4,16)
                    
                    i = 0
                    while i <= IndexMax:
                        FirstSection = (random.choice(UpperLetters + LowerLetters) for i in range(NameLength))
                        SecondSection = random.randint(0,9)
                        
                        UpdatedName = ''.join(FirstSection)
                        UpdatedName = UpdatedName + str(SecondSection)
                        
                        NameArray.append(UpdatedName)
                        i += 1
                        if i == IndexMax:
                            RandomVarName = ''.join(NameArray)
                            NameArray.clear()
                            
                    RandomVarNum = random.randint(10,32)
                    x = 0
                    while x <= RandomVarNum:
                        
                        IndexMax = random.randint(2,8)
                        y = 0
                        while y <= IndexMax:
                        
                            FirstSection = (random.choice(UpperLetters + LowerLetters) for i in range(NameLength))
                            SecondSection = random.randint(0,9)
                            
                            UpdatedName = ''.join(FirstSection)
                            UpdatedName = UpdatedName + str(SecondSection)
                            
                            NameArray.append(UpdatedName)
                            y += 1
                            if y == IndexMax:
                                RandomName = ''.join(NameArray)
                                VarNameArray.append(f'${RandomName}')
                                NameArray.clear()
                        x += 1
                    VarNamelist = " + ".join(VarNameArray)
                    VarNameArray.clear()
                    b64Array.append(f'\n${RandomVarName} = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String({VarNamelist}));')
                    z += 1
                    
            
        for b64Value in b64Array:    
            data.insert(random.randint(0,10), b64Value)

        data = "\n".join(data)
        data = re.sub(r';', ';\n', data)
        data = re.sub(r'^\n{2}', '', data)

        return data


if __name__ == "__main__":
    
    # Writes help document if -h is provided in arguments.
    
    if  helpme:
        Help()
    
    elif ArgPS:
        with open(ifile, 'r') as r:
            data = r.read()
        r.close()
        
        print('''\nPlease select any of the following to execute in the following format with space delimited. (IE: -ioc -rc -fo):\n 
        -ioc    Obfuscates any IP/URLs found by encoding in Base64 then splitting up IOCs into multiple functions with random names and a single character return value.
        -rc     Removes any comments (single line or blocks) from inputted ifile.
        -fo     Obfuscates Functions with random names in varying lengths.
        -vo     Obfuscates Variables with random names in varying lengths.
        -ro     Removes output messages and throw comments in inputted ifile. \n''')
        UserInput = input()
        UserInputList = UserInput.split(' ')
        
        if Decoy:
            data = PowerShell.Decoy(data)

        if '-ioc' in UserInputList:
            data = PowerShell.IOC_Obfuscator(data)
        
        if '-rc' in UserInputList:
            data = PowerShell.RemoveComments(data)
        
        if '-fo' in UserInputList:
            data = PowerShell.FunctionObfuscate(data)
        
        if '-vo' in UserInputList:
            data = PowerShell.OutputMessagesObfuscate(data)
        
        if '-ro' in UserInputList:
            data = PowerShell.VariableObfuscate(data)
        
            
        
        with open(f'{ofile}', 'w') as w:
            w.write(data)
        w.close()

        print(f'\nScript Completed successfully. File has been written to \'{ofile}\'. Press enter to exit.')
        input()
        exit()
    
    else:
        print('No script type selected in arguments. Please provide the script type to be processed. Use -h for help on proper usage.\n\nPress ENTER to exit.')
        Help()
        input()
        exit()