import re
import requests
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", required=True, help="Input URL")
parser.add_argument("-o", "--output", help="Output file location")
args = parser.parse_args()

if args.url: 
    print("""\033[31m\n\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠉⣎⣧⢀⣀⡀⢀⣇⠀⠀⣐⠂⠆⠊⡱⣏⣿⡿⠋⠁⢀⣀⣤⢤⣴⡲⣖⡶⣾⣹⢯⣟⡽⣯⢿⣽⣻
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠄⣿⢿⠿⣯⣇⠀⢹⢀⡴⡠⠂⣠⢾⣹⠟⠁⠀⣀⣨⣶⣻⣼⣫⢷⣻⣭⢿⡵⣯⣟⣾⣻⣟⡿⣾⡽
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣌⢻⡏⠀⠈⠉⠓⡿⠏⠛⢰⠿⢻⢺⡿⢖⣾⠿⣟⣿⡽⣃⣉⠉⠉⢙⢓⣊⢿⡽⣛⣾⢷⣻⣽⡳⡟
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄⢂⠍⡉⣹⣻⢾⣽⣏⣯⣟⣾⢯⡽⣿⢽⣫⣷⡿⠝⣓
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠃⠌⢒⠠⠱⣭⣿⣳⣟⣾⡽⣞⡯⣟⣞⣯⣷⣿⡽⣟⣉
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠜⡀⢣⠘⡠⣽⣿⣽⣫⡽⢯⣽⣏⡿⣞⣟⣮⣽⠷⠋
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⡀⠣⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⠁⡌⠄⢣⠐⡉⢿⣯⢿⣽⣻⣧⡿⣽⣿⣻⣷⠗⡂⠠
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠰⠬⠝⣖⠀⠀⠀⢠⢔⣂⡭⢅⠰⠠⢆⡙⠲⢥⣂⠅⡒⡘⣿⠟⢈⡤⡙⣿⣽⢾⡷⢁⣀⣤⣤
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢆⠀⠀⠩⠀⠀⠀⠀⠉⠒⠐⠢⠭⣭⠖⣂⡅⢂⠌⡡⢐⡐⢃⠞⡓⡗⡍⢿⡾⣯⠿⠛⠉⠉⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢰⠁⠀⠆⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⢀⠁⡆⠸⢀⠁⢆⢹⣆⡰⢹⠇⣿⡿⠷⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠈⠀⠌⠀⢀⠀⠀⠀⠀⠀⠀⣸⠀⠀⠀⠅⠂⢌⠂⡅⢊⢤⣞⡄⠜⢫⡼⠋⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⡊⠀⡠⠊⡁⢄⠀⠀⠀⠀⢻⠀⠀⢠⢈⠰⢈⠒⡈⢤⡎⢀⣤⡾⠟⣁⣀⣀⠀⠤⠠⠄⠒⣂
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠈⠪⠡⠐⠁⠀⠀⠀⠀⠛⠀⠀⡀⠂⡌⢂⡑⣨⡣⢂⣿⣿⡧⠵⠶⠖⠒⠚⠛⠋⠉⠉⠉
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠒⠂⠀⠠⠄⡀⠀⠀⠀⢀⠡⠡⡐⠂⣔⣾⠑⣺⣿⣿⡇⢰⡀⠦⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠱⠒⢂⣀⠄⠀⠀⠀⠀⡌⠠⢁⡴⢋⢹⡁⢂⣿⣿⣿⡧⣧⣼⠧⠴⠬⠤⠤⣤⠤⠤
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⡂⠀⠈⠈⠀⠀⠀⠀⡠⢊⣠⠕⢋⡐⢤⢫⢀⢃⣿⣿⣿⣟⣿⣿⣯⡔⣽⡼⡩⣥⠇⣀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢟⠋⢸⡏⢆⠀⠀⠀⠀⠠⣊⠔⡋⠄⢌⡐⢄⢎⠅⣂⣾⡿⣿⣿⣿⣿⣿⣳⡗⣾⣗⣧⢹⡆⡥
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢻⡋⠘⢆⠈⠻⢷⣗⣶⢶⣳⢮⣥⣜⣤⣮⣔⣤⣾⣼⢿⣟⣯⣿⣟⣿⣿⣿⣿⣳⡝⣶⡽⣹⣞⡳⣵
⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⠋⠀⢐⡇⢰⡀⢂⠉⠢⠤⢈⣉⣛⡙⢿⣺⡽⣞⡷⣯⣟⣾⡽⣿⢾⣻⢾⣽⡾⣯⡙⠻⢷⣭⣳⠟⣽⡧⣟⣽
--------{ Coded By Boutadjine Alaa }--------------\033[0m""")
    print("\033[31m@Boutadjine36264\033[0m")
    try:
        content = requests.get(args.url).text.split('"')

        extensions = (".png", ".jpg", ".wav", ".jpeg", ".json", ".js", ".php", ".xml")
        starts = ("/", "http://", "https://", "file://", "php://", "ftp://", "./", "../")

        end_point = set()
        for i in content:
            if re.match("^[a-zA-Z0-9_\/:&?%.\-=]*$", i):
                if i.startswith(starts) or i.endswith(extensions):
                    end_point.add(i)
                elif not i.startswith(starts):
                    temp = i.split("/")
                    if any(j in end_point for j in ["/" + temp[0], "./" + temp[0], "../" + temp[0]]):
                        end_point.add(i)

        if args.output:
            with open(args.output, "w") as f:
                for url in end_point:
                    f.write(f"{url}\n")
        else:
            for url in end_point:
                sys.stdout.write("\033[32m" + url + "\n\033[0m")

    except Exception as e:
        print(f"An error occurred: {e}")
