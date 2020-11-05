class colours:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def server_log(*args):
    print('[SERVER LOG] ', end='')
    for var in args:
        print(var, end='')
    print('\n')


def server_error(*args):
    print(f'{colours.FAIL}[SERVER ERROR] ', end='')
    for var in args:
        print(var, end='')
    print('\n')

def server_warning(*args):
    print(f'{colours.WARNING}[SERVER WARNING] ', end='')
    for var in args:
        print(var, end='')
    print('\n')

