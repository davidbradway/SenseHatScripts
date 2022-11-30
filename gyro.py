import time
import sys
import threading
from sense_hat import SenseHat
#from sense_emu import SenseHat

red = (255, 0, 0)
green = (0, 255, 0)

class Stepper():
    def __init__(self, increment):
        self.increment = float(increment)
        
        self.s = SenseHat()
        self.s.low_light = True
        self.x = 4
        self.y = 4
        self.color = green #red
        self.s.set_pixel(self.x, self.y, self.color)
        self.o0 = self.unwrap(self.s.get_orientation_degrees())
        self.d = self.unwrap(self.s.get_orientation_degrees())
        self.next_t = time.time_ns()/1000.
        self._run()
    
    def __del__(self):
        self.s.clear()
        
    def _run(self):
        try:
            while(True):
                if True: #time.time_ns()/1000. > self.next_t:
                    self.next_t += self.increment

                    # Get the new orientation
                    o = self.unwrap(self.s.get_orientation_degrees())

                    # calculate the differential orientation
                    for k, v in self.d.items():
                        self.d[k] = o[k]-self.o0[k]
                    #self.o0 = o
                    
                    self.d = self.unwrap(self.d)
                    self.move_dot()
                    self.update_screen()
        except:
            self.s.clear()

    def unwrap(self, o):
        'Unwrap the roll, pitch, and yaw to range [-180, 180]'
        for k, v in o.items():
            o[k] = v-360 if v> 180 else v
            o[k] = v+360 if v<-180 else v
        return o
    
    def move_dot(self, thresh=0.3):
        self.x = self.clamp(self.x+1) if self.d['pitch']<-1*thresh else self.x
        self.x = self.clamp(self.x-1) if self.d['pitch']>   thresh else self.x
        self.y = self.clamp(self.y+1) if self.d['roll'] >   thresh else self.y
        self.y = self.clamp(self.y-1) if self.d['roll'] <-1*thresh else self.y
        
    def clamp(self, value, min_value=0, max_value=7):
        return min(max_value, max(min_value, value))

    def update_screen(self):
        self.s.clear()
        self.s.set_pixel(self.x, self.y, self.color)


def main():
    a = Stepper(increment = 10.)

if __name__ == '__main__':
   main()
