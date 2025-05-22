import datetime

def print_current_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    print("Current Time:", current_time)

def lambda_handler(event, context):
    print_current_time()