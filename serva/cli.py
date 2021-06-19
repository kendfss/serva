import subprocess, os, argparse, json, re

import pyperclip

from .mail import quick_mail 
from .ip import get_ip 

here, this = os.path.split(__file__)
settings_path = os.path.join(here, 'settings.json')

class UnrecognizedProtocolError(Exception): pass

def load_settings():
    with open(settings_path, 'r') as fob:
        return json.load(fob)

def save_settings():
    with open(settings_path, 'w') as fob:
        json.dump(settings, fob, sort_keys=True)

settings = {
    "protocols": {
        "gemini": "gemini://",
        "gopher": "gopher://",
        "http": "http://",
    },
    "email": {
        "address": None,
        "password": None
    },
    # "block": False,
    "browser": None,
    "number": 8000,
    "dont": False,
    "copy": False,
    "extensions": {
        ".ps1": '',
        ".sh": '',
        ".bat": '',
        ".py": 'python',
        ".js": 'node',
    }
} if not os.path.exists(settings_path) else load_settings()
save_settings()

def setting(args):
    if args.protocol:
        settings['protocols'][args.protocol] = input(f"Enter a uri prefix for the {args.protocol} protocol:\n\t")
        yield f'added {protocol} protocol'
    if args.mail:
        settings['email']['address'] = args.mail
        yield f"email address set to {settings['email']['address']}"
        settings['email']['password'] = input(f"Enter the password for {settings['email']['address']}:\n\t")
        yield f"email password set to {''.join('*' for i in settings['email']['password'])}"
    if args.browser:
        settings['browser'] = args.browser
        yield f"browser set to {settings['browser']}"
    # if args.block:
    #     settings['block'] = not settings['block']
    #     yield f"block set to {settings['block']}"
    if args.number:
        settings['number'] = int(args.number)
        yield f"number set to {settings['number']}"
    if args.dont:
        settings['dont'] = not settings['dont']
        yield f"dont set to {settings['dont']}"
    if args.copy:
        settings['copy'] = not settings['copy']
        yield f"copy set to {settings['copy']}"
    if args.extension:
        settings['extensions'][args.script] = input("Which program should execute the script? (leave blank for system default, otherwise include flags as needed)\n\t")
    save_settings()

def parse_protocol(protocol):
    if protocol.endswith("://"):
        return protocol
    if (protocol := settings['protocols'].get(protocol)):
        return protocol
    raise UnrecognizedProtocolError

def find_script():
    path = os.getcwd()
    fnames = os.listdir(os.getcwd())
    for name in fnames:
        if os.path.isfile(name):
            fmt = "^%s(?P<ext>{})$" % (re.escape("serve."))
            patstr = "|".join(fmt.format(ext[1:]) for ext in settings['extensions'].keys())
            pat = re.compile(pat, re.I)
            # if any(fi)
            if (match := pat.match(name)):
                return name

def running(args):
    os.chdir(args.root)
    
    if (ext := find_script()):
        subprocess.run([settings[ext], "serve."+ext])
    else:
        address = f"{parse_protocol(args.protocol)}{get_ip()}:{args.number}"
        if not args.dont:
            if (browser := args.open):
                subprocess.run([browser, address])
                yield f"opened with {browser}"
            elif (browser := settings["browser"]):
                subprocess.run([browser, address])
                yield f"opened with {browser}"
            else:
                os.startfile(address)            
                yield "opened with system default"
        
        if args.copy:
            pyperclip.copy(address)
        if args.mail: 
            quick_mail(
                       address, 
                       args.mail, 
                       settings['email']['address'], 
                       settings['email']['password']
                      )
        yield f"serving @ {address}"
        subprocess.run(['python', '-m', 'http.server', address, '&' if not args.block else ''])

def handler(args):
    if args.mode == "running":
        [*map(print, running(args))]
    elif args.mode == "setting":
        [*map(print, setting(args))]

def main():
    parser = argparse.ArgumentParser(description="Serve the current/given directory on a given port. Unless otherwise stated, all arguments are supported in both 'setting' and 'running' modes")
    parser.add_argument('mode', default='running', choices="running setting".split(), help="Execute cli in running or setting mode")
    parser.add_argument('--root', '-r', default='.', help="root to the directory you wish to serve")
    parser.add_argument('--mail', '-m', default=None, help="send local address to an email-address of your choice")
    parser.add_argument('--copy', '-c', default=settings['copy'], action='store_true', help="copy url to clipboard")
    parser.add_argument('--block', '-b', default=False, action='store_true', help="(unimplemented) Block/unblock the prompt while the server is running")
    parser.add_argument('--protocol', '-p', default="http://", help="Set the protocol for the local address")
    parser.add_argument('--number', '-n', default=8000, type=int, help="Set the number of the serving port")
    parser.add_argument('--dont', '-d', default=settings['dont'], action='store_true', help="Choose not to open in browser")
    parser.add_argument('--open', '-o', default=settings['browser'], help="Choose a browser to open in")
    parser.add_argument('--extension', '-e', default=None, help="(setting only) lookout for a script named 'serve' with given extension")
    handler(parser.parse_args())

if __name__=='__main__':
    main()






"""
more info
    https://stackoverflow.com/questions/5663787/upload-folders-from-local-system-to-ftp-using-python-script
    https://stackoverflow.com/questions/9382045/send-a-file-through-sockets-in-python
    https://stackabuse.com/serving-files-with-pythons-simplehttpserver-module/
    https://docs.python.org/3.7/library/http.server.html
"""
