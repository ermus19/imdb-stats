from __future__ import print_function
from sys import argv
import signal
import time
import csv
import sys
import os



class Logger(object):
    """Logger object that prints messages to both a file and the terminal."""

    def __init__(self, log_name):
        """Opens the log file."""

        self.terminal = sys.stdout
        self.log = open(log_name, "a", 1)
        self.log.write('-------------------------------------------------------------------------------------------\n')

    def flush(self):
        """Flush attribute needed when replacing sys.stdout"""

        pass

    def write(self, message):
        """Writes a message to both log file and the terminal."""

        timestamp = ""
        if message != "\n":
            timestamp = generate_timestamp()
        
        self.terminal.write(message)
        self.log.write(timestamp + " " + message)
        self.log.flush()
        os.fsync(self.log)

def signal_handler(signal, frame):
    print("")
    print("Received SIGINT signal, exiting...")

def generate_timestamp():
    """Generates and returns a formatted timestamp."""

    timestamp = time.gmtime()
    formatted_timestamp = time.strftime("%Y-%m-%d %H:%M:%S", timestamp)
    return formatted_timestamp

def format_time(minutes):
    """Converts a time value in minutes to days and minutes"""

    days = int((minutes / 1440))
    minutes = int((minutes % 1440))
    hours = int((minutes / 60))
    minutes = int((minutes % 60))

    formatted_time = "\nTotal time watching movies: " + str(days) + " day/s, " + str(hours)  + " hours and " + str(minutes) + " minutes."
    
    return formatted_time

def parse_file(file_name):
    """Opens the imdb list csv file and returns its data."""

    try:
        with open(file_name, mode='r+') as file:

            reader = csv.reader(file)

            print(file_name + " file successfully opened!")
            print("Reading file data...")

            file_lines = list(reader)
            
    except IOError:
        print("There was an error openning the file>", file_name)
        sys.exit()
    finally:
        print("Closing file...")
        file.close()
    
    return file_lines

def calculate_metrics(data):
    """Calculate some metrics from the dataset. """

    entries = 0
    line_data = []
    total_minutes = 0
    years_sum = 0

    start_time = time.time()

    for line in data[1:]:

        entries += 1
        total_minutes += int(line[9])
        years_sum += int(line[10])

    mean_years = int(round(years_sum/entries))
    
    print(format_time(total_minutes))
    print("The release year mean of the movies is " + str(mean_years))

    elapsed_time = (time.time() -start_time) * 1000
    print("Analyzed %s entries in %s milliseconds.\n\n" % (entries, int(elapsed_time)))

if __name__ == '__main__':

    signal.signal(signal.SIGINT, signal_handler)

    log_file = 'stats.log'
    argv_size = len(argv)

    print("\nWelcome to the IMDB stats script!\n")

    sys.stdout = Logger(log_file)

    if argv_size != 2:
        print("script usage> python imdb-stats.py imdb_list.csv")   
        sys.exit()
    elif argv[1].lower().endswith('.csv'): 
        file_name = argv[1]
        file_data = parse_file(file_name)
        calculate_metrics(file_data)
    else:
        print("imdb-stats takes a csv file as input!")
        print("Input file taken: ", argv[1])
        sys.exit()
