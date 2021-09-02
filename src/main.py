#!/usr/bin/env python

import sys, argparse, pathlib, os


os.chdir(sys.path[0])



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
                #                  		 Maltek Labs MalCode Obfuscator		                          #
                #######################################################################################
                # optional arguments:                                                                 #
                #   -h, --help            Show this help message and exit                             #
                #   --version             Show program's version number and exit.                     #      
                #                                                                                     #
                # required arguments:                                                                 #
                #   -i INPUT, --input INPUT PATH to base64 encoded payload.							  #
				#	-o OUTPUT, --output OUTPUT PATH for completed file 								  #
                #                            						                                  #
                #                                                                                     #
                #######################################################################################
                '''
                )
###############################################################################################################

parser = argparse.ArgumentParser(description='Maltek Labs MalCode Obfuscator', prog='MalCode - Obfuscator', add_help=False)

# CMDLine arguments to be passed
parser.add_argument('-h','--help', action='store_true')
parser.add_argument("-i", '--input', help="INPUT PATH to base64 encoded payload.", type=str)
parser.add_argument("-o", '--output', help="OUTPUT PATH for completed file", type=str)
parser.add_argument('--version', action='version', version='%(prog)s 0.1')

# Set up arguments
args = vars(parser.parse_args())
ifile = args['input']
ofile = args['output']
helpme = args['help']



###############################################################################################################

    
if __name__ == "__main__":
    
    if helpme == True:
        exit()
        print('')

    
        

    
 
    print('\t######################################################################################################\n')
    print('')
    print('Script has been completed. Press enter to exit\n')
    input()
    exit()