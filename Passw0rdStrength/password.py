import re
import hashlib
import requests
import argparse
import random
import string

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

def check_password(password, check_common, check_most_used, check_leaked, custom_file, verbose, generate_password):
    compromised = False
    if generate_password:
        length = generate_password
        password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length))
        print(f"Generated password: {password}")
        return

    if is_strong_password(password):
        if verbose:
            print("Your password meets the requirements!")
        
        if check_common:
            if verbose:
                print("Checking against common passwords...")
            with open("common_passwd.txt", "r") as f:
                for line in f:
                    if password.lower() == line.strip().lower():
                        print("Your password has been compromised in the common password list!")
                        compromised = True
                        return

        if check_most_used:
            if verbose:
                print("Checking against most used passwords...")
            with open("most_used_passwd.txt", "r") as f:
                for line in f:
                    if password.lower() == line.strip().lower():
                        print("Your password is one of the most used passwords!")
                        compromised = True
                        return

        if custom_file:
            if verbose:
                print(f"Checking against passwords in {custom_file}...")
            try:
                with open(custom_file, "r") as f:
                    for line in f:
                        if password.lower() == line.strip().lower():
                            print(f"Your password has been compromised in the custom password list from {custom_file}!")
                            compromised = True
                            return
            except FileNotFoundError:
                print(f"The file {custom_file} does not exist.")
                return
        
        if check_leaked:
            if verbose:
                print("Checking for leaked passwords...")
            try:
                requests.get("https://www.google.com", timeout=5)
            except requests.ConnectionError:
                print("No internet connection available.")
                return
            
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
        print("Your password is weak! Please try again.")

def main():
    parser = argparse.ArgumentParser(description='Password Strength Checker')
    parser.add_argument('password', type=str, nargs='?', help='Password to check')
    parser.add_argument('-c', '--check-common', action='store_true', help='Check against common password list')
    parser.add_argument('-m', '--check-most-used', action='store_true', help='Check against most used password list')
    parser.add_argument('-l', '--check-leaked', action='store_true', help='Check against leaked password list')
    parser.add_argument('-f', '--file', type=str, help='Custom password file to check against')
    parser.add_argument('-g', '--generate', type=int, nargs='?', help='Generate a random password with the specified length')
    parser.add_argument('-v','--verbose', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    if not args.password and not args.generate:
        print("Please provide a password as an argument or use the generate option.")
        return

    check_common = args.check_common or not (args.check_most_used or args.check_leaked or args.file or args.generate)
    check_most_used = args.check_most_used or not (args.check_common or args.check_leaked or args.file or args.generate)
    check_leaked = args.check_leaked or not (args.check_common or args.check_most_used or args.file or args.generate)
    generate_password = args.generate or not (check_common or check_most_used or check_leaked or args.file)
    print(generate_password)
    check_password(args.password, check_common, check_most_used, check_leaked, args.file, args.verbose, generate_password)

if __name__ == "__main__":
    main()
