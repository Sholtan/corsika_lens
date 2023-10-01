
import struct

from .constants import BLOCK_SIZE_BYTES   # 1248 THIN, 1092 NO THIN

#: buffersize
DEFAULT_BUFFER_SIZE = BLOCK_SIZE_BYTES * 100    # 124800 for THIN, 109200 for NO THIN
#: to read how many bytes in the file
RECORD_MARKER = struct.Struct('i')







def read_buffer_size(path):
    '''
    Reads the first 4 bytes of a file and checks if
    it is the 'RUNH' designation None is returned,
    if not interpret it as unsigned integer, the
    size of the CORSIKA buffer in bytes
    '''

    with open(path, 'rb') as f:
        data = f.read(RECORD_MARKER.size)

        buffer_size, = RECORD_MARKER.unpack(data)

    return buffer_size



def iter_blocks(f):
    is_fortran_file = True
    buffer_size = DEFAULT_BUFFER_SIZE  # 109200

    data = f.read(4)
    f.seek(0)
    if data == b'RUNH':
        print("\n\n\nFILE DOESN'T HAVE SIZE RECORD_MARKER, SO IT'S NOT FORTRAN_FILE\n\n\n")
        is_fortran_file = False


    while True:
        # for the fortran-chunked output, we need to read the record size
        if is_fortran_file:
            data = f.read(RECORD_MARKER.size)
            if len(data) < RECORD_MARKER.size:
                raise IOError("Read less bytes than expected, file seems to be truncated")

            buffer_size, = RECORD_MARKER.unpack(data)

        data = f.read(buffer_size)

        n_blocks = len(data) // BLOCK_SIZE_BYTES

        for block in range(n_blocks):
            start = block * BLOCK_SIZE_BYTES
            stop = start + BLOCK_SIZE_BYTES
            block = data[start:stop]

            if len(block) < BLOCK_SIZE_BYTES:
                raise IOError("Read less bytes than expected, file seems to be truncated")
            #print("yielding block")
            yield block

        # read trailing record marker
        if is_fortran_file:
            f.read(RECORD_MARKER.size)