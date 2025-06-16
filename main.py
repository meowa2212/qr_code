'''
Wojciech Gorzynski
16-06-2025 v1

Program for generating QR codes
'''
from draw import Draw
from alignment_table import table

class QRcode():
    def __init__(self, data, version=3):
        self.raw_data = data
        self.version = version
        self.initialize()
        self.add_timing()
        self.add_position(3,3)
        self.add_position(self.size-12,3)
        self.add_position(3,self.size-12)
        self.add_alignment()
    
    def initialize(self):
        self.size = 29+(self.version-1)*4
        self.qr_code = [[None for x in range(self.size)] for y in range(self.size)]
        self.qr_code = [[0 if x in range(0, 4) or x in range(self.size-4, self.size) else None for x in range(self.size)] if y not in range(0, 4) and y not in range(self.size-4, self.size) else [0 for x in range(self.size)] for y in range(self.size)]
    
    def add_timing(self):
        color = 1
        for x_offset in range(3, self.size-6):
            self.qr_code[10][3+x_offset] = color
            if color == 1:
                color = 0
            else:
                color = 1
        
        color = 1    
        for y_offset in range(3, self.size-6):
            self.qr_code[3+y_offset][10] = color
            if color == 1:
                color = 0
            else:
                color = 1
          
    def add_position(self, x, y):
        color = 0
        for square_offset in range(4):   
            for x_offset in range(square_offset, 9-square_offset):
                for y_offset in range(square_offset, 9-square_offset):
                    self.qr_code[y+y_offset][x+x_offset] = color
            if color == 1:
                color = 0
            else:
                color = 1
    
    def add_alignment(self): # needs to be fixed
        cords = table(self.version)
        for cord in cords:
            if self.qr_code[cord+2][cord+2] == None:
                color = 1
                for size_offset in range(2):
                    for x_offset in range(5-size_offset):
                        for y_offset in range(5-size_offset):
                            self.qr_code[cord+x_offset][cord+y_offset] = color
                    if color == 1:
                        color = 0
                    else:
                        color = 1

    def draw(self):
        Draw.draw(self.qr_code, 10)

if __name__ == "__main__":
    code = QRcode([[1,0,1],[0,1,0],[1,0,1]],5)
    code.draw()