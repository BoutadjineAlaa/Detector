import argparse
import requests
import re
from termcolor import colored

# Command Line Argument
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--jsfile', help='JavaScript file URL', required=True)
args = parser.parse_args()


response = requests.get(args.jsfile)

if response.status_code == 200:
    # search for URLs in the JavaScript file
    urls = re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', response.text)
    if len(urls) > 0:
        for url in urls:
            print(colored("\n---------------- URLs DETECTED !! ---------------\n",'green'))
            print(colored(url+"\n", 'green'))
    else:
        print(colored('NO URLS FOUND !!', 'red'))
else:
    print(colored('Error: COULD NOT FETCH !! ' + args.jsfile, 'red'))