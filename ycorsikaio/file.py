import numpy as np
from collections import namedtuple

from .subblocks import (
    parse_run_header,
    parse_run_end,
    parse_event_header,
    parse_event_end,
    parse_longitudinal,
    parse_cherenkov_photons,
)

from .io import iter_blocks, read_buffer_size

PhotonEvent = namedtuple(
    'PhotonEvent',
    ['header', 'photons', 'longitudinal', 'end']
)

class CorsikaCherenkovFile:
    
    def __init__(self, path):
        self.EventClass = PhotonEvent
        self._buffer_size = read_buffer_size(path)
        self._f = open(path, 'rb')
        self._block_iter = iter_blocks(self._f)

        runh_bytes = next(self._block_iter)
        if not runh_bytes[:4] == b'RUNH':
            raise ValueError("MISSING b'RUNH'")


        self.run_header = parse_run_header(runh_bytes)[0]
        self.version = round(float(self.run_header['version']), 4)
        self._run_end = None

    def __next__(self):     #   iterates through events, starting from EVENT_HEADER, till EVENT_END
        block = next(self._block_iter)

        if block[:4] == b'RUNE':   # check for RUN-END block
            self._run_end = parse_run_end(block)
            raise StopIteration()
        if block[:4] != b'EVTH':       # must start from EVENT_HEADER
            raise IOError("EVTh block expected but found {}".format(block[:4]))
        
        event_header = parse_event_header(block)[0]

        data_bytes = bytearray()
        long_bytes = bytearray()

        block = next(self._block_iter)

        block_counter = 0

        while block[:4] != b'EVTE':
            if block[:4] == b'LONG':
                long_bytes += block[longitudinal_header_dtype.itemsize:]
            else:
                data_bytes += block
                block_counter += 1
            block = next(self._block_iter)

        event_end = parse_event_end(block)[0]
        data = self.parse_data_blocks(data_bytes)
        longitudinal = parse_longitudinal(long_bytes)
        return self.EventClass(event_header, data, longitudinal, event_end)




    @classmethod
    def parse_data_blocks(cls, data_bytes):
        photons = parse_cherenkov_photons(data_bytes)
        return photons


    def __iter__(self):
            return self



    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self._f.close()