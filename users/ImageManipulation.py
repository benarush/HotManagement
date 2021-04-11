from PIL import Image

class ImageManipulation:
    __ORIENT = {
        # exif_val: (rotate degrees cw, mirror 0=no 1=horiz 2=vert); see http://www.sno.phy.queensu.ca/~phil/exiftool/TagNames/EXIF.html
        2: (0, 1),
        3: (180, 0),
        4: (0, 2),
        5: (90, 1),
        6: (270, 0),
        7: (270, 1),
        8: (90, 0),
    }

    def __init__(self, img_full_path):
        self.img_full_path = img_full_path
        self.img = Image.open(img_full_path)
        self.img_format = self.img.format
        self.fix_oriantation()
        self.resize_img()

    # fix imageManipulate orientation (issue with jpegs taken by cams; phones in particular):
    def fix_oriantation(self):
        try:
            orient = self.img._getexif()[274]
        except (AttributeError, KeyError, TypeError, ValueError):
            orient = 1  # default (normal)
        print(f"Orient - {orient}")
        if orient in self.__ORIENT:
            (rotate, mirror) = self.__ORIENT[orient]
            if rotate:
                self.img = self.img.rotate(rotate)
            if mirror == 1:
                self.img = self.img.transpose(Image.FLIP_LEFT_RIGHT)
            elif mirror == 2:
                self.img = self.img.transpose(Image.FLIP_TOP_BOTTOM)

    # for now i resize to 300X300
    def resize_img(self):
        if self.img.height > 300 or self.img.width > 300:
            resize = (300, 300)
            self.img.thumbnail(resize)
            self.img.save(self.img_full_path)