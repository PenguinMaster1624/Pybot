from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
import logging
import json

class CustomJSONFormatter(logging.Formatter):
    def __init__(self, fmt):
        logging.Formatter.__init__(self, fmt)

    def format(self, record: logging.LogRecord) -> str:
        logging.Formatter.format(self, record)
        return json.dumps(get_log(record), indent=2)


def get_log(record: logging.LogRecord) -> dict:
    d = {
        "time": datetime.fromisoformat(record.asctime).astimezone(tz=ZoneInfo('America/New_York')).isoformat(sep=' ', timespec='seconds'),
        "process_name": record.processName,
        "process_id": record.process,
        "thread_name": record.threadName,
        "thread_id": record.thread,
        "level": record.levelname,
        "logger_name": record.name,
        "pathname": Path(record.pathname).as_posix(),
        "function_name": record.funcName,
        "line": record.lineno,
        "message": record.message,
    }

    return d

LOGGING_CONFIG = { 
    'version': 1,
    'formatters': { 
        'standard': { 
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'custom_formatter': { 
			"format": "[{asctime}] [{levelname:<8}] {name}: {message}",
			"datefmt": "%Y-%m-%d %H:%M:%S%z",
			"style": "{",
            "exc_info": True,
			"validate": True
        },
        'json_formatter': { 
            '()':  lambda: CustomJSONFormatter(fmt='%(asctime)s')
        }
    },
    'handlers': { 
        'default': { 
            'formatter': 'custom_formatter',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
        'json_handler': { 
            'formatter': 'json_formatter',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'json.log',
            'maxBytes': 1024 * 1024 * 32, # = 32MB
            'backupCount': 3
        },
        'readable_handler': {
            'formatter': 'custom_formatter',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'readable.log',
            'maxBytes': 1024 * 1024 * 32, # = 32MB
            'backupCount': 3,
        }
    },
    'loggers': { 
        'main': {
            'handlers': ['default', 'json_handler', 'readable_handler'],
            'level': 'INFO',
            'propagate': False
        }
    }
}