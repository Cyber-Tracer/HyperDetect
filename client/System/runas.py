import os
import argparse

SYS_DIR = os.path.dirname(os.path.abspath(__file__))
CRED_FILE = os.path.join(SYS_DIR, 'cred.xml')
RUNAS_FILE = os.path.join(SYS_DIR, 'runas.ps1')
STORE_CREDS_FILE = os.path.join(SYS_DIR, 'store_credentials.ps1')

def cred_file_exists():
    return os.path.exists(CRED_FILE)

def store_creds():
    os.system(f'powershell -File {STORE_CREDS_FILE} {CRED_FILE}')

def runas_client(batch_file):
    os.system(f'powershell -File {RUNAS_FILE} {CRED_FILE} {batch_file}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Wrapper for running as different users")
    subparsers = parser.add_subparsers(help="sub-command help")

    # Command one
    parser_one = subparsers.add_parser('store_creds', help="Store credentials used by this wrapper")
    parser_one.set_defaults(func=store_creds)

    # Command two
    parser_two = subparsers.add_parser('command_two', help="Run a batch file as a different user")
    parser_two.add_argument("batch_file", type=str, help="Path to the batch file to run")
    parser_two.set_defaults(func=runas_client)

    args = parser.parse_args()
    if 'func' in args:
        if len(vars(args))==1:
            args.func()
        else:
            args.func(args)
    else:
        parser.print_help()