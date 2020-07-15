import argparse
import signal
import time
import os
import sys
import re
import logging


__author__ = 'Diarte Jeffcoat w/help from Daniel Lomelino, Kyle Negley and Randy Charity Jr'

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s.%(msecs)03d [%(name)-12s][ %(levelname)s ]: %(message)s',
                              datefmt='%Y-%m-%d &%H:%M:%S')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)

exit_flag = False


def scan_single_file(filename, text, extension):
    with open(filename) as f:
        for line in f.readlines():
            if re.search(text, line):
                logger.info(f"I found the magic text in {filename}!")


def detect_added_files(dirname):
    """Searches current directory for any new files that were added"""
    watch_list = dirname
    prev_path = dict([(f, None) for f in os.listdir(watch_list)])

    while True:
        time.sleep(1)
        new_path = dict([(f, None) for f in os.listdir(watch_list)])
        for f in new_path:
            if f not in prev_path:
                logger.warning(f"Added: {f} found in {dirname}")
        prev_path = new_path


def detect_removed_files(dirname):
    """Searches current directory for any files that were removed"""
    watch_list = dirname
    prev_path = dict([(f, None) for f in os.listdir(watch_list)])

    while True:
        time.sleep(1)
        new_path = dict([(f, None) for f in os.listdir(watch_list)])
        for f in new_path:
            if f not in prev_path:
                logger.warning(f"Removed: {f} deleted from {dirname}")
        prev_path = new_path


def watch_directory(dirname, text, extension):
    """While the directory is open, this function keeps a watch of
    the activity within the directory"""
    dir_list = os.listdir(dirname)
    if os.path.isdir(dirname):
        print(dir_list)


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
        "text", help="magic string to monitor within files")
    # Optional Arguments
    parser.add_argument(
        "-int", "--interval", default='3', type=int, help="controls the polling interval of the search")
    parser.add_argument(
        "-ext", "--extension", default='.txt', type=str, help="filter the type of files to include in the search")
    return parser


def main(args):
    parser = create_parser()
    ns = parser.parse_args(args)
    magic = ns.text
    path = ns.dir
    interval = ns.interval
    extension = ns.extension

    # Hook into these two signals from the OS
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    # Now my signal_handler will get called if OS sends
    # either of these to my process.

    start = time.perf_counter()

    logger.info(f'''
    {"-" * 60}\n
    Running {__file__}\n
    Started on {time.ctime()}\n
    {"-" * 60}
    ''')

    while not exit_flag:
        try:
            watch_directory(path, magic, extension)
            # detect_added_files(path)
            # detect_removed_files(path)
        except FileNotFoundError as fnfe:
            if fnfe.errno == errno.ENOENT:
                logger.error(f'{path} not found on system')
            else:
                logger.error(fnfe)
        except OSError as ose:
            logger.error(ose)
        except Exception as e:
            # This is an UNHANDLED exception
            logger.error(
                f"UNHANDLED EXCEPTION: Found an unknown exception - {e}")
        # put a sleep inside my while loop so I don't peg the cpu usage at 100%
        time.sleep(5)

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
