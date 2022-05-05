#!/usr/bin/env python
"""This programme displays the date and time on an RGBMatrix display."""

import time
import datetime
from rgbmatrix import graphics
from rgbmatrix import RGBMatrix
from samplebase import SampleBase

# Load up the font (use absolute paths so script can be invoked
# from /etc/rc.local correctly)

    
class Clock(SampleBase):
    global fonts
    def __init__(self, *args, **kwargs):
        super(Clock, self).__init__(*args, **kwargs)

    def loadFont(self,font):
        
             
        self.fonts[font] = graphics.Font()
        self.fonts[font].LoadFont("/opt/led-matrix/fonts/" + font + ".bdf")
    
    def run(self):
        flip = True
        tick = True
        scroller = 32


        # set colour
        ColorWHI = graphics.Color(255, 255, 255)
        RED = graphics.Color(255, 0, 0)
        GREEN = graphics.Color(0, 255, 0)
        BLUE = graphics.Color(0, 0, 255)
        YELLOW = graphics.Color(255, 255, 0)
        PURPLE = graphics.Color(255, 0, 255)

        lastDateFlip = int(round(time.time() * 1000))
        lastSecondFlip = int(round(time.time() * 1000))
        lastScrollTick = int(round(time.time() * 1000))

        self.fonts = {}
        
        
        self.loadFont('7x13B')
        self.loadFont('6x13')#Hour Font 6x13
        self.loadFont('6x9')

        # Create the buffer canvas
         
        MyOffsetCanvas = self.matrix.CreateFrameCanvas()
        while(1):
            currentDT = datetime.datetime.now()

            if currentDT.hour < 23:
                time.sleep(0.05)
                scrollColour = BLUE
                fulldate = currentDT.strftime("%d-%m-%y  %A")
                if currentDT.day < 10:
                    fulldate = fulldate[1:]

            sizeofdate = len(fulldate)*7

            Millis = int(round(time.time() * 1000))

            if Millis-lastSecondFlip > 1000:
                lastSecondFlip = int(round(time.time() * 1000))
                tick = not tick

            if Millis-lastDateFlip > 5000:
                lastDateFlip = int(round(time.time() * 1000))
                flip = not flip

            scroller = scroller-1
            if scroller == (-sizeofdate):
                scroller = 32

            thetime = currentDT.strftime("%l"+(":" if tick else " ")+"%M")

            thetime = str.lstrip(thetime)
            sizeoftime = (25 - (len(thetime) * 9) / 2)

            pmam = currentDT.strftime("%p")

            graphics.DrawText(MyOffsetCanvas, self.fonts['7x13B'], scroller, 28,
                              scrollColour, fulldate)

            graphics.DrawText(MyOffsetCanvas, self.fonts['6x13'], sizeoftime, 14, RED,
                              thetime)

            graphics.DrawText(MyOffsetCanvas, self.fonts['6x9'], 50, 14, GREEN, pmam)

            MyOffsetCanvas = self.matrix.SwapOnVSync(MyOffsetCanvas)
            MyOffsetCanvas.Clear()
    
if __name__ == "__main__":
    clock = Clock()
    if (not clock.process()):
        clock.print_help()