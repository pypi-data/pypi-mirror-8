# -*- python -*-
# -*- coding: utf-8 -*-
#
#  This file is part of the easydev software
#
#  Copyright (c) 2011-2013 
#
#  File author(s): Thomas Cokelaer <cokelaer@gmail.com>
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  Website: https://www.assembla.com/spaces/pyeasydev/wiki
#  Documentation: http://packages.python.org/easydev
#
##############################################################################
# $:Id $
"""Utilities provided in this module can be found either in the
standard Python module called :mod:`colorsys` or in matplotlib.colors (e.g rgb2hex)
or are original to this module (e.g., rgb2huv)

The dependencies to matplotlib are minimal and within the function. So, if
you do not use the class ColorMapTools, you do not need matplotlib.

"""


import colorsys
from .tools import check_param_in_list, swapdict, check_range
from .xfree86 import XFree86_colors


__all__ = ["HEX", "Color", "hex2web", "web2hex", "hex2rgb", "hex2dec",
    "rgb2hex", "rgb2hsv", "hsv2rgb", "rgb2hls", "hls2rgb","yuv2rgb", "rgb2yuv", 
    "to_intensity", "ColorMapTools", "yuv2rgb_int", "rgb2yuv_int"
    ]



def hex2web(hexa):
    """Convert hexadecimal string (6 digits) into *web* version (3 digits) 

    .. doctest::

        >>> from easydev.colors import hex2web
        >>> hex2web("#FFAA11")
        '#FA1'

    .. seealso:: :func:`web2hex`, :func:`hex2rgb`
        :func:`rgb2hex`, :func:`rgb2hsv`, :func:`hsv2rgb`, :func:`rgb2hls`, 
        :func:`hls2rgb`
    """
    hexa = HEX().get_standard_hex_color(hexa)
    return "#" + hexa[1::2]


def web2hex(web):
    """Convert *web* hexadecimal string (3 digits) into  6 digits version

    .. doctest::

        >>> from easydev.colors import web2hex
        >>> web2hex("#FA1")
        '#FFAA11'

    .. seealso:: :func:`hex2web`, :func:`hex2rgb`
        :func:`rgb2hex`, :func:`rgb2hsv`, :func:`hsv2rgb`, :func:`rgb2hls`, 
        :func:`hls2rgb`
    """
    return HEX().get_standard_hex_color(web)
    


def hex2rgb(hexcolor, normalise=False):
    """This function converts a hex color triplet into RGB
    
    Valid hex code are: 
     
     * #FFF
     * #0000FF
     * 0x0000FF
     * 0xFA1


    .. doctest::

        >>> from easydev.colors import hex2rgb
        >>> hex2rgb("#FFF", normalise=False)
        (255, 255, 255)
        >>> hex2rgb("#FFFFFF", normalise=True)
        (1.0, 1.0, 1.0)


    .. seealso:: :func:`hex2web`, :func:`web2hex`, 
        :func:`rgb2hex`, :func:`rgb2hsv`, :func:`hsv2rgb`, :func:`rgb2hls`, 
        :func:`hls2rgb`
    """
    hexcolor = HEX().get_standard_hex_color(hexcolor)[1:]
    r, g, b =  int(hexcolor[0:2], 16), int(hexcolor[2:4], 16), int(hexcolor[4:6], 16)
    if normalise:
        r, g, b = _normalise(r,g,b)
    return r, g, b


def rgb2hex(r, g, b, normalised=False):
    """Convert RGB to hexadecimal color
    
    :param: can be a tuple/list/set of 3 values (R,G,B)
    :return: a hex vesion ofthe RGB 3-tuple

    .. doctest::

        >>> from easydev.colors import rgb2hex
        >>> rgb2hex(0,0,255, normalised=False)
        '#0000FF'
        >>> rgb2hex(0,0,1, normalised=True)
        '#0000FF'

    .. seealso:: :func:`hex2web`, :func:`web2hex`, :func:`hex2rgb`
        , :func:`rgb2hsv`, :func:`hsv2rgb`, :func:`rgb2hls`, 
        :func:`hls2rgb`

    """
    if normalised:
        r,g,b = _denormalise(r,g,b, mode="rgb")
    check_range(r, 0, 255)
    check_range(g, 0, 255)
    check_range(b, 0, 255)
    return '#%02X%02X%02X' % (r, g, b)


def rgb2hls(r, g, b, normalised=True):
    """Convert an RGB value to an HLS value. 

    :param bool normalised: if *normalised* is True, the input RGB triplet 
        should be in the range 0-1 (0-255 otherwise)
    :return: the HLS triplet. If *normalised* parameter is True, the output 
        triplet is in the range 0-1; otherwise, H in the range 0-360 and LS
        in the range 0-100.

    .. doctest::

        >>> from easydev.colors import rgb2hls
        >>> rgb2hls(255,255,255, normalised=False)
        (0.0, 1.0, 0.0)


    .. seealso:: :func:`hex2web`, :func:`web2hex`, :func:`hex2rgb`
        :func:`rgb2hex`, :func:`hsv2rgb`,  
        :func:`hls2rgb`
    """
    # rgb_to_hsv expects normalised values !
    if normalised: upper = 1
    else: upper = 255
    check_range(r, 0, upper)
    check_range(g, 0, upper)
    check_range(b, 0, upper)
    if normalised==False:
        r,g,b = _normalise(r,g,b)
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return h, l, s


def rgb2hsv(r, g, b, normalised=True):
    """Convert an RGB value to an HSV value.
   
    :param bool normalised: if *normalised* is True, the input RGB triplet 
        should be in the range 0-1 (0-255 otherwise)
    :return: the HSV triplet. If *normalised* parameter is True, the output 
        triplet is in the range 0-1; otherwise, H in the range 0-360 and LS
        in the range 0-100.

    .. doctest::

        >>> from easydev.colors import rgb2hsv
        >>> rgb2hsv(0.5,0,1)
        (0.75, 1, 1)


    .. seealso:: :func:`hex2web`, :func:`web2hex`, :func:`hex2rgb`
        :func:`rgb2hex`, :func:`hsv2rgb`, :func:`rgb2hls`, 
        :func:`hls2rgb`
    """
    # rgb_to_hsv expects normalised values !
    if normalised: upper = 1
    else: upper = 255
    check_range(r, 0, upper)
    check_range(g, 0, upper)
    check_range(b, 0, upper)
    if normalised==False:
        r,g,b = _normalise(r,g,b)
    h,s,v = colorsys.rgb_to_hsv(r, g, b)
    return h,s,v


def hsv2rgb(h, s, v, normalised=True):
    """Convert a hue-saturation-value (HSV) value to a red-green-blue (RGB). 
    
    :param bool normalised: If *normalised* is True, the input HSV triplet
        should be in the range 0-1; otherwise, H in the range 0-360 and LS
        in the range 0-100.
    :return: the RGB triplet. The output 
        triplet is in the range 0-1 whether the input is normalised or not.
    
    .. doctest::

        >>> from easydev.colors import hsv2rgb
        >>> hsv2rgb(0.5,1,1, normalised=True)  # doctest: +SKIP
        (0, 1, 1)
   

    .. seealso:: :func:`hex2web`, :func:`web2hex`, :func:`hex2rgb`
        :func:`rgb2hex`, :func:`rgb2hsv`, :func:`rgb2hls`, 
        :func:`hls2rgb`
    .. seealso:: :func:`rgb2hex`
    """
    if normalised: upper = 1
    else: upper = 100
    if normalised: uppera = 1
    else: uppera = 360
    check_range(h, 0, uppera)
    check_range(s, 0, upper)
    check_range(v, 0, upper)
    if normalised == False:
        h,s,v = _normalise(h,s,v, mode="hsv")
    return colorsys.hsv_to_rgb(h, s, v)


def hls2rgb(h, l, s, normalised=True):
    """Convert an HLS value to a RGB value. 

    :param bool normalised: If *normalised* is True, the input HLS triplet
        should be in the range 0-1; otherwise, H in the range 0-360 and LS
        in the range 0-100.
    
    :return: the RGB triplet. The output 
        triplet is in the range 0-1 whether the input is normalised or not.

    .. doctest::

        >>> from easydev.colors import hls2rgb
        >>> hls2rgb(360, 50, 60, normalised=False)  # doctest: +SKIP
        (0.8, 0.2, 0.2)


    .. seealso:: :func:`hex2web`, :func:`web2hex`, :func:`hex2rgb`
        :func:`rgb2hex`, :func:`rgb2hsv`, :func:`hsv2rgb`, :func:`rgb2hls`, 
       
    """
    if normalised: upper = 1
    else: upper = 100
    if normalised: uppera = 1
    else: uppera = 360
    check_range(h, 0, uppera)
    check_range(s, 0, upper)
    check_range(l, 0, upper)
    if normalised == False:
        h,l,s = _normalise(h,l, s, mode="hls")
    return colorsys.hls_to_rgb(h, l, s)


def hex2dec(data):
    """convert integer (data) into hexadecimal."""
    return int(data, 16)/255.


def rgb2yuv(r,g,b):
    """Convert RGB triplet into YUV
    
    :return: YUV triplet with values between 0 and 1
    
    `YUV wikipedia <http://en.wikipedia.org/wiki/YUV>`_
    
    .. warning:: expected input must be between 0 and 1
    .. note:: the constants referenc used is  Rec. 601
    """
    check_range(r, 0, 1)
    check_range(g, 0, 1)
    check_range(b, 0, 1)
    
    #y = int(0.299 * r + 0.587 * g + 0.114 * b)
    #u = int(-0.14713 * r + -0.28886 * g + 0.436 * b)
    #v = int(0.615 * r + -0.51499 * g + -0.10001 * b)
    
    
    
    y = 0.299 * r + 0.587 * g + 0.114 * b
    u = -32591.0/221500.0 * r + -63983.0/221500.0 * g + 0.436 * b
    v = 0.615 * r + -72201./140200 * g + -7011/70100. * b
    return (y, u, v)
    
def yuv2rgb(y,u,v):
    """Convert YUV triplet into RGB
    
    `YUV <http://en.wikipedia.org/wiki/YUV>`_

    .. warning:: expected input must be between 0 and 255 (not normalised)
    
    """
    check_range(y, 0,1)
    check_range(u, 0, 1)
    check_range(v, 0, 1)
    A, B, C, D = 701.0/615.0, 25251.0/63983.0, 209599.0/361005.0, 443.0/218.0 
    r = y + A * v
    g = y - B * u - C * v
    b = y + D * u
    return (r, g, b)
    

def rgb2yuv_int(r, g, b):
    """Convert RGB triplet into YUV
    
    `YUV wikipedia <http://en.wikipedia.org/wiki/YUV>`_
    
    .. warning:: expected input must be between 0 and 255 (not normalised)
    
    """
    check_range(r, 0, 255)
    check_range(g, 0, 255)
    check_range(b, 0, 255)

    y = int(0.299 * r + 0.587 * g + 0.114 * b)
    u = int(-32591.0/221500.0 * r + -63983.0/221500.0 * g + 0.436 * b)
    v = int(0.615 * r + -72201./140200 * g + -7011/70100. * b)
   
    return (y, u, v)
 

def yuv2rgb_int(y, u, v):
    """Convert YUV triplet into RGB
    
    `YUV <http://en.wikipedia.org/wiki/YUV>`_

    .. warning:: expected input must be between 0 and 255 (not normalised)
    
    """
    check_range(y, 0, 255)
    check_range(u, 0, 255)
    check_range(v, 0, 255)
    r = int(y + 1.13983 * v)
    g = int(y - 0.39465 * u - 0.58060 * v)
    b = int(y + 2.03211 * u)
    return (r, g, b)


def _denormalise(r,g,b, mode="rgb"):
    check_param_in_list(mode, ["rgb", "hls", "hsv"])
    if mode == "rgb":
        return r*255., g*255., b*255.
    elif mode in ["hls", "hsv"]:
        return r*360., g*100., b*100.


def _normalise(r, g, b, mode="rgb"):
    check_param_in_list(mode, ["rgb", "hls", "hsv"])
    if mode == "rgb":
        return r/255., g/255., b/255.
    elif mode in ["hls", "hsv"]:
        return r/360., g/100., b/100.


def to_intensity(n):
    """Return intensity

    :param n: value between 0 and 1
    :return: value between 0 and 255; round(n*127.5+127.5)
    """
    check_range(n, 0, 1)
    return int(round(n * 127.5 + 127.5))
    

class HEX(object):
    """Class to check the validity of an hexadecimal string and get standard string

    By standard, we mean #FFFFFF (6 digits)

    """
    def __init__(self):
        pass
    def is_valid_hex_color(self, value, verbose=True):
        """Return True is the string can be interpreted as hexadecimal color
        
        Valid formats are 
     
         * #FFF
         * #0000FF
         * 0x0000FF
         * 0xFA1
        """
        try:
            self.get_standard_hex_color(value)
            return True
        except Exception as err:
            if verbose:print(err)
            return False
    
    def get_standard_hex_color(self, value):
        """Return standard hexadecimal color
        
        By standard, we mean a string that starts with # sign followed by 6
        character, e.g. #AABBFF
        """
        if isinstance(value, str)==False:
            raise TypeError("value must be a string")
        if len(value) <= 3:
            raise ValueError("input string must be of type 0xFFF, 0xFFFFFF or #FFF or #FFFFFF")
    
        if value.startswith("0x") or value.startswith("0X"):
            value =  value[2:]
        elif value.startswith("#"):
            value = value[1:]
        else:
            raise ValueError("hexa string must start with a '#' sign or '0x' string")
        value = value.upper()
        # Now, we have either FFFFFF or FFF
        # now check the length
        for x in value:
            if x not in "0123456789ABCDEF":
                raise ValueError("Found invalid hexa character {0}".format(x))
    
    
        if len(value) == 6 or len(value) == 8:
            value  = "#" + value[0:6]
        elif len(value) == 3:
            value = "#" + value[0]*2 + value[1]*2 + value[2]*2
        else:
            raise ValueError("hexa string should be 3, 6 or 8 digits. if 8 digits, last 2 are ignored")
        return value


class Color(HEX):
    """Class to ease manipulation and conversion between color codes

    You can create an instance in many differen ways. You can either use a 
    human-readable name as long as it is part of the 
    `XFree86 list <http://en.wikipedia.org/wiki/X11_color_names>`_
    You can also provide a hexadecimal string (either 3 or 6 digits). You can 
    use triplets of values corresponding to the RGB, HSV or HLS conventions. 

    Here are some examples:

    .. doctest::

        from easydev import Color

        Color("red")           # human XFree86 compatible representation
        Color("#f00")          # standard 3 hex digits
        Color("#ff0000")       # standard 6 hex digits
        Color(hsv=(0,1,0.5))
        Color(hls=(0, 1, 0.5)) # HLS triplet
        Color(rgb=(1, 0, 0))   # RGB triplet
        Color(Color("red"))    # using an instance of :class:`Color`

    Note that the RGB, HLS and HSV triplets use normalised values. If you need 
    to normalise the triplet, you can use :mod:`easydev.colors._normalise` that 
    provides a function to normalise RGB, HLS and HSV triplets::

        colors._normalise(*(255, 255, 0), mode="rgb")
        colors._normalise(*(360, 50, 100), mode="hls")

    If you provide a string, it has to be a valid string from XFree86. In addition to 
    the official names, the lower case names are valid. Besides, there are names with 
    spaces. The equivalent names without space are also valid. Therefore the name 
    "Spring Green", which is an official name can be provided as "Spring Green", 
    "spring green", "springgreen" or "SpringGreen".

    """
    # Get official color names
    colors = XFree86_colors.copy()
    # add color names without spaces
    aliases = dict([(x.replace(" ", ""),x) for x in colors.keys() if " " in x])
    # add color names without spaces in lower cases
    aliases.update([(x.replace(" ", "").lower(),x) for x in colors.keys() if " " in x])
    # add color names in lower case
    aliases.update(dict([(x.lower(),x) for x in colors.keys()]))
    aliases.update(dict([(x,x) for x in colors.keys()]))

    # keep track of all possible names
    color_names = sorted(list(set(list(colors.keys()) +list( aliases.keys()))))

    def __init__(self, name=None, rgb=None, hls=None, hsv=None):
        super(Color, self).__init__()
        self._name = None
        self._mode = None
        self._rgb = None

        # Does the user provided the name argument (first one) as a string ?
        if isinstance(name, str):
            # if so, it can be a valid human name (e.g., red) or an hex
            # assuming that valid hexadecimal starts with # or 0x, 
            # if we can interpret the string as an hexadecimal, we are done
            if self.is_valid_hex_color(name, verbose=False):
                self.hex = name
            else:
                # if not, then, the user probably provided a valid color name
                # the property will check the validity.
                self.name = name[:]
                #all other input parameters are ignored
        elif name == None:
            if rgb:
                self.rgb = rgb
            elif hls:
                self.hls = hls
            elif hsv:
                self.hsv = hsv
            else:
                raise ValueError("You must set one of the parameter")
        elif isinstance(name, Color):
            self.rgb = name.rgb
        else:
            raise ValueError("name parameter must be a string")

    def _get_name(self):
        return self._name
    def _set_name(self, name):
        check_param_in_list(name, self.color_names)
        name = self.aliases[name]
        self._name = name
        # set hex and rgb at the same time based on the name
        self.hex = self.colors[name]
    name = property(_get_name, _set_name)
    color = property(_get_name, _set_name)

    def _get_hex(self):
        return self._hex
    def _set_hex(self, value):
        # hex is an approximation made of 255 bits so do not define rgb here
        if self.is_valid_hex_color(value):
            value = self.get_standard_hex_color(value)
            self._hex = value
            if self._hex in self.colors.values():
                self._name = swapdict(self.colors, check_ambiguity=False)[self._hex]
            else:
                self._name = "undefined"
            self._rgb = hex2rgb(self._hex, normalise=True)
        else:
            # just to warn the user
            self.get_standard_hex_color(value)
    hex = property(_get_hex, _set_hex, doc="getter/setter the hexadecimal value.")
    
    def _get_rgb(self):
        return self._rgb
    def _set_rgb(self, value):
        # set name, hex and rgb
        self.hex = rgb2hex(*value , normalised=True)
        # must reset rgb with its real value (set_hex may round the rgb)
        # in _set_hex
        self._rgb = value
    rgb = property(_get_rgb, _set_rgb, 
            doc="getter/setter the RGB values (3-length tuple)")

    def _get_hsv(self):
        hsv = rgb2hsv(*self.rgb)
        return hsv
    def _set_hsv(self, value):
        # TODO: value must be normalised
        self.rgb = hsv2rgb(*value)
    hsv = property(_get_hsv, _set_hsv,
            doc="getter/setter the HSV values (3-length tuple)")

    def _get_hls(self):
        hls = rgb2hls(*self.rgb)
        return hls
    def _set_hls(self, value):
        #hls = _normalise(*value, mode="hls")
        #else:
        hls = value
        self.rgb = hls2rgb(*hls)
    hls = property(_get_hls, _set_hls,
            doc="getter/setter the HLS values (3-length tuple)")

    def _get_lightness(self):
        return self.hls[1]
    def _set_lightness(self, lightness):
        h,l,s = self.hls
        self.hls = (h,lightness,s)
    lightness = property(_get_lightness, _set_lightness,
            doc="getter/setter the lightness in the HLS triplet")

    def _get_saturation_hls(self):
        return self.hls[2]
    def _set_saturation_hls(self, saturation):
        h,l,s = self.hls
        self.hls = (h,l, saturation)
    saturation_hls = property(_get_saturation_hls, _set_saturation_hls,
            doc="getter/setter the saturation in the HLS triplet")

    def _get_hue(self):
        return self.hls[0]
    def _set_hue(self, hue):
        h,l,s = self.hls
        self.hls = (hue,l, s)
    hue = property(_get_hue, _set_hue,
            doc="getter/setter the saturation in the HLS triplet")

    def _get_red(self):
        return self.rgb[0]
    def _set_red(self, red):
        r,g,b = self.rgb
        self.rgb = (red,g,b)
    red = property(_get_red, _set_red,
            doc="getter/setter for the red color in RGB triplet")

    def _get_green(self):
        return self.rgb[1]
    def _set_green(self, green):
        r,g,b = self.rgb
        self.rgb = (r,green,b)
    green = property(_get_green, _set_green,
            doc="getter/setter for the green color in RGB triplet")

    def _get_blue(self):
        return self.rgb[2]
    def _set_blue(self, blue):
        r,g,b = self.rgb
        self.rgb = (r,g, blue)
    blue = property(_get_blue, _set_blue,
            doc="getter/setter for the blue color in RGB triplet")

    def _get_value(self):
        return self.hls[0]
    def _set_value(self, value):
        h,s,v = self.hsv
        self.hsv = (h,s,value)
    value = property(_get_value, _set_value,
            doc="getter/setter the value in the HSV triplet")

    def _get_yiq(self):
        return colorsys.rgb_to_yiq(*self.rgb)
    yiq = property(_get_yiq, doc="Getter for the YIQ triplet")

    def __str__(self):
        txt = 'Color {0}\n'.format(self.name)
        txt+= '  hexa code: {0}\n'.format(self.hex)
        txt+= '  RGB code: {0}\n'.format(self.rgb)
        txt+= '  RGB code (un-normalised): {0}\n\n'.format([x*255 for x in self.rgb])
        txt+= '  HSV code: {0}\n'.format(self.hsv)
        txt+= '  HSV code: (un-normalised) {0} {1} {2}\n\n'.format(self.hsv[0]*360, self.hsv[1]*100, self.hsv[2]*100)
        txt+= '  HLS code: {0}\n'.format(self.hls)
        txt+= '  HLS code: (un-normalised) {0} {1} {2}\n\n'.format(self.hls[0]*360, self.hls[1]*100, self.hls[2]*100)
        return txt




class ColorMapTools(object):
    """Class to create matplotlib colormaps

    This example show how to get the pre-defined colormap called *heat*
    and how to define your own colormap in 2 steps.

    .. plot::
        :include-source:
        :width: 80%

        from pylab import *
        from easydev.colors import ColorMapTools

        c = ColorMapTools()
        cmap = c.get_cmap_heat()
        c.test_cmap(cmap)

        # design your own colormap
        d = {'blue': [0,0,0,1,1,1,0], 
                'green':[0,1,1,1,0,0,0], 
                'red':  [1,1,0,0,0,1,1]}
        cmap = c.get_cmap(d, reverse=False)

        # see the results
        c.test_cmap(cmap)



    """
    def plot_rgb_from_hex_list(self, cols):
        """This functions takes a list of hexadecimal values and plots
        the RGB curves. This can be handy to figure out the RGB functions
        to be used in the :meth:`get_cmap`.

        .. plot::
            :include-source:
            :width: 60%

            from easydev.colors import ColorMapTools
            c = ColorMapTools()
            t = ['#FF0000FF', '#FF4D00FF', '#FF9900FF', '#FFE500FF',
                 '#CCFF00FF', '#80FF00FF', '#33FF00FF', '#00FF19FF', 
                 '#00FF66FF', '#00FFB2FF', '#00FFFFFF', '#00B3FFFF',
                 '#0066FFFF', '#001AFFFF', '#3300FFFF', '#7F00FFFF', 
                 '#CC00FFFF','#FF00E6FF','#FF0099FF', '#FF004DFF']
            c.plot_rgb_from_hex_list(t)


        """
        import pylab
        red = [hex2rgb(x)[0]/255. for x in cols]
        blue = [hex2rgb(x)[2]/255. for x in cols]
        green = [hex2rgb(x)[1]/255. for x in cols]
        x = pylab.linspace(0,1,len(cols))
        pylab.clf(); 
        pylab.plot(x,red,'ro-'); 
        pylab.plot(x,green,'go-'); 
        pylab.plot(x,blue,'bo-')
        pylab.ylim([-0.1,1.1])

    def get_cmap(self, colors=None, reverse=False, N=50):
        """Return a colormap object to be used within matplotlib

        :param dict colors: a dictionary that defines the RGB colors to be 
            used in the colormap. See :meth:`get_cmap_heat` for an example.
        :param bool reverse: reverse the colormap is  set to True (defaults to False)
        :param int N: Defaults to 50
        
    
        """
        # Keep these dependencies inside the function to allow 
        # installation of easydev without those dependencies
        import numpy as np
        import matplotlib
        # extracted from R, heat.colors(20)
    
        if reverse:
            for k in colors.keys():
                colors[k].reverse()
    
        # If index not given, RGB colors are evenly-spaced in colormap.
        index = np.linspace(0, 1, len(colors['red']))
    
        # Adapt color_data to the form expected by LinearSegmentedColormap.
        print(colors)
        color_data = dict((key, [(x, y, y) for x, y in zip(index, value)])
                 for key, value in list(colors.items()))
            
        
        f = matplotlib.colors.LinearSegmentedColormap
        m = f('my_color_map', color_data, N)
        return m


    def get_cmap_heat(self):
        """Return a heat colormap matplotlib-compatible colormap 

        This heat colormap should be equivalent to heat.colors() in R.
        
        ::

            >>> from easydev.colors import ColorMapTools
            >>> cmap = ColorMapTools.get_cmap_heat()
        
        You can generate the colormap based solely on this information for the RGB
        functions along::

            d=  {   'blue':[0,0,0,0,1], 
                    'green':[0,.35,.7,1,1], 
                    'red':[1,1,1,1,1]}
            cmap = ColorMapTools.get_cmap(d)

        """
        return self.get_cmap(
                {   'blue':[0,0,0,0,1], 
                    'green':[0,.35,.7,1,1], 
                    'red':[1,1,1,1,1]}, reverse=False)
    
    def get_cmap_heat_r(self):
        """Return a heat colormap matplotlib-compatible colormap
        
        Same as :meth:`get_cmap_heat` but reversed
        """ 
        return self.get_cmap(
                {   'blue':[0,0,0,0,1], 
                    'green':[0,.35,.7,1,1], 
                    'red':[1,1,1,1,1]}, reverse=True)
    
    def get_cmap_rainbow(self):
        """colormap similar to rainbow colormap from R
        
        .. note:: The red is actually appearing on both sides... Yet 
            this looks like what is coded in R 3.0.1
    
        """
        return self.get_cmap(
                {   'blue': [0,0,0,1,1,1,0], 
                    'green':[0,1,1,1,0,0,0], 
                    'red':  [1,1,0,0,0,1,1]}, reverse=False)


    def get_cmap_red_green(self):         
        return self.get_cmap(
                {   'green': [0,0.4,0.6,.75,.8,.9,1,.9,.8,.6], 
                    'blue' : [0,.4,.6,.75,.8,.7,.6,.35,.17,.1], 
                    'red':   [1,1,1,1,1,.9,.8,.6,.3,.1]}, reverse=True)

    def test_cmap(self, cmap=None):
        if cmap==None:
            cmap = self.get_cmap_heat()
        import numpy as np
        from pylab import clf, pcolor, colorbar, show, linspace 
        A,B = np.meshgrid(linspace(0,10,100), linspace(0,10,100))
        clf()
        pcolor((A-5)**2+(B-5)**2, cmap=cmap)
        colorbar()
        show()
