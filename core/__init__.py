#!/usr/bin/python

import os
import sys
import logging
import logging.handlers

__version__ = '0.5'

log = logging.getLogger('main')

_logging_configured = False
_mem_handler = None
def initialize_logging(unit_test=False):
    global _logging_configured, _mem_handler

    if not _logging_configured:
        if unit_test:
            _logging_configured = True
            return

        # root logger
        logger = logging.getLogger()

        # time format is same format of strftime
        log_format = ['%(asctime)-15s %(levelname)-8s %(name)-11s %(message)s', '%Y-%m-%d %H:%M']
        formatter = logging.Formatter(*log_format)

        _mem_handler = logging.handlers.MemoryHandler(1000*1000, 100)
        _mem_handler.setFormatter(formatter)
        logger.addHandler(_mem_handler)

        logger.setLevel(logging.INFO)

        _logging_configured = True

_logging_started = False
def start_logging(filename=None, level=logging.INFO, debug=False, quiet=False):
    global _logging_configured, _mem_handler, _logging_started

    if not _logging_started:
        if debug:
            hdlr = logging.StreamHandler()
        else:
            hdlr = logging.handlers.RotatingFileHandler(filename, maxBytes=1000*1024, backupCount=9)

        hdlr.setFormatter(_mem_handler.formatter)

        _mem_handler.setTarget(hdlr)

        # root logger
        logger = logging.getLogger()

        logger.removeHandler(_mem_handler)
        logger.addHandler(hdlr)

        logger.setLevel(level)

        if not debug and not quiet:
            console = logging.StreamHandler()
            console.setFormatter(hdlr.formatter)
            logger.addHandler(console)

            # flush memory handler to the console without
            # destroying the buffer
            if len(_mem_handler.buffer) > 0:
                for record in _mem_handler.buffer:
                    console.handle(record)

        # flush what we have stored from the plugin initialization
        _mem_handler.flush()

        _logging_started = True
        
def flush_logging():
    """Flushes memory logger to console"""
    console = logging.StreamHandler()
    console.setFormatter(_mem_handler.formatter)
    logger = logging.getLogger()
    logger.addHandler(console)
    if len(_mem_handler.buffer) > 0:
        for record in _mem_handler.buffer:
            console.handle(record)
    _mem_handler.flush()

def main():
    initialize_logging()
    log.debug('initilise logging')
    # 
    # try:
    #     manager = Manager(options)
    # except IOError, e:
    #     # failed to load config
    #     log.critical(e.message)
    #     flush_logging()
    #     sys.exit(1)
    #     
    # manager.acquire_lock()
    # 
    start_logging(os.path.join(os.path.dirname(__file__), 'flexget.log'), logging.DEBUG)

main()