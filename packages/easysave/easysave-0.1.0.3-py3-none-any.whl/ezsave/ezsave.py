import os
import json
import cryptocode
files= {}

def add_to_dicts(file: str, value,name):  #adds the value to the specified "file" which is just a dictionary
    #checking if the dictionary wheech in we well save the data exists
    if file in files:
        #adds the value to the dicitionary
        files[file][name] = value
    else:
        #creates the dictionary for the data and adds the value to it
        exec(f"var_{file} = {{}}")
        files[file] = eval(f"var_{file}")
        files[file][name]=value
def json_and_save(passw=None):  #takes all the data, turnes it to json and encrypts it
    #sets defult encription key if no key provided
    if passw==None:
        passw="jhsdyuweikdi6784hfdsffjgdfusdjghe7iusy%$^%^yhjert87wyurh"
    #coverts to json
    jsonfile=json.dumps(files, sort_keys=True, indent=4)
    #encrypts
    encoded = cryptocode.encrypt(jsonfile, passw)
    #writing to the file
    f=open("ezsavetodata.json","w")
    f.write(encoded)
    f.close()
def decrypt_and_read(passw=None):  #decrypts the files, and converts to dictionary
    # sets defult encription key if no key provided
    if passw==None:
        passw="jhsdyuweikdi6784hfdsffjgdfusdjghe7iusy%$^%^yhjert87wyurh"
    f=open("ezsavedata.json","r")
    #decodeing
    decoded = cryptocode.decrypt(f.read(), passw)
    #converts to dictionary
    files=json.loads(decoded)
    return files
def clear(clearfile:bool):
    files={}
    if (clearfile==True):
        os.remove("ezsavedata.json")