# encoding=utf-8
# The Python Imaging Library (PIL) is

#    Copyright © 1997-2011 by Secret Labs AB
#    Copyright © 1995-2011 by Fredrik Lundh

# By obtaining, using, and/or copying this software and/or its associated
# documentation, you agree that you have read, understood, and will comply
# with the following terms and conditions:

# Permission to use, copy, modify, and distribute this software and its
# associated documentation for any purpose and without fee is hereby granted,
# provided that the above copyright notice appears in all copies, and that
# both that copyright notice and this permission notice appear in supporting
# documentation, and that the name of Secret Labs AB or the author not be used
# in advertising or publicity pertaining to distribution of the software
# without specific, written prior permission.

# SECRET LABS AB AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS
# SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS.
# IN NO EVENT SHALL SECRET LABS AB OR THE AUTHOR BE LIABLE FOR ANY SPECIAL,
# INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
# OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.

__version__ = "0.1.0"

from PIL import Image, ImageFile
import array
import png
try:
    from itertools import izip_longest as zip_l
except ImportError:
    from itertools import zip_longest as zip_l

try:
    bytes
except NameError:
    bytes = str


def buf_emu(not_buffer):
    if hasattr(not_buffer, 'tostring'):
        return not_buffer.tostring()
    else:
        return bytes(not_buffer)


try:
    buffer
except NameError:
    try:
        buffer = memoryview
    except NameError:
        buffer = buf_emu

def group(s, n):
    # See http://www.python.org/doc/2.6/library/functions.html#zip
    return list(zip(*[iter(s)] * n))


class PngImageFile(ImageFile.ImageFile):
    format = "PNG"
    format_description = "Portable network graphics"

    def _open(self):
        self.png = png.Reader(file=self.fp)
        self.png.preamble()
        direct = self.png.asDirect
        bitdepth = self.png.bitdepth
        if self.png.sbit:
            import struct
            sbit = struct.unpack('%dB' % len(self.png.sbit), self.png.sbit)
            bitdepth = max(sbit)
        if bitdepth < 8:
            x, y, pixels, meta = self.png._as_rescale(direct, 8)
        else:
            x, y, pixels, meta = direct()
        self.size = y, x
        self.mode = "L" if meta['greyscale'] else "RGB"
        if meta['alpha']:
            self.mode = self.mode + 'A'

        if meta['bitdepth'] > 8:
            if self.mode == 'L':
                self.mode = 'I'
                rawmode = 'I;16'
            elif self.mode == 'RGBA':
                rawmode = 'RGBA;16B'
            elif self.mode == 'RGB':
                rawmode = 'RGB;16B'
            else:
                rawmode = self.mode + ';' + str(meta['bitdepth'])
        else:
            rawmode = self.mode
        self.pixels = pixels
        # image data
        self.tile = [("raw", (0, 0) + self.size, 0, rawmode)]
        self.info['gamma'] = meta.get('gamma')
        #self.text = self.png.im_text # experimental

    def verify(self):
        "Verify PNG file"

        pass

    def load_read(self, n_bytes):
        "internal: read more image data"
        row = next(self.pixels)
        if isinstance(row, array.array):
            if row.typecode == 'H':
                if self.mode == 'RGBA' or self.mode == 'RGB':
                    row.byteswap()
        return bytes(buffer(row))

    def load_seek(self, pos=0):
        pass


# --------------------------------------------------------------------
# PNG writer
def _save(im, fp, filename):
    # save an image to disk (called by the save method)
    def rows():
        for i in range(im.size[0]):
            row = []
            for j in range(im.size[1]):
                px = im.getpixel((j, i))
                if hasattr(px, '__iter__'):
                    #Multi-channel image
                    row.extend(px)
                else:
                    #Single channel image
                    row.append(px)
            yield row
    # Default values
    bits = 8
    palette = None
    alpha = False
    greyscale = (im.mode == 'L')
    if im.mode == 'I':
        greyscale = True
        bits = 16
    elif im.mode == 'LA':
        greyscale = True
        alpha = True
    elif im.mode == 'RGBA':
        alpha = True
    elif im.mode == 'L;4':
        greyscale = True
        bits = 4
    elif im.mode == 'L;2':
        greyscale = True
        bits = 2
    elif im.mode == 'L;1':
        greyscale = True
        bits = 1
    elif im.mode == '1':
        greyscale = True
        bits = 1
        fullrows = rows

        def rows():
            for row in fullrows():
                yield [bool(it) for it in row]

    if im.mode == "P":
        palette_bytes = im.palette.getdata()[1]
        # attempt to minimize storage requirements for palette images
        if "bits" in im.encoderinfo:
            # number of bits specified by user
            colors = 1 << im.encoderinfo["bits"]
        else:
            # check palette contents
            if im.palette:
                # For now palette only RGB
                colors = max(min(len(palette_bytes) // 3, 256), 2)
            else:
                colors = 256

        if colors <= 2:
            bits = 1
        elif colors <= 4:
            bits = 2
        elif colors <= 16:
            bits = 4
        else:
            bits = 8

        # For now palette only RGB
        palette_byte_number = (2 ** bits) * 3
        # Match to declared palette size
        palette_bytes = bytearray(palette_bytes[:palette_byte_number])
        if len(palette_bytes) < palette_byte_number:
            palette_bytes.extend((0,) * \
                                 (palette_byte_number - len(palette_bytes)))
        #while len(palette_bytes) < palette_byte_number:
        #    palette_bytes.append(0)
        palette = group(palette_bytes, 3)

    transparency = im.encoderinfo.get('transparency',
                        im.info.get('transparency',
                            None))
    if (transparency or transparency == 0):
        if im.mode == "P":
            # "Patch" palette with transparency
            if isinstance(transparency, bytes):
                transparency = bytearray(transparency)
            else:  # not sure about this
                transparency = max(0, min(255, transparency))
                transparency = bytearray((255,) * transparency)

            # limit to actual palette size
            alpha_bytes = 2 ** bits
            palette = zip_l(palette, transparency[:alpha_bytes], fillvalue=255)
            palette = list(map(lambda it: it[0] + (it[1],), palette))
            transparency = None
        elif im.mode == "L":
            transparency = max(0, min(65535, transparency))
        elif im.mode == "RGB":
            pass  # triade will pass to writer
        else:
            if "transparency" in im.encoderinfo:
                # don't bother with transparency if it's an RGBA
                # and it's in the info dict. It's probably just stale.
                raise IOError("cannot use transparency for this mode")

    writer = png.Writer(size=im.size,
                        greyscale=greyscale,
                        bitdepth=bits,
                        alpha=alpha,
                        palette=palette,
                        transparent=transparency,
                        compression=im.encoderinfo.get("compress_level", -1),
                        gamma=im.info.get('gamma'),
                        )

    writer.write(fp, rows())

    #  TODO: pHYs
    #  TODO: pnginfo (?)
    #  TODO: ICC

    try:
        fp.flush()
    except:
        pass


# --------------------------------------------------------------------
# Registry
Image.register_open("PNG", PngImageFile)
Image.register_save("PNG", _save)

Image.register_extension("PNG", ".png")

Image.register_mime("PNG", "image/png")
