import os
import time
import fcntl
import logging
import logging.handlers


class TimedRotatingFileHandlerSafe(logging.handlers.TimedRotatingFileHandler):

    def _open(self):
        if getattr(self, '_lockf', None) and not self._lockf.closed:
            return logging.handlers.TimedRotatingFileHandler._open(self)
        while True:
            try:
                self._aquire_lock()
                return logging.handlers.TimedRotatingFileHandler._open(self)
            except IOError:
                self._lockf.close()
            finally:
                self._release_lock()

    def _aquire_lock(self):
        self._lockf = open(self.baseFilename + '_rotating_lock', 'a')
        fcntl.flock(self._lockf,fcntl.LOCK_EX|fcntl.LOCK_NB)

    def _release_lock(self):
        self._lockf.close()

    def is_same_file(self, file1, file2):
        '''check is files are same by comparing inodes'''
        return os.fstat(file1.fileno()).st_ino == os.fstat(file2.fileno()).st_ino

    def doRollover(self):
        """
        do a rollover; in this case, a date/time stamp is appended to the filename
        when the rollover happens.  However, you want the file to be named for the
        start of the interval, not the current time.  If there is a backup count,
        then we have to get a list of matching filenames, sort them and remove
        the one with the oldest suffix.
        """

        try:
            self._aquire_lock()
        except IOError:
            # cant aquire lock, return
            self._lockf.close()
            return

        # check if file is same
        _tmp_f = open(self.baseFilename, 'r')
        is_same = self.is_same_file(self.stream, _tmp_f)
        _tmp_f.close()

        if self.stream:
            self.stream.close()
        # get the time that this sequence started at and make it a TimeTuple
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
        dfn = self.baseFilename + "." + time.strftime(self.suffix, timeTuple)

        if is_same and not os.path.exists(dfn):
            os.rename(self.baseFilename, dfn)
        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)
        self.mode = 'a'
        self.stream = self._open()
        currentTime = int(time.time())
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        #If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dstNow = time.localtime(currentTime)[-1]
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
                    newRolloverAt = newRolloverAt - 3600
                else:           # DST bows out before next rollover, so we need to add an hour
                    newRolloverAt = newRolloverAt + 3600
        self.rolloverAt = newRolloverAt
        self._release_lock()
