import os
import struct
import glob
import json
from collections import deque


class FifoMemoryQueue(object):
    """In-memory FIFO queue, API compliant with FifoDiskQueue."""

    def __init__(self):
        self.q = deque()
        self.push = self.q.append

    def pop(self):
        q = self.q
        return q.popleft() if q else None

    def close(self):
        pass

    def __len__(self):
        return len(self.q)


class LifoMemoryQueue(FifoMemoryQueue):
    """In-memory LIFO queue, API compliant with LifoDiskQueue."""

    def pop(self):
        q = self.q
        return q.pop() if q else None


class FifoDiskQueue(object):
    """Persistent FIFO queue."""

    szhdr_format = ">L"
    szhdr_size = struct.calcsize(szhdr_format)

    def __init__(self, path, chunksize=100000, filesize=10000000, syncAll=False):
        self.path = path
        if not os.path.exists(path):
            os.makedirs(path)
        self.syncAll = syncAll
        self.info = self._loadinfo(chunksize, filesize)
        self.chunksize = self.info['chunksize']
        self.filesize = self.info['filesize']
        self.headf = self._openchunk(self.info['head'][0], 'ab+')
        self.tailf = self._openchunk(self.info['tail'][0])
        os.lseek(self.tailf.fileno(), self.info['tail'][2], os.SEEK_SET)

    def push(self, string):
        hnum, hpos = self.info['head']
        hpos += 1
        szhdr = struct.pack(self.szhdr_format, len(string))
        os.write(self.headf.fileno(), szhdr + string)
        headf_size = self._chunk_fstat(self.tailf.fileno()).st_size
        
        if hpos == self.chunksize or headf_size >= self.filesize:  # Roll to next chunk
            hpos = 0
            hnum += 1
            self.headf.close()
            self.headf = self._openchunk(hnum, 'ab+')
        
        self.info['size'] += 1
        self.info['head'] = [hnum, hpos]
        
        if self.syncAll==True:
            self._saveinfo(self.info)

    def _openchunk(self, number, mode='r'):
        return open(os.path.join(self.path, 'q%05d' % number), mode)

    def pop(self):
        self.rollover_tail()
        tnum, tcnt, toffset = self.info['tail']
        if [tnum, tcnt] >= self.info['head']:
            if tnum == self.info['head'][0] and tcnt == self.info['head'][1] and self.info['size'] > 0:
                self.info['size'] = 0
                self._saveinfo(self.info)
            
            return
            
        tfd = self.tailf.fileno()
        szhdr = os.read(tfd, self.szhdr_size)
        if not szhdr:
            return
        size, = struct.unpack(self.szhdr_format, szhdr)
        data = os.read(tfd, size)
        
        tcnt += 1
        toffset += self.szhdr_size + size
        tailf_size = self._chunk_fstat(self.tailf.fileno()).st_size
        
        if ((tcnt == self.chunksize or tailf_size >= self.filesize or toffset >= tailf_size) and 
                tnum < self.info['head'][0]):  # roll over to next chunk
            tcnt = toffset = 0
            tnum += 1
            self.tailf.close()
            os.remove(self.tailf.name)
            self.tailf = self._openchunk(tnum)
        
        self.info['size'] -= 1
        self.info['tail'] = [tnum, tcnt, toffset]
        
        if self.syncAll==True:
            self._saveinfo(self.info)
        
        return data

    def close(self):
        self.headf.close()
        self.tailf.close()
        self._saveinfo(self.info)
        if len(self) == 0:
            self._cleanup()
            
    def rollover_tail(self):
        tnum, tcnt, toffset = self.info['tail']
        tailf_size = self._chunk_fstat(self.tailf.fileno()).st_size
        if ((tcnt == self.chunksize or tailf_size >= self.filesize or toffset >= tailf_size) and 
                tnum < self.info['head'][0]):  # roll over to next chunk
            tcnt = toffset = 0
            tnum += 1
            self.tailf.close()
            os.remove(self.tailf.name)
            self.tailf = self._openchunk(tnum)
        
        self.info['tail'] = [tnum, tcnt, toffset]

    def __len__(self):
        return self.info['size']

    def _loadinfo(self, chunksize, filesize):
        infopath = self._infopath()
        if os.path.exists(infopath):
            with open(infopath) as f:
                info = json.load(f)
        else:
            info = {
                'chunksize': chunksize,
                'filesize': filesize,
                'size': 0,
                'tail': [0, 0, 0],
                'head': [0, 0],
            }
            self._saveinfo(info)
        return info

    def _saveinfo(self, info):
        with open(self._infopath(), 'w') as f:
            json.dump(info, f)
            f.flush()

    def _infopath(self):
        return os.path.join(self.path, 'info.json')
    
    def _chunk_fstat(self, fd):
        return os.fstat(fd)

    def _cleanup(self):
        for x in glob.glob(os.path.join(self.path, 'q*')):
            os.remove(x)
        os.remove(os.path.join(self.path, 'info.json'))
        if not os.listdir(self.path):
            os.rmdir(self.path)



class LifoDiskQueue(object):
    """Persistent LIFO queue."""

    SIZE_FORMAT = ">L"
    SIZE_SIZE = struct.calcsize(SIZE_FORMAT)

    def __init__(self, path):
        self.path = path
        if os.path.exists(path):
            self.f = open(path, 'rb+')
            qsize = self.f.read(self.SIZE_SIZE)
            self.size, = struct.unpack(self.SIZE_FORMAT, qsize)
            self.f.seek(0, os.SEEK_END)
        else:
            self.f = open(path, 'wb+')
            self.f.write(struct.pack(self.SIZE_FORMAT, 0))
            self.size = 0

    def push(self, string):
        self.f.write(string)
        ssize = struct.pack(self.SIZE_FORMAT, len(string))
        self.f.write(ssize)
        self.size += 1

    def pop(self):
        if not self.size:
            return
        self.f.seek(-self.SIZE_SIZE, os.SEEK_END)
        size, = struct.unpack(self.SIZE_FORMAT, self.f.read())
        self.f.seek(-size-self.SIZE_SIZE, os.SEEK_END)
        data = self.f.read(size)
        self.f.seek(-size, os.SEEK_CUR)
        self.f.truncate()
        self.size -= 1
        return data

    def close(self):
        if self.size:
            self.f.seek(0)
            self.f.write(struct.pack(self.SIZE_FORMAT, self.size))
        self.f.close()
        if not self.size:
            os.remove(self.path)

    def __len__(self):
        return self.size
