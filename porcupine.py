import logging
import os
import sys
from threading import Thread
from kalliope import Utils
from cffi import FFI as _FFI

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from porcupinedecoder import HotwordDetector

class PorcupineWakeWordNotFound(Exception):
    pass


class MissingParameterException(Exception):
    pass

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Porcupine(Thread):

    def __init__(self, **kwargs):
        super(Porcupine, self).__init__()
        self._ignore_stderr()
        # Pause listening boolean.
        self.kill_received = False
        # Get input device if set by the user.
        self.input_device_index = kwargs.get('input_device_index', None)
        # Callback function to call when hotword caught.
        self.callback = kwargs.get('callback', None)
        if self.callback is None:
            raise MissingParameterException("Callback function is required with porcupine")
        # Get keywords to load.
        self.keywords = kwargs.get('keywords', None)

        if self.keywords is None:
            raise MissingParameterException("At least one keyword is required with porcupine")
        
        keyword_file_paths = list()
        sensitivities = list()
        
        for keyword in self.keywords:
            path = Utils.get_real_file_path(keyword['keyword']['ppn_file'])  
            try:
                os.path.isfile(path)
            except TypeError: 
                raise PorcupineWakeWordNotFound("The porcupine keyword at %s does not exist" % keyword['keyword']['ppn_file'])
            try:
                sensitivity = keyword['keyword']['sensitivity']
            except KeyError:
                sensitivity = 0.5
            
            keyword_file_paths.append(path)
            sensitivities.append(sensitivity)
            
        keyword_file_paths = ", ".join(keyword_file_paths)
        sensitivities = ", ".join(map(str, sensitivities))

        self.detector = HotwordDetector(keyword_file_paths=keyword_file_paths,
                                        sensitivities=sensitivities,
                                        input_device_index=self.input_device_index,
                                        detected_callback=self.callback
                                        )

    def run(self):
        """
        Start the porcupine thread and wait for a Kalliope trigger word
        :return:
        """
        # start porcupine loop forever
        self.detector.daemon = True
        self.detector.start()
        self.detector.join()

    def pause(self):
        """
        pause the porcupine main thread
        """
        logger.debug("[Porcupine] Pausing porcupine process")
        self.detector.paused = True

    def unpause(self):
        """
        unpause the porcupine main thread
        """
        logger.debug("[Porcupine] Unpausing porcupine process")
        self.detector.paused = False

    def stop(self):
        """
        Kill the porcupine process
        :return: 
        """
        logger.debug("[Porcupine] Killing porcupine process")
        self.interrupted = True
        self.detector.terminate()

    @staticmethod
    def _ignore_stderr():
        """
        Try to forward PortAudio messages from stderr to /dev/null.
        """
        ffi = _FFI()
        ffi.cdef("""
            /* from stdio.h */
            extern  FILE* fopen(const char* path, const char* mode);
            extern int fclose(FILE* fp);
            extern FILE* stderr;  /* GNU C library */
            extern FILE* __stderrp;  /* Mac OS X */
            """)
        stdio = ffi.dlopen(None)
        devnull = stdio.fopen(os.devnull.encode(), b'w')
        try:
            stdio.stderr = devnull
        except KeyError:
            try:
                stdio.__stderrp = devnull
            except KeyError:
                stdio.fclose(devnull)