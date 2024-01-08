import numpy as np
propose = [(color_out, color_in, out_num, in_num) 
            for color_out in range(0,4)
            for color_in in range(0,4)
            for out_num in range(1, 6)
            for in_num in range(1, 6)
            if color_out != color_in
     ]
print(propose[0])

