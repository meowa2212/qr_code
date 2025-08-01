'''
Wojciech Gorzynski
16-06-2025 v1

Program for generating QR codes
'''
from draw import Draw
from alignment_table import table

class QRcode_frame():
    def __init__(self, data, version=3, err_cor="M"):
        self.raw_data = data
        self.version = version
        self.err_corr = err_cor
        self.initialize()
        self.error_correction()
        self.mask()
        self.inscript()
    
    def mask(self):
        self.qr_code[12][6] = 1
        self.qr_code[12][7] = 0
        self.qr_code[12][8] = 1
        
        self.qr_code[self.size-9][12] = 1
        self.qr_code[self.size-8][12] = 0
        self.qr_code[self.size-7][12] = 1
    
    def error_correction(self):
        match self.err_corr:
            case "L":
                self.qr_code[self.size-6][12] = 1
                self.qr_code[self.size-5][12] = 1
                
                self.qr_code[12][5] = 1
                self.qr_code[12][4] = 1
                
            case "M":
                self.qr_code[self.size-6][12] = 0
                self.qr_code[self.size-5][12] = 1
                
                self.qr_code[12][5] = 0
                self.qr_code[12][4] = 1
                
            case "Q":
                self.qr_code[self.size-6][12] = 1
                self.qr_code[self.size-5][12] = 0
                
                self.qr_code[12][5] = 1
                self.qr_code[12][4] = 0   
                       
            case "H":
                self.qr_code[self.size-6][12] = 0
                self.qr_code[self.size-5][12] = 0
                
                self.qr_code[12][5] = 0
                self.qr_code[12][4] = 0
    
    def initialize(self):
        self.size = 29+(self.version-1)*4
        self.qr_code = [[0 if x in range(0, 4) or x in range(self.size-4, self.size) else None for x in range(self.size)] if y not in range(0, 4) and y not in range(self.size-4, self.size) else [0 for x in range(self.size)] for y in range(self.size)] #initial board with quiet zone
        self.qr_code[self.size-12][12] = 1 # format dot
        self.add_position(3,3)
        self.add_position(self.size-12,3)
        self.add_position(3,self.size-12)
        self.add_alignment()
        self.add_timing()
    
    def add_timing(self):
        color = 1
        for x_offset in range(9, self.size-15):
            self.qr_code[10][3+x_offset] = color
            if color == 1:
                color = 0
            else:
                color = 1
        
        color = 1    
        for y_offset in range(9, self.size-15):
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
    
    def add_alignment(self):
        cords = table(self.version)

        for cord_x in cords:
            for cord_y in cords:
                if self.qr_code[cord_x+2][cord_y+2] == None:
                    color = 1
                    for size_offset in range(3):
                        for x_offset in range(size_offset, 5-size_offset):
                            for y_offset in range(size_offset, 5-size_offset):
                                self.qr_code[cord_x+x_offset][cord_y+y_offset] = color
                        if color == 1:
                            color = 0
                        else:
                            color = 1

    def inscript(self): # need to add mask pattern
        
        bit_length = len(self.raw_data)-1
        bit_index = 0
        move_flag = "flat"
        elev_flag = True # True for moving up
        x, y = self.size-5, self.size-5
        while bit_index < bit_length:
            if y in range(4, self.size-4):
                match move_flag:
                    case "flat":
                        if self.qr_code[y][x] == None:
                            self.qr_code[y][x] = self.raw_data[bit_index]
                            bit_index += 1
                        x -= 1
                        if elev_flag:
                            move_flag = "up"
                        else:
                            move_flag = "down"
                        
                    case "up":
                        if self.qr_code[y][x] == None:
                            self.qr_code[y][x] = self.raw_data[bit_index]
                            bit_index += 1
                        x += 1
                        y -= 1
                        move_flag = "flat"
                    
                    case "down":
                        if self.qr_code[y][x] == None:
                            self.qr_code[y][x] = self.raw_data[bit_index]
                            bit_index += 1
                        x += 1
                        y += 1
                        move_flag = "flat"
            elif x < 4:
                print("too much data (rest got cutoff)")
                return
            else:
                if elev_flag:
                    elev_flag = False
                    y += 1
                else:
                    elev_flag = True
                    y -= 1
                x -= 2
                move_flag = "flat"
                
                
                
if __name__ == "__main__":
    code = QRcode_frame([-1*(x % 3)-1 for x in range(501)], 1)
    Draw.draw(code.qr_code, 10)