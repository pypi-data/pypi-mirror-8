class ChannelOrder:
    RGB = [0,1,2]
    RBG = [0,2,1]
    GRB = [1,0,2]
    GBR = [1,2,0]
    BRG = [2,0,1]
    BGR = [2,1,0]

class DriverBase(object):
    """Base driver class to build other drivers from"""
    
    def __init__(self, num = 0, width = 0, height = 0, c_order = ChannelOrder.RGB, gamma = None):
        if num == 0:
            num = width * height
            if num == 0:
                raise ValueError("Either num or width and height must be provided!")

        self.numLEDs = num
        self.gamma = gamma
        if self.gamma == None:
            self.gamma = [i for i in range(256)]

        self.c_order = c_order

        self.width = width
        self.height = height
        self.bufByteCount = int(3 * self.numLEDs)

        self._buf = []
        for i in range(0, self.bufByteCount):
            self._buf.append(0)

        #in case the driver needs the matrix mapping
        self.matrix_map = None

    #Push new data to strand
    def update(self, data):
        raise RuntimeError("Base class update() called. This shouldn't happen")

    def setMasterBrightness(self, brightness):
        return False

    def _fixData(self, data):
        gamma = self.gamma
        for a, b in enumerate(self.c_order):
            self._buf[a:self.numLEDs*3:3] = [gamma[v] for v in data[b::3]]



