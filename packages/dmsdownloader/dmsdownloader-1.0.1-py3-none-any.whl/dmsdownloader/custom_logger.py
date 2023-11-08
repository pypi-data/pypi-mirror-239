import logging
from .color_format import ColorFormats as format

class CustomLogger(logging.Formatter):

    def __init__(self,colored=True, debug=False):
        super().__init__()
        self.debug = debug
        self.coloring = format()
        if self.debug:
            line_func = ':[%(lineno)s:%(funcName)s]:'
        else:
            line_func = ':'
        self.fmt = '%(asctime)s'+line_func+'[%(levelname)s]:%(message)s'
        self.FORMATS = {
            logging.DEBUG:self.fmt,
            logging.INFO: self.fmt,
            logging.WARNING: self.fmt,
            logging.ERROR: self.fmt,
            logging.CRITICAL: self.fmt,
            logging.SUCCESS: self.fmt
        }
        if colored:
            self.FORMATS = {
            logging.DEBUG:'%(asctime)s'+line_func+self.coloring.DEBUG+'[%(levelname)s]'+self.coloring.RESET+':%(message)s',
            logging.INFO: '%(asctime)s'+line_func+self.coloring.INFO+'[%(levelname)s]'+self.coloring.RESET+':%(message)s',
            logging.WARNING: '%(asctime)s'+line_func+self.coloring.WARNING+'[%(levelname)s]'+self.coloring.RESET+':%(message)s',
            logging.ERROR: '%(asctime)s'+line_func+self.coloring.ERROR+'[%(levelname)s]'+self.coloring.RESET+':%(message)s',
            logging.CRITICAL: '%(asctime)s'+line_func+self.coloring.CRITICAL+'[%(levelname)s]'+self.coloring.RESET+':%(message)s',
            logging.SUCCESS: '%(asctime)s'+line_func+self.coloring.SUCCESS+'[%(levelname)s]'+self.coloring.RESET+':%(message)s'
        }
            
    def addLoggingLevel(levelName, levelNum, methodName=None):
        """
        Comprehensively adds a new logging level to the `logging` module and the
        currently configured logging class.

        `levelName` becomes an attribute of the `logging` module with the value
        `levelNum`. `methodName` becomes a convenience method for both `logging`
        itself and the class returned by `logging.getLoggerClass()` (usually just
        `logging.Logger`). If `methodName` is not specified, `levelName.lower()` is
        used.

        To avoid accidental clobberings of existing attributes, this method will
        raise an `AttributeError` if the level name is already an attribute of the
        `logging` module or if the method name is already present 

        Example
        -------
        >>> addLoggingLevel('TRACE', logging.DEBUG - 5)
        >>> logging.getLogger(__name__).setLevel("TRACE")
        >>> logging.getLogger(__name__).trace('that worked')
        >>> logging.trace('so did this')
        >>> logging.TRACE
        5

        """
        if not methodName:
            methodName = levelName.lower()

        if hasattr(logging, levelName):
            raise AttributeError('{} already defined in logging module'.format(levelName))
        if hasattr(logging, methodName):
            raise AttributeError('{} already defined in logging module'.format(methodName))
        if hasattr(logging.getLoggerClass(), methodName):
            raise AttributeError('{} already defined in logger class'.format(methodName))

        # This method was inspired by the answers to Stack Overflow post
        # http://stackoverflow.com/q/2183233/2988730, especially
        # http://stackoverflow.com/a/13638084/2988730
        def logForLevel(self, message, *args, **kwargs):
            if self.isEnabledFor(levelNum):
                self._log(levelNum, message, args, **kwargs)
        def logToRoot(message, *args, **kwargs):
            logging.log(levelNum, message, *args, **kwargs)

        logging.addLevelName(levelNum, levelName)
        setattr(logging, levelName, levelNum)
        setattr(logging.getLoggerClass(), methodName, logForLevel)
        setattr(logging, methodName, logToRoot)


    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt,"%Y-%m-%d %H:%M:%S")
        return formatter.format(record)
