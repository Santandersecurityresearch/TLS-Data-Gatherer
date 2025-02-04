# Terminal colors for beautiful output
class t_color:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDER = '\033[4m'

def print_usage():
    print("Usage: " + t_color.BOLD + "python tls_data_gatherer.py <file_name.csv> <tech>" + t_color.ENDC)

def print_error(error_message:str):
    print("%s%s%s"%(t_color.RED, error_message, t_color.ENDC))

def print_success(success_message:str):
    print("%s%s%s"%(t_color.GREEN, success_message, t_color.ENDC))
