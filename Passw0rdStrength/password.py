import re
import sys
import hashlib
import requests

def is_strong_password(password):
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True



def main():
    if len(sys.argv) < 2:
        print("""
        _______  _______  _______  _______           _______  _______  ______  
        (  ____ )(  ___  )(  ____ \(  ____ \|\     /|(  ___  )(  ____ )(  __  \ 
        | (    )|| (   ) || (    \/| (    \/| )   ( || (   ) || (    )|| (  \  )
        | (____)|| (___) || (_____ | (_____ | | _ | || |   | || (____)|| |   ) |
        |  _____)|  ___  |(_____  )(_____  )| |( )| || |   | ||     __)| |   | |
        | (      | (   ) |      ) |      ) || || || || |   | || (\ (   | |   ) |
        | )      | )   ( |/\____) |/\____) || () () || (___) || ) \ \__| (__/  )
        |/       |/     \|\_______)\_______)(_______)(_______)|/   \__/(______/ 
                                                                                
        _______           _______  _______  _        _______  _______          
        (  ____ \|\     /|(  ____ \(  ____ \| \    /\(  ____ \(  ____ )         
        | (    \/| )   ( || (    \/| (    \/|  \  / /| (    \/| (    )|         
        | |      | (___) || (__    | |      |  (_/ / | (__    | (____)|         
        | |      |  ___  ||  __)   | |      |   _ (  |  __)   |     __)         
        | |      | (   ) || (      | |      |  ( \ \ | (      | (\ (            
        | (____/\| )   ( || (____/\| (____/\|  /  \ \| (____/\| ) \ \__         
        (_______/|/     \|(_______/(_______/|_/    \/(_______/|/   \__/         
                                                                                
        """)
        print("Welcome to the password checker!")
        print("This program will check if your password is strong enough.")
        print("Let's get started!")
        print("")
        print("Please enter your password below:")
        password = input()
    else:
        password = sys.argv[1]



    compromised = False
    if is_strong_password(password):
        print("Your password meets the requirements!")
        print("Offline password checking...")
        print("Checking if your password is in the common password list...")
        with open("common_passwd.txt", "r") as f:
            line = f.readline()
            while line:
                if password.lower() == line.strip().lower():
                    print("Your password has been compromised!")
                    compromised = True
                    return
                line = f.readline()

        print("Checking if your password is in the most used password list...")
        with open("most_used_passwd.txt", "r") as f:
            line = f.readline()
            while line:
                if password.lower() == line.strip().lower():
                    print("Your password is one of the most used passwords!")
                    compromised = True
                    return
                line = f.readline()
        print("Online password checking...")
        try:
            requests.get("https://www.google.com", timeout=5)
        except requests.ConnectionError:
            print("No internet connection available.")
            return
        
        print("Checking if your password is in the leaked password list...")
        sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        prefix = sha1_password[:5]
        suffix = sha1_password[5:]
        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        response = requests.get(url)
        if response.status_code == 200:
            hashes = response.text.split("\r\n")
            for h in hashes:
                if h.split(":")[0] == suffix:
                    print("Your password has been leaked! It has been used " + h.split(":")[1] + " times.")
                    compromised = True
                    return
        if not compromised:
            print("Your password is secured!")
    else:
        print("Your password is weak! Please try again. Remember to use at least 8 characters, both uppercase and lowercase characters, at least one numerical digit, and at least one special character.")




if __name__ == "__main__":
    main()