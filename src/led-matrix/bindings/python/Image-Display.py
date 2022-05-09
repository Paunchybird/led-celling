#!/usr/bin/env python3
import time
from samplebase import SampleBase
from PIL import Image


class ImageDisplay(SampleBase):
    def __init__(self, *args, **kwargs):
        super(ImageDisplay, self).__init__(*args, **kwargs)
        self.parser.add_argument("-i", "--image",
                                 help="The image to display",
                                 default="/opt/mypanel-icons/My-Empty.png")
        self.parser.add_argument("-R", "--rotation",
                                 help="Image rotation",
                                 default="0")
    
    def run(self):
        if not 'image' in self.__dict__:
            self.image = Image.open(self.args.image).convert('RGB')
            
       
        self.image.resize((self.matrix.width, self.matrix.height), Image.ANTIALIAS)
        self.image = self.image.rotate(int(self.args.rotation))
        my_matrix = self.matrix.CreateFrameCanvas()
        img_width, img_height = self.image.size
        
        while True:
            my_matrix.SetImage(self.image)
            my_matrix = self.matrix.SwapOnVSync(my_matrix)
            time.sleep(10)

# Main function
# e.g. call with
#  sudo ./image-scroller.py --chain=4
# if you have a chain of four
if __name__ == "__main__":
    image_display = ImageDisplay()
    if (not image_display.process()):
        image_display.print_help()


