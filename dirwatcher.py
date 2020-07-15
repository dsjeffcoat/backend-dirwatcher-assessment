import argparse
import signal
import time
import os
import sys
import re
import logging


__author__ = '''Diarte Jeffcoat w/help from Daniel Lomelino, Kyle Negley, Randy Charity Jr
            & the #after-hours-work 07/07/20 study session with Piero Madar'''

# Progress Report: Currently, the file & text detection are functioning, but the extension filter is not functioning. Also, need to have text detection not start over upon searching for magic text.


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s.%(msecs)03d [%(name)-12s][ %(levelname)s ]: %(message)s',
                              datefmt='%Y-%m-%d &%H:%M:%S')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)

exit_flag = False
path_list = {}


def scan_single_file(path, cursor, magic):
    cursor = 0
    with open(path) as d:
        for linenum, line in enumerate(d):
            if linenum >= cursor:
                if re.search(magic, line):
                    logger.info(
                        f"I found the magic text \'{magic}\' in {path} on {linenum}!")


def detect_added_files(files):
    """Searches current directory for any new files that were added"""
    global path_list
    for f in files:
        if f not in path_list:
            path_list[f] = None
            logger.info(f"Added: {f} found in this directory.")
    return files


def detect_removed_files(files):
    """Searches current directory for any files that were removed"""
    global path_list
    for f in list(path_list):
        if f not in files:
            del path_list[f]
            logger.info(f"Removed: {f} was deleted from this directory.")
    return files


def watch_directory(args):
    """While the directory is open, this function keeps a watch of
    the activity within the directory"""
    dir_list = os.listdir(args.dir)
    detect_added_files(dir_list)
    detect_removed_files(dir_list)

    if os.path.isdir(args.dir):
        print(dir_list)
    for fname in dir_list:
        pathname = os.path.join(args.dir, fname)
        path_list[fname] = scan_single_file(
            pathname, path_list[fname], args.magic)


def signal_handler(sig_num, frame):
    """
    This is a handler for SIGTERM and SIGINT. Other signals can be mapped here as well (SIGHUP?)
    Basically, it just sets a global flag, and main() will exit its loop if the signal is trapped.
    :param sig_num: The integer signal number that was trapped from the OS.
    :param frame: Not used
    :return None
    """
    # log the associated signal name
    global exit_flag
    logger.warning(
        f'Received {signal.Signals(sig_num).name} call from terminal. Shutting down program.')
    exit_flag = True


def create_parser():
    '''Create an argument parser object for command line arguments in the terminal'''
    parser = argparse.ArgumentParser(
        description="Search within files for the magic string text.")
    # Positional Arguments
    parser.add_argument("dir", help="directory path to monitor")
    parser.add_argument(
        "magic", help="magic string to monitor within files")
    # Optional Arguments
    parser.add_argument(
        "-int", "--interval", default=1.0, type=int, help="controls the polling interval of the search")
    parser.add_argument(
        "-ext", "--extension", default='.txt', type=str, help="filter the type of files to include in the search")
    return parser


def main(args):
    parser = create_parser()
    ns = parser.parse_args(args)
    text = ns.magic
    path = ns.dir
    interval = ns.interval
    extension = ns.extension
    print(ns)
    # Hook into these two signals from the OS
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    start = time.perf_counter()

    # detect_added_files(path)
    # detect_removed_files(path)

    logger.info(f'''
    {"-" * 60}\n
    Running {__file__}\n
    Started on {time.ctime()}\n
    {"-" * 60}
    ''')

    while not exit_flag:
        try:
            watch_directory(ns)
        except FileNotFoundError as fnfe:
            logger.error(fnfe)
        except OSError as ose:
            logger.error(ose)
        except Exception as e:
            # This is an UNHANDLED exception
            logger.error(
                f"UNHANDLED EXCEPTION: Found an unknown exception - {e}")
        # put a sleep inside my while loop so I don't peg the cpu usage at 100%
        time.sleep(interval)

    # final exit point happens here
    end = time.perf_counter()

    uptime = (end - start)
    # Log a message that we are shutting down
    # Include the overall uptime since program start

    logger.info(f'''
    {"-" * 60}\n
    Stopped {__file__}\n
    Uptime was {uptime:.4f} seconds\n
    {"-" * 60}
    ''')


if __name__ == '__main__':
    # main()
    main(sys.argv[1:])
