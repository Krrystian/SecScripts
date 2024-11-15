import argparse
import nmap
import os
import sys

def check_root(options):
    if os.geteuid() != 0 and options:
        print("This script requires root privileges to run some nmap scans.")
        print("Please run the script with 'sudo'.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Portify - A simple porting tool')
    parser.add_argument('-t', '--target', nargs='?', type=str, help='Target address', required=False)
    parser.add_argument('-o', '--options', nargs='?', type=str, help='Nmap options (require admin access)', required=False)
    args = parser.parse_args()
    check_root(args.options)

    target = args.target or 'scanme.nmap.org'
    options = args.options or "-sT -T3 -F"
    
    print('Target address:', target)
    print('Options:', options)
    nm = nmap.PortScanner()
    nm.scan(target, arguments=options)
    for host in nm.all_hosts():
        print('Host: %s (%s)' % (host, nm[host].hostname()))
        print('State: %s' % nm[host].state())
        for proto in nm[host].all_protocols():
            print('Protocol: %s' % proto)
            print('------------------')
            lport = nm[host][proto].keys()
            for port in lport:
                print('%s\tport: %s\tstate: %s' % (nm[host][proto][port]['name'], port, nm[host][proto][port]['state']))
            print('------------------')

if __name__ == '__main__':
    main()

