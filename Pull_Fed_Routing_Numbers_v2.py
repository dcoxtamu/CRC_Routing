#--- Pull_Fed_Routing_Numbers.py

#---
#--- This is a script to pull the ACH Routing codes from the Federal Reserve.
#--- You can either provide the parameters via CLI or you can provide them interactively.
#---
#--- The script requires two arguments: Organization ID and Download Code.
#--- These will be provided by the sponsoring Organization.

import re
import sys
import requests
content = ""
org_id = ""
download_cd = ""
download_list = []
cli_status = False
console_status = False
headers = {
    "X_FRB_EPAYMENTS_DIRECTORY_ORG_ID" : "",        #--- Insert your organization ID here.
    "X_FRB_EPAYMENTS_DIRECTORY_DOWNLOAD_CD" : ""    #--- Insert your download code here.
    }
#--- --- Set the following variable to the desired output format:  XML or JSON or TEXT.
return_format = 'TEXT'       # 'XML' or 'JSON' or 'TEXT', Fixed Width TEXT should be default.

#--- --- Put the Function Definitions here.  There are two functions that are used in the script.
#--- --- The first function is to check the input Organization ID (org_id).
#--- --- The second function is to check the input Download Code (download_cd).

#--- --- Validate org_id and download_cd

def check_org_id(org_id):
    if org_id.isdigit() == False:
        print ('Organization ID must be all numeric digits.')
        return False
    if len(org_id) != 9:
        print ('Organization ID must be 9 numeric digits.')
        return False
    return True

def check_download_cd(download_cd):
    if len(download_cd) != 36:
        print('download_cd entered: >', download_cd,'<')
        print ('Download code must be 36 characters including 4 hyphens.')
        return False
    download_list = re.split('-',download_cd)
    if len(download_list) != 5:
        print ('download_list has ', len(download_list), ' sections.')
        print ('Download code must have 5 sections separated by 4 hyphens.')
        return False
    if len(download_list[0]) != 8:
        print ('Download code must have 8 characters in the first section.')
        return False
    if len(download_list[1]) != 4:
        print ('Download code must have 4 characters in the second section.')
        return False  
    if len(download_list[2]) != 4:
        print ('Download code must have 4 characters in the third section.')
        return False
    if len(download_list[3]) != 4:
        print ('Download code must have 4 characters in the fourth section.')
        return False
    if len(download_list[4]) != 12:
        print ('Download code must have 12 characters in the fifth section.')
        return False
    return True
#--- --- End Validate org_id and download_cd


#--- --- Check to see if there are any Command Line Arguments
if len(sys.argv) > 1:
    if sys.argv[1] == '-h':     #--- Help option
        print ('This script pulls the ACH Routing codes from the Federal Reserve.')
        print ('The script requires three arguments: Return File Format, Organization ID and Download Code.')
        print ('The Return File Format can be XML, JSON, or TEXT.')
        print ('The Organization ID is a 9-digit number.')
        print ('The Download Code is a 32-character string in 5 sections separated by 4 hyphens.')
        print ('The first section has 8 characters, the second section has 4 characters, the third section has 4 characters, the fourth section has 4 characters, and the fifth section has 12 characters.')
        print ('The script will pull the FedWire and FedACH routing codes in the format specified.')
        print ('The formats available are XML, JSON, or Fixed Width TEXT.')
        print ('The script will write the output to a file with the appropriate extension.')
        print ('The script will also print the status code of the response.')
        print ('The script output files will be saved in the same directory as the script.')
        print ('The script will exit after the output files are written.')
        print ('Typical usage: > python Pull_Fed_Routing_Numbers_v2.py return_format org_id download_code')
        print ('           or: > python Pull_Fed_Routing_Numbers_v2.py')
        print ('                   and the program will prompt you for the return_format, org_id and download_code.')
        print ('          the typical return_format is TEXT but XML and JSON are also available.')
        print ('          the org_id is EPayments Directory ORG_ID and is 9 numeric digits.')
        print ('          the download_code is EPayments Directory Download Code and is 36 alpha-numeric characters in 5 section divided by hyphens.')
        print ('The above example will pull the routing codes in TEXT format.')
        exit()
    else:
        #--- --- There are CLI arguments. Check to see if they are valid.
        return_format = sys.argv[1].upper()
        if return_format != 'XML' and return_format != 'JSON' and return_format != 'TEXT':
            print (f'Return format must be XML, JSON, or TEXT but was: {sys.argv[1]} - Defaulting to TEXT.')
            return_format = 'TEXT'
            exit()

        org_id = sys.argv[2]
        if check_org_id(org_id) == False:
            print ('Organization ID must be 9 digits.')
            print ('You will need to restart the script with a correct Org_ID argument. Exiting.')
            exit()

        download_cd = sys.argv[3]
        if check_download_cd(download_cd) == False:
            print ('Download code must be 36 characters.')
            print ('You will need to restart the script with a correct Download_CD argument. Exiting.')
            exit()
        
        cli_status = True

else:   #--- --- sysargv has only one argument, which is the program name.
        #--- --- need to get the org_id and download_cd from the user at the console.

    # cli_status = False  <-- this is the inital state.

    #--- --- Read from the input console for ORG ID and Download CD
    rtn_form = input("Enter the desired return format (XML, JSON, or TEXT): ")
    return_format = rtn_form.upper()
    if return_format != 'XML' and return_format != 'JSON' and return_format != 'TEXT':
        print (f'Return format must be XML, JSON, or TEXT but was: {sys.argv[1]} - Defaulting to TEXT.')
        return_format = 'TEXT'

    org_id = input("Enter your Organization ID (9 numeric digits): ")
    if check_org_id(org_id) == False:
        print ('Organization ID must be 9 numeric digits. Exiting.')
        exit()
        
    download_cd = input("Enter your Download Code (32 alpha-numeric chars in 5 sections separated by 4 hyphens): ")
    if check_download_cd(download_cd) == False:
        print ('Download code must be 36 characters. Exiting.')
        exit()

    console_status = True

if cli_status == True or console_status == True:

    headers["X_FRB_EPAYMENTS_DIRECTORY_ORG_ID"] = org_id
    headers["X_FRB_EPAYMENTS_DIRECTORY_DOWNLOAD_CD"] = download_cd

    #--- --- ----------------------------- --- ---
    #--- --- FedWire directory information --- ---
    #--- --- ----------------------------- --- ---
    #---
    if return_format == 'XML':
        #--- Pull codes from FedWire in XML format
        directory = "https://frbservices.org/EPaymentsDirectory/directories/fedwire?format=xml"
        filename = "fedwire_routing_numbers.xml"

    if return_format == 'JSON':
        #--- Pull codes from FedWire in JSON format
        directory = "https://frbservices.org/EPaymentsDirectory/directories/fedwire?format=json"
        filename = "fedwire_routing_numbers.json"

    if return_format == 'TEXT':
        #--- Pull codes from FedWire in Fixed Width Text format
        directory = "https://frbservices.org/EPaymentsDirectory/directories/fedwire?format=text"
        filename = "fedwire_routing_numbers.txt"

    f = open(filename,"wt")

    #--- --- ------------------------- --- ---
    #--- --- Process FedWire directory --- ---
    #--- --- ------------------------- --- ---
    try:
        response = requests.get(directory, headers = headers)
        response.raise_for_status()       # Raise an HTTPError if response code was unsuccessful

        if response.status_code == 200:
            if return_format == 'JSON':
                content = str(response.json())
            else:
                content = response.text
            f.write(content)
            f.close()

        print('FedWire Status code is:',response.status_code)
        print('FedWire is done.')

    except requests.exceptions.HTTPError as err:
        print('Http error occurred:', err)

        if response.status_code == 204:
            print ('Download code does not exist.')

        if response.status_code == 205:
            print ('Download code has expired. Need new download code.')

        if response.status_code == 206:
            print ('Download limits have been exceeded for the day.')
            print ('You must wait for tomorrow to try again.')

        if response.status_code == 207:
            print ('The format inserted in script is not all lowercase.')

    finally:
        response.close()

        #--- --- ------------------------- --- ---
        #--- --- FedACH Directory information --- ---
        #--- --- ------------------------- --- ---
        #---
        if return_format == 'XML':
            #--- Pull codes from FedACH in XML format
            directory = "https://frbservices.org/EPaymentsDirectory/directories/fedach?format=xml"
            filename = "fedACH_routing_numbers.xml"

        if return_format == 'JSON':
            #--- Pull codes from FedACH in JSON format
            directory = "https://frbservices.org/EPaymentsDirectory/directories/fedach?format=json"
            filename = "fedACH_routing_numbers.json"

        if return_format == 'TEXT':
            #--- Pull codes from FedACH in Fixed Width Textformat
            directory = "https://frbservices.org/EPaymentsDirectory/directories/fedach?format=text"
            filename = "fedACH_routing_numbers.txt"
        
        f = open(filename,"wt")

        #--- --- Process FedACH directory --- ---
        try:
            response = requests.get(directory, headers = headers)
            response.raise_for_status()       # Raise an HTTPError if response code was unsuccessful
        
            if response.status_code == 200:
                if return_format == 'JSON':
                    content = str(response.json())
                else:
                    content = response.text
                f.write(content)
                f.close()

            print('FedACH Status code is:',response.status_code)
            print('FedACH is done.')

        except requests.exceptions.HTTPError as err:
            print('Http error occurred:', err)

            if response.status_code == 204:
                print ('Download code does not exist.')

            if response.status_code == 205:
                print ('Download code has expired. Need new download code.')

            if response.status_code == 206:
                print ('Download limits have been exceeded for the day.')
                print ('You must wait for tomorrow to try again.')

            if response.status_code == 207:
                print ('The format inserted in script is not all lowercase.')

        finally:
            response.close()

print ('Last Done.')
