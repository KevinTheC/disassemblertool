import io
class FormatStream:
    def __init__(self,flag,filename):
        self.flag = flag
        self._stream = open(filename,"rb")
        self._stream.seek(0,io.SEEK_END)
        self._max = self._stream.tell()
        self._stream.seek(0,io.SEEK_SET)
    #1 should be equal to a single byte. offer support for raw binaries, binary strings, and hex strings
    #8:1 ratio for binary, 2:1 ratio for hex
    def seek(self,number,ptrType):
        if self.flag == "-h":
            self._stream.seek(number*2,ptrType)
        elif self.flag == "-b":
            self._stream.seek(number*8,ptrType)
        elif self.flag == "-raw":
            self._stream.seek(number,ptrType)
    def read(self,number):
        if self.flag == "-h":
            return bin(int(self._stream.read(2*number).decode('ascii'),16))
        elif self.flag == "-b":
            return self._stream.read(8*number).decode('ascii')
        elif self.flag == "-raw":
            var = self._stream.read(number)
            var = (format(byte, '08b') for byte in var)
            var = var.__str__.__get__
            print(var)
            if (self.tell()<1):
                print(var)
            return bin(int(var))
    def readable(self):
        return self._stream.tell() < self._max
    def tell(self):
        return self._stream.tell()