#!/usr/bin/env python
import time
from samplebase import SampleBase
from PIL import Image


class ImageScroller(SampleBase):
    def __init__(self, *args, **kwargs):
        super(ImageScroller, self).__init__(*args, **kwargs)
        self.parser.add_argument("-i", "--image",
                                 help="The image to display",
                                 default="../../../examples-api-use/runtext.ppm")
        self.parser.add_argument("-s", "--speed",
                                 help="Speed between scroll",
                                 default="0.1")
        self.parser.add_argument("-R", "--rotation",
                                 help="Image rotation",
                                 default="0")
    
    def run(self):
        if not 'image' in self.__dict__:
            self.image = Image.open(self.args.image).convert('RGB')
            self.image = self.image.rotate(int(self.args.rotation))
        
        self.image.resize((self.matrix.width, self.matrix.height), Image.ANTIALIAS)
       
        
        double_buffer = self.matrix.CreateFrameCanvas()
        img_width, img_height = self.image.size

        # let's scroll
        xpos = 0
        while True:
            xpos += 1
            if (xpos > img_width):
                xpos = 0

            double_buffer.SetImage(self.image, -xpos)
            double_buffer.SetImage(self.image, -xpos + img_width)

            double_buffer = self.matrix.SwapOnVSync(double_buffer)
            time.sleep(float(self.args.speed))

# Main function
# e.g. call with
#  sudo ./image-scroller.py --chain=4
# if you have a chain of four
if __name__ == "__main__":
    image_scroller = ImageScroller()
    if (not image_scroller.process()):
        image_scroller.print_help()
