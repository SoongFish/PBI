import os
import time
import getpass
import hashlib

username = ""
id = []
pw = []

def login(func):
    def wrapper(*args, **kwargs):
        os.system("cls")
        option = int(input("▶ Select menu\n>> 1 : Sign in\n>> 2 : Sign up\n"))
        
        if option == 1: # Sign in    
            loginDB = open("loginDB.txt", "r")
            
            for line in loginDB:
                line = line.split("\t")
                global id, pw
                id.append(line[0])
                pw.append(line[1][:-1])
                
            loginDB.close()
            
            input_id = input("\nInput ID > ")
            input_pw = getpass.getpass("Input Password > ")
            
            ## sha256 encoding
            encoded_input_id = input_id.encode()
            encoded_input_pw = input_pw.encode()
            
            if hashlib.sha256(encoded_input_id).hexdigest() in id:
                index_id = id.index(hashlib.sha256(encoded_input_id).hexdigest())
                if hashlib.sha256(encoded_input_pw).hexdigest() == pw[index_id]:
                    global username
                    username = input_id
                    return func(*args, **kwargs)
                else:
                    print("\ninvaild Password! main menu is displayed after 2 seconds.")
                    time.sleep(2)
                    wrapper()
            else: 
                print("\ninvaild ID! main menu is displayed after 2 seconds.")
                time.sleep(2)
                wrapper()
                
        elif option == 2: # Sing up
            os.system("cls")
            
            loginDB = open("loginDB.txt", "r+")
            
            newID = input("Input ID : ")
            newPW = getpass.getpass("Input PW : ")
            
            ## sha256 encoding
            encoded_newID = newID.encode()
            encoded_newPW = newPW.encode()
            
            ## ID duplication check
            sha256_CheckDuplicated_id = hashlib.sha256(encoded_newID).hexdigest()
            for line in loginDB:
                line = line.split("\t")
                if line[0] == sha256_CheckDuplicated_id:
                    print("ID already existed. main menu is displayed after 2 seconds.")
                    time.sleep(2)
                    wrapper()
            
            loginDB.write(hashlib.sha256(encoded_newID).hexdigest() + "\t" + hashlib.sha256(encoded_newPW).hexdigest() + "\n")
            loginDB.close()
            
            print("\nWelcome to <>. main menu is displayed after 2 seconds.")
            time.sleep(2)
            wrapper()
    return wrapper

@login
def main():
    print("\nGreetings, " + username + "!")

main()