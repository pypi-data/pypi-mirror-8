#
# ImageViewCanvas.py -- Abstract base classes for ImageViewCanvas{Gtk,Qt}.
#
# Eric Jeschke (eric@naoj.org)
#
# Copyright (c) Eric R. Jeschke.  All rights reserved.
# This is open-source software licensed under a BSD license.
# Please see the file LICENSE.txt for details.
#
import math
import time
import numpy

from ginga.misc import Bunch
from ginga.util import wcs
from ginga import trcalc
from ginga.util.six.moves import map, zip, filter

class CanvasObjectError(Exception):
    pass

class CanvasObjectBase(object):
    """This is the abstract base class for a CanvasObject.  A CanvasObject
    is an item that can be placed on a ImageViewCanvas.

    This class defines common methods used by all such objects.
    """

    def __init__(self, **kwdargs):
        self.is_cc = False
        self.__dict__.update(kwdargs)
        self.data = None

    def initialize(self, tag, viewer, logger):
        self.tag = tag
        self.viewer = viewer
        self.logger = logger

    def set_data(self, **kwdargs):
        if self.data == None:
            self.data = Bunch.Bunch(kwdargs)
        else:
            self.data.update(kwdargs)
            
    def get_data(self, *args):
        if len(args) == 0:
            return self.data
        elif len(args) == 1:
            return self.data[args[0]]
        elif len(args) == 2:
            try:
                return self.data[args[0]]
            except KeyError:
                return args[1]
        else:
            raise CanvasObjectError("method get_data() takes at most 2 arguments")

    def redraw(self, whence=3):
        self.viewer.redraw(whence=whence)
        
    def canvascoords(self, x, y, center=True):
        if self.is_cc:
            return (x, y)
        a, b = self.viewer.canvascoords(x, y, center=center)
        return (a, b)

    def is_compound(self):
        return False
    
    def use_cc(self, tf):
        self.is_cc = tf
    
    def contains(self, x, y):
        return False
    
    def calcVertexes(self, start_x, start_y, end_x, end_y,
                     arrow_length=10, arrow_degrees=0.35):

        angle = math.atan2(end_y - start_y, end_x - start_x) + math.pi

        x1 = end_x + arrow_length * math.cos(angle - arrow_degrees);
        y1 = end_y + arrow_length * math.sin(angle - arrow_degrees);
        x2 = end_x + arrow_length * math.cos(angle + arrow_degrees);
        y2 = end_y + arrow_length * math.sin(angle + arrow_degrees);

        return (x1, y1, x2, y2)

    def calc_radius(self, x1, y1, radius):
        # scale radius
        cx1, cy1 = self.canvascoords(x1, y1)
        cx2, cy2 = self.canvascoords(x1, y1 + radius)
        # TODO: the accuracy of this calculation of radius might be improved?
        cradius = math.sqrt(abs(cy2 - cy1)**2 + abs(cx2 - cx1)**2)
        return (cx1, cy1, cradius)
    
    def swapxy(self, x1, y1, x2, y2):
        if x2 < x1:
            x1, x2 = x2, x1
        if y2 < y1:
            y1, y2 = y2, y1
        return (x1, y1, x2, y2)

    def scale_font(self):
        zoomlevel = self.viewer.get_zoom()
        if zoomlevel >= -4:
            return 14
        elif zoomlevel >= -6:
            return 12
        elif zoomlevel >= -8:
            return 10
        else:
            return 8

    def rotate_pt(self, x, y, theta, xoff=0, yoff=0):
        a = x - xoff
        b = y - yoff
        cos_t = math.cos(math.radians(theta))
        sin_t = math.sin(math.radians(theta))
        ap = (a * cos_t) - (b * sin_t)
        bp = (a * sin_t) + (b * cos_t)
        return (ap + xoff, bp + yoff)

    def move_delta(self, xoff, yoff):
        if hasattr(self, 'x'):
            self.x, self.y = self.x + xoff, self.y + yoff
        if hasattr(self, 'x1'):
            self.x1, self.y1 = self.x1 + xoff, self.y1 + yoff
        if hasattr(self, 'x2'):
            self.x2, self.y2 = self.x2 + xoff, self.y2 + yoff
        if hasattr(self, 'x3'):
            self.x3, self.y3 = self.x3 + xoff, self.y3 + yoff
            
        if hasattr(self, 'points'):
            for i in range(len(self.points)):
                (x, y) = self.points[i]
                x, y = x + xoff, y + yoff
                self.points[i] = (x, y)

    def set_point_by_index(self, i, pt):
        if hasattr(self, 'points'):
            self.points[i] = pt
        elif i == 0:
            if hasattr(self, 'x'):
                self.x, self.y = pt
            elif hasattr(self, 'x1'):
                self.x1, self.y1 = pt
        elif i == 1:
            self.x2, self.y2 = pt
        elif i == 2:
            self.x3, self.y3 = pt

    # TODO: move these into utility module
    #####
    def within_radius(self, a, b, x, y, radius):
        new_radius = math.sqrt(math.fabs(x - a)**2 + math.fabs(y - b)**2)
        if new_radius <= radius:
            return True
        return False

    def get_pt(self, points, x, y, radius=3):
        for i in range(len(points)):
            a, b = points[i]
            if self.within_radius(x, y, a, b, radius):
                return i
        return None

    def point_within_line(self, a, b, x1, y1, x2, y2, fuzz):
        if x1 > x2:
            x1, y1, x2, y2 = x2, y2, x1, y1

        # check for point OOB
        if (a + fuzz < x1) or (x2 < a - fuzz):
            return False
        elif (b + fuzz < min(y1, y2)) or (max(y1, y2) < b - fuzz): 
            return False

        dx, dy = x2 - x1, y2 - y1
        # test for vertical line
        if (dx == 0) or (dy == 0):
            # earlier boundary check will have determined if point is
            # not on the line
            return True

        slope, offset = dy / dx, y1 - x1*slope
        calcy = a*slope + offset
        contains = (b - fuzz <= calcy <= b + fuzz)
        return contains
    #####
        
    def get_reference_pt(self):
        if hasattr(self, 'x'):
            return (self.x, self.y)
        if hasattr(self, 'x1'):
            return (self.x1, self.y1)
        if hasattr(self, 'points'):
            return self.points[0]
        raise CanvasObjectError("No point of reference in object")

    def move_to(self, xdst, ydst):
        x, y = self.get_reference_pt()
        return self.move_delta(xdst - x, ydst - y)


class CompoundMixin(object):
    """A CompoundMixin makes an object that is an aggregation of other objects.
    It is used to make generic compound drawing types as well as (for example)
    layers of canvases on top of an image.
    """

    def __init__(self):
        # holds a list of objects to be drawn
        self.objects = []

    def contains(self, x, y):
        for obj in self.objects:
            if obj.contains(x, y):
                return True
        return False

    def getItemsAt(self, x, y):
        res = []
        for obj in self.objects:
            if obj.contains(x, y):
                res.insert(0, obj)
        return res
        
    def initialize(self, tag, viewer, logger):
        self.tag = tag
        self.viewer = viewer
        self.logger = logger

        # TODO: subtags for objects?
        for obj in self.objects:
            obj.initialize(None, viewer, logger)

    def is_compound(self):
        return True
    
    def use_cc(self, tf):
        for obj in self.objects:
            obj.use_cc(tf)

    def draw(self):
        for obj in self.objects:
            obj.draw()

    def getObjects(self):
        return self.objects
    
    def deleteObject(self, obj):
        self.objects.remove(obj)
        
    def deleteObjects(self, objects):
        for obj in objects:
            self.deleteObject(obj)
        
    def deleteAllObjects(self):
        self.objects = []

    def setAttrAll(self, **kwdargs):
        for obj in self.objects:
            for attrname, val in kwdargs.items():
                if hasattr(obj, attrname):
                    setattr(obj, attrname, val)
        
    def addObject(self, obj, belowThis=None):
        #obj.initialize(None, self.viewer, self.logger)
        obj.viewer = self.viewer
        if not belowThis:
            self.objects.append(obj)
        else:
            index = self.objects.index(belowThis)
            self.objects.insert(index, obj)
        
    def raiseObject(self, obj, aboveThis=None):
        if not aboveThis:
            # no reference object--move to top
            self.objects.remove(obj)
            self.objects.append(obj)
        else:
            # Force an error if the reference object doesn't exist in list
            index = self.objects.index(aboveThis)
            self.objects.remove(obj)
            index = self.objects.index(aboveThis)
            self.objects.insert(index+1, obj)

    def lowerObject(self, obj, belowThis=None):
        if not belowThis:
            # no reference object--move to bottom
            self.objects.remove(obj)
            self.objects.insert(0, obj)
        else:
            # Force an error if the reference object doesn't exist in list
            index = self.objects.index(belowThis)
            self.objects.remove(obj)
            index = self.objects.index(belowThis)
            self.objects.insert(index, obj)

    def rotate(self, theta, xoff=0, yoff=0):
        for obj in self.objects:
            obj.rotate(theta, xoff=xoff, yoff=yoff)
            
    def move_delta(self, xoff, yoff):
        for obj in self.objects:
            obj.move_delta(xoff, yoff)

    def get_reference_pt(self):
        for obj in self.objects:
            try:
                x, y = obj.get_reference_pt()
                return (x, y)
            except CanvasObjectError:
                continue
        raise CanvasObjectError("No point of reference in object")

    def move_to(self, xdst, ydst):
        x, y = self.get_reference_pt()
        for obj in self.objects:
            obj.move_delta(xdst - x, ydst - y)

class CanvasMixin(object):
    """A CanvasMixin is combined with the CompoundMixin to make a
    tag-addressible canvas-like interface.  This mixin should precede the
    CompoundMixin in the inheritance (and so, method resolution) order.
    """

    def __init__(self):
        assert isinstance(self, CompoundMixin), "Missing CompoundMixin class"
        # holds the list of tags
        self.tags = {}
        self.count = 0

    def add(self, obj, tag=None, tagpfx=None, belowThis=None, redraw=True):
        self.count += 1
        if tag:
            # user supplied a tag
            if tag in self.tags:
                raise CanvasObjectError("Tag already used: '%s'" % (tag))
        else:
            if tagpfx:
                # user supplied a tag prefix
                if tagpfx.startswith('@'):
                    raise CanvasObjectError("Tag prefix may not begin with '@'")
                tag = '%s%d' % (tagpfx, self.count)
            else:
                # make up our own tag
                tag = '@%d' % (self.count)
                
        obj.initialize(tag, self.viewer, self.logger)
        #obj.initialize(tag, self.viewer, self.viewer.logger)
        self.tags[tag] = obj
        self.addObject(obj, belowThis=belowThis)

        if redraw:
            self.redraw(whence=3)
        return tag
        
    def deleteObjectsByTag(self, tags, redraw=True):
        for tag in tags:
            try:
                obj = self.tags[tag]
                del self.tags[tag]
                super(CanvasMixin, self).deleteObject(obj)
            except Exception as e:
                continue
        
        if redraw:
            self.redraw(whence=3)

    def deleteObjectByTag(self, tag, redraw=True):
        self.deleteObjectsByTag([tag], redraw=redraw)

    def getObjectByTag(self, tag):
        obj = self.tags[tag]
        return obj

    def lookup_object_tag(self, obj):
        # TODO: we may need to have a reverse index eventually
        for tag, ref in self.tags:
            if ref == obj:
                return tag
        return None
        
    def getTagsByTagpfx(self, tagpfx):
        res = []
        keys = filter(lambda k: k.startswith(tagpfx), self.tags.keys())
        return keys

    def getObjectsByTagpfx(self, tagpfx):
        return list(map(lambda k: self.tags[k], self.getTagsByTagpfx(tagpfx)))

    def deleteAllObjects(self, redraw=True):
        self.tags = {}
        CompoundMixin.deleteAllObjects(self)
        
        if redraw:
            self.redraw(whence=3)

    def deleteObjects(self, objects, redraw=True):
        for tag, obj in self.tags.items():
            if obj in objects:
                self.deleteObjectByTag(tag, redraw=False)
        
        if redraw:
            self.redraw(whence=3)

    def deleteObject(self, obj, redraw=True):
        self.deleteObjects([obj], redraw=redraw)
        
    def raiseObjectByTag(self, tag, aboveThis=None, redraw=True):
        obj1 = self.getObjectByTag(tag)
        if not aboveThis:
            self.raiseObject(obj1)
        else:
            obj2 = self.getObjectByTag(aboveThis)
            self.raiseObject(obj1, obj2)

        if redraw:
            self.redraw(whence=3)

    def lowerObjectByTag(self, tag, belowThis=None, redraw=True):
        obj1 = self.getObjectByTag(tag)
        if not belowThis:
            self.lowerObject(obj1)
        else:
            obj2 = self.getObjectByTag(belowThis)
            self.lowerObject(obj1, obj2)

        if redraw:
            self.redraw(whence=3)
            

class DrawingMixin(object):
    """The DrawingMixin is a mixin class that adds drawing capability for
    some of the basic CanvasObject-derived types.  The setSurface method is
    used to associate a ImageViewCanvas object for layering on.
    """

    def __init__(self, drawDict):
        # For interactive drawing
        self.candraw = False
        self._isdrawing = False
        self.drawDict = drawDict
        drawtypes = drawDict.keys()
        self.drawtypes = []
        for key in ['point', 'line', 'circle', 'ellipse', 'square',
                    'rectangle', 'box', 'polygon', 'path',
                    'triangle', 'righttriangle', 'equilateraltriangle',
                    'ruler', 'compass', 'text']:
            if key in drawtypes:
                self.drawtypes.append(key)
        self.t_drawtype = 'point'
        self.t_drawparams = {}
        self._drawtext = "EDIT ME"
        self._start_x = 0
        self._start_y = 0
        self._points = []

        self._editing = False
        self._cp_index = None
        self._cp_radius = 10

        self._processTime = 0.0
        # time delta threshold for deciding whether to update the image
        self._deltaTime = 0.020
        self.drawObj = None

        self.fitsobj = None
        self.drawbuttonmask = 0x4

        # NOTE: must be mixed in with a Callback.Callbacks
        for name in ('draw-event', 'draw-down', 'draw-move', 'draw-up',
                     'drag-drop', 'edit-event'):
            self.enable_callback(name)

    def setSurface(self, viewer):
        self.viewer = viewer

        # register this canvas for events of interest
        self.set_callback('draw-down', self.draw_start)
        self.set_callback('draw-move', self.draw_motion)
        self.set_callback('draw-up', self.draw_stop)
        self.set_callback('keydown-poly_add', self.draw_poly_add)
        self.set_callback('keydown-poly_del', self.draw_poly_delete)

        #self.ui_setActive(True)

    def getSurface(self):
        return self.viewer

    def draw(self):
        super(DrawingMixin, self).draw()
        if self.drawObj:
            self.drawObj.draw()

    def set_drawtext(self, text):
        self._drawtext = text
        
    def get_ruler_distances(self, x1, y1, x2, y2):
        mode = self.t_drawparams.get('units', 'arcmin')
        try:
            image = self.viewer.get_image()
            if mode == 'arcmin':
                # Calculate RA and DEC for the three points
                # origination point
                ra_org, dec_org = image.pixtoradec(x1, y1)

                # destination point
                ra_dst, dec_dst = image.pixtoradec(x2, y2)

                # "heel" point making a right triangle
                ra_heel, dec_heel = image.pixtoradec(x2, y1)

                text_h = wcs.get_starsep_RaDecDeg(ra_org, dec_org,
                                                  ra_dst, dec_dst)
                text_x = wcs.get_starsep_RaDecDeg(ra_org, dec_org,
                                                  ra_heel, dec_heel)
                text_y = wcs.get_starsep_RaDecDeg(ra_heel, dec_heel,
                                                  ra_dst, dec_dst)
            else:
                dx = abs(x2 - x1)
                dy = abs(y2 - y1)
                dh = math.sqrt(dx**2 + dy**2)
                text_x = str(dx)
                text_y = str(dy)
                text_h = ("%.3f" % dh)
                
        except Exception as e:
            text_h = 'BAD WCS'
            text_x = 'BAD WCS'
            text_y = 'BAD WCS'

        return (text_x, text_y, text_h)

    def _draw_update(self, data_x, data_y):

        klass = self.drawDict[self.t_drawtype]
        obj = None
        
        if self.t_drawtype == 'point':
            radius = max(abs(self._start_x - data_x),
                         abs(self._start_y - data_y))
            obj = klass(self._start_x, self._start_y, radius,
                        **self.t_drawparams)

        elif self.t_drawtype == 'compass':
            radius = max(abs(self._start_x - data_x),
                         abs(self._start_y - data_y))
            image = self.viewer.get_image()
            x, y, xn, yn, xe, ye = image.calc_compass_radius(self._start_x,
                                                             self._start_y,
                                                             radius)
            obj = klass(x, y, xn, yn, xe, ye, **self.t_drawparams)

        elif self.t_drawtype == 'rectangle':
            obj = klass(self._start_x, self._start_y,
                        data_x, data_y, **self.t_drawparams)
                
        elif self.t_drawtype == 'square':
                len_x = self._start_x - data_x
                len_y = self._start_y - data_y
                length = max(abs(len_x), abs(len_y))
                len_x = cmp(len_x, 0) * length
                len_y = cmp(len_y, 0) * length
                obj = klass(self._start_x, self._start_y,
                            self._start_x-len_x, self._start_y-len_y,
                            **self.t_drawparams)

        elif self.t_drawtype == 'equilateraltriangle':
                len_x = self._start_x - data_x
                len_y = self._start_y - data_y
                length = max(abs(len_x), abs(len_y))
                obj = klass(self._start_x, self._start_y,
                            length, length, **self.t_drawparams)
            
        elif self.t_drawtype in ('box', 'ellipse', 'triangle'):
            xradius = abs(self._start_x - data_x)
            yradius = abs(self._start_y - data_y)
            obj = klass(self._start_x, self._start_y, xradius, yradius,
                        **self.t_drawparams)

        elif self.t_drawtype == 'circle':
            radius = math.sqrt(abs(self._start_x - data_x)**2 + 
                               abs(self._start_y - data_y)**2 )
            obj = klass(self._start_x, self._start_y, radius,
                        **self.t_drawparams)

        elif self.t_drawtype == 'line':
            obj = klass(self._start_x, self._start_y, data_x, data_y,
                        **self.t_drawparams)

        elif self.t_drawtype == 'righttriangle':
            obj = klass(self._start_x, self._start_y, data_x, data_y,
                        **self.t_drawparams)

        elif self.t_drawtype == 'polygon':
            points = list(self._points)
            points.append((data_x, data_y))
            obj = klass(points, **self.t_drawparams)

        elif self.t_drawtype == 'path':
            points = list(self._points)
            points.append((data_x, data_y))
            obj = klass(points, **self.t_drawparams)

        elif self.t_drawtype == 'text':
            obj = klass(self._start_x, self._start_y, self._drawtext,
                        **self.t_drawparams)

        elif self.t_drawtype == 'ruler':
            text_x, text_y, text_h = self.get_ruler_distances(self._start_x,
                                                              self._start_y,
                                                              data_x, data_y)
            obj = klass(self._start_x, self._start_y, data_x, data_y,
                        text_x=text_x, text_y=text_y, text_h = text_h,
                        **self.t_drawparams)

        if obj != None:
            obj.initialize(None, self.viewer, self.logger)
            #obj.initialize(None, self.viewer, self.viewer.logger)
            self.drawObj = obj
            if time.time() - self._processTime > self._deltaTime:
                self.processDrawing()
            
        return True
            
    def _edit_update(self, data_x, data_y):
        if self._cp_index != None:
            self.drawObj.set_point_by_index(self._cp_index, (data_x, data_y))

            if time.time() - self._processTime > self._deltaTime:
                self.processDrawing()
        return True
        
    def draw_start(self, canvas, action, data_x, data_y):
        if not self.candraw:
            return False

        if self._editing and (self.drawObj != None):
            #print("editing %s" % str(self.drawObj))
            edit_pts = self.drawObj.edit_points()
            i = self.drawObj.get_pt(edit_pts, data_x, data_y,
                                    self._cp_radius)
            if i != None:
                #print("editing a cp")
                # editing a control point from an existing object
                self._isdrawing = True
                self._cp_index = i
                self._edit_update(data_x, data_y)

            elif not self.drawObj.contains(data_x, data_y):
                #print("no operation")
                return False

            else:
                # TODO: moving an existing object
                #print("moving an object")
                return False

        else:
            #print("drawing an object")
            # drawing a new object
            self._isdrawing = True
            self._points = [(data_x, data_y)]
            self._start_x = data_x
            self._start_y = data_y
            self._draw_update(data_x, data_y)

        self.processDrawing()
        return True

    def draw_stop(self, canvas, button, data_x, data_y):
        if self.candraw and self._isdrawing:
            self._isdrawing = False

            if self._editing:
                self._edit_update(data_x, data_y)
                self._cp_index = None
                objtag = self.lookup_object_tag(self.drawObj)
                self.make_callback('edit-event', objtag)
                return True
                
            self._draw_update(data_x, data_y)
            obj, self.drawObj = self.drawObj, None
            self._points = []

            if obj:
                objtag = self.add(obj, redraw=True)
                self.make_callback('draw-event', objtag)
                return True
            else:
                self.processDrawing()

            return True

    def draw_poly_add(self, canvas, action, data_x, data_y):
        if self.candraw and (self.t_drawtype in ('polygon', 'path')):
            self._points.append((data_x, data_y))
        return True

    def draw_poly_delete(self, canvas, action, data_x, data_y):
        if self.candraw and (self.t_drawtype in ('polygon', 'path')):
            if len(self._points) > 0:
                self._points.pop()
        return True

    def draw_motion(self, canvas, button, data_x, data_y):
        if self._isdrawing:
            if self._editing and (self.drawObj != None) and (self._cp_index != None):
                self._edit_update(data_x, data_y)
            else:
                self._draw_update(data_x, data_y)
            return True

    def processDrawing(self):
        self._processTime = time.time()
        self.viewer.redraw(whence=3)
    
    def isDrawing(self):
        return self._isdrawing
    
    def enable_draw(self, tf):
        self.candraw = tf
        
    def set_drawcolor(self, colorname):
        self.t_drawparams['color'] = colorname
        
    def set_drawtype(self, drawtype, **drawparams):
        drawtype = drawtype.lower()
        assert drawtype in self.drawtypes, \
               CanvasObjectError("Bad drawing type '%s': must be one of %s" % (
            drawtype, self.drawtypes))
        self.t_drawtype = drawtype
        self.t_drawparams = drawparams.copy()

    def get_drawtypes(self):
        return self.drawtypes

    def get_drawtype(self):
        return self.t_drawtype

    def getDrawClass(self, drawtype):
        drawtype = drawtype.lower()
        klass = self.drawDict[drawtype]
        return klass
        
    def get_drawparams(self):
        return self.t_drawparams.copy()

#
#   ==== BASE CLASSES FOR GRAPHICS OBJECTS ====
#
class TextBase(CanvasObjectBase):
    """Draws text on a ImageViewCanvas.
    Parameters are:
    x, y: 0-based coordinates in the data space
    text: the text to draw
    Optional parameters for fontsize, color, etc.
    """

    def __init__(self, x, y, text, font='Sans Serif', fontsize=None,
                 color='yellow', alpha=1.0):
        self.kind = 'text'
        super(TextBase, self).__init__(color=color, alpha=alpha,
                                       x=x, y=y, font=font, fontsize=fontsize,
                                       text=text)

    def rotate(self, theta, xoff=0, yoff=0):
        self.x, self.y = self.rotate_pt(self.x, self.y, theta,
                                        xoff=xoff, yoff=yoff)

    def edit_points(self):
        return [(self.x, self.y)]

class PolygonBase(CanvasObjectBase):
    """Draws a polygon on a ImageViewCanvas.
    Parameters are:
    List of (x, y) points in the polygon.  The last one is assumed to
    be connected to the first.
    Optional parameters for linesize, color, etc.
    """

    def __init__(self, points, color='red',
                 linewidth=1, linestyle='solid', cap=None,
                 fill=False, fillcolor=None, alpha=1.0,
                 fillalpha=1.0, rot_deg=0.0):
        self.kind = 'polygon'
        
        super(PolygonBase, self).__init__(points=points, color=color,
                                          linewidth=linewidth, cap=cap,
                                          linestyle=linestyle, alpha=alpha,
                                          fill=fill, fillcolor=fillcolor,
                                          fillalpha=fillalpha,
                                          rot_deg=rot_deg)

    def get_center_pt(self):
        P = numpy.array(self.points + [self.points[0]])
        x = P[:, 0]
        y = P[:, 1]

        a = x[:-1] * y[1:]
        b = y[:-1] * x[1:]
        A = numpy.sum(a - b) / 2.
        
        cx = x[:-1] + x[1:]
        cy = y[:-1] + y[1:]

        Cx = numpy.sum(cx * (a - b)) / (6. * A)
        Cy = numpy.sum(cy * (a - b)) / (6. * A)
        return (Cx, Cy)
    
    def get_cpoints(self):
        rpoints = self.points
        if self.rot_deg != 0.0:
            # rotate vertices according to rotation
            x, y = self.get_center_pt()
            rpoints = tuple(map(lambda p: self.rotate_pt(p[0], p[1],
                                                         self.rot_deg,
                                                         xoff=x, yoff=y),
                                self.points))
        cpoints = tuple(map(lambda p: self.canvascoords(p[0], p[1]),
                            rpoints))
        return cpoints

    def contains(self, x, y):
        # rotate point back to cartesian alignment for test
        cx, cy = self.get_center_pt()
        xp, yp = self.rotate_pt(x, y, -self.rot_deg,
                                xoff=cx, yoff=cy)
        # NOTE: we use a version of the ray casting algorithm
        # See: http://alienryderflex.com/polygon/
        result = False
        xj, yj = self.points[-1]
        for (xi, yi) in self.points:
            if ((((yi < yp) and (yj >= yp)) or
                 ((yj < yp) and (yi >= yp))) and
                ((xi <= xp) or (xj <= xp))):
                cross = (xi + float(yp - yi)/(yj - yi)*(xj - xi)) < xp
                result ^= cross
            xj, yj = xi, yi

        return result
            
    def rotate(self, theta, xoff=0, yoff=0):
        newpts = list(map(lambda p: self.rotate_pt(p[0], p[1], theta,
                                              xoff=xoff, yoff=yoff),
                          self.points))
        self.points = newpts

    def edit_points(self):
        return self.points


class RectangleBase(CanvasObjectBase):
    """Draws a rectangle on a ImageViewCanvas.
    Parameters are:
    x1, y1: 0-based coordinates of one corner in the data space
    x2, y2: 0-based coordinates of the opposing corner in the data space
    Optional parameters for linesize, color, etc.

    PLEASE NOTE: that the coordinates will be arranged in the final
    object such that x1, y1 always refers to the lower-left corner.
    """

    def __init__(self, x1, y1, x2, y2, color='red',
                 linewidth=1, linestyle='solid', cap=None,
                 fill=False, fillcolor=None, alpha=1.0,
                 drawdims=False, font='Sans Serif', fillalpha=1.0):
        self.kind = 'rectangle'
        # ensure that rectangles are always bounded LL to UR
        x1, y1, x2, y2 = self.swapxy(x1, y1, x2, y2)
        
        super(RectangleBase, self).__init__(color=color,
                                            x1=x1, y1=y1, x2=x2, y2=y2,
                                            linewidth=linewidth, cap=cap,
                                            linestyle=linestyle,
                                            fill=fill, fillcolor=fillcolor,
                                            alpha=alpha, fillalpha=fillalpha,
                                            drawdims=drawdims, font=font)
        
    def contains(self, x, y):
        if ((x >= self.x1) and (x <= self.x2) and
            (y >= self.y1) and (y <= self.y2)):
            return True
        return False

    def rotate(self, theta, xoff=0, yoff=0):
        x1, y1 = self.rotate_pt(self.x1, self.y1, theta,
                                xoff=xoff, yoff=yoff)
        x2, y2 = self.rotate_pt(self.x2, self.y2, theta,
                                xoff=xoff, yoff=yoff)
        self.x1, self.y1, self.x2, self.y2 = self.swapxy(x1, y1, x2, y2)

    def edit_points(self):
        return [(self.x1, self.y1), (self.x2, self.y2)]

    def move_point(self):
        x, y = (self.x1 + self.x2) / 2.0, (self.y1 + self.y2) / 2.0
        return (x, y)

    def toPolygon(self):
        points = [(self.x1, self.y1), (self.x2, self.y1),
                  (self.x2, self.y2), (self.x1, self.y2)]
        p = Polygon(points, color=self.color,
                    linewidth=self.linewidth, linestyle=self.linestyle,
                    cap=self.cap, fill=self.fill, fillcolor=self.fillcolor,
                    alpha=self.alpha, fillalpha=self.fillalpha)
        return p


class BoxBase(CanvasObjectBase):
    """Draws a box on a ImageViewCanvas.
    Parameters are:
    x, y: 0-based coordinates of the center in the data space
    xradius, yradius: radii based on the number of pixels in data space
    Optional parameters for linesize, color, etc.
    """

    def __init__(self, x, y, xradius, yradius, color='red',
                 linewidth=1, linestyle='solid', cap=None,
                 fill=False, fillcolor=None, alpha=1.0, fillalpha=1.0,
                 rot_deg=0.0):
        super(BoxBase, self).__init__(color=color,
                                      linewidth=linewidth, cap=cap,
                                      linestyle=linestyle,
                                      fill=fill, fillcolor=fillcolor,
                                      alpha=alpha, fillalpha=fillalpha,
                                      x=x, y=y, xradius=xradius,
                                      yradius=yradius, rot_deg=0.0)
        self.kind = 'box'

    def get_cpoints(self):
        # rotate corners according to box rotation
        rpoints = tuple(map(lambda p: self.rotate_pt(p[0], p[1], self.rot_deg,
                                                     xoff=self.x, yoff=self.y),
                            ((self.x - self.xradius, self.y - self.yradius),
                             (self.x + self.xradius, self.y - self.yradius),
                             (self.x + self.xradius, self.y + self.yradius),
                             (self.x - self.xradius, self.y + self.yradius))))
        # calculate canvas positions of corners
        cpoints = tuple(map(lambda p: self.canvascoords(p[0], p[1]),
                            rpoints))
        return cpoints
    
    def contains(self, x, y):
        # rotate point back to cartesian alignment for test
        xp, yp = self.rotate_pt(x, y, -self.rot_deg,
                                xoff=self.x, yoff=self.y)
        x1, y1 = self.x - self.xradius, self.y - self.yradius
        x2, y2 = self.x + self.xradius, self.y + self.yradius
        if ((xp >= x1) and (xp <= x2) and
            (yp >= y1) and (yp <= y2)):
            return True
        return False

    def rotate(self, theta, xoff=0, yoff=0):
        self.x, self.y = self.rotate_pt(self.x, self.y, theta,
                                        xoff=xoff, yoff=yoff)

    def edit_points(self):
        return [(self.x, self.y)]


class CircleBase(CanvasObjectBase):
    """Draws a circle on a ImageViewCanvas.
    Parameters are:
    x, y: 0-based coordinates of the center in the data space
    radius: radius based on the number of pixels in data space
    Optional parameters for linesize, color, etc.
    """

    def __init__(self, x, y, radius, color='yellow',
                 linewidth=1, linestyle='solid', cap=None,
                 fill=False, fillcolor=None, alpha=1.0, fillalpha=1.0):
        super(CircleBase, self).__init__(color=color,
                                         linewidth=linewidth, cap=cap,
                                         linestyle=linestyle,
                                         fill=fill, fillcolor=fillcolor,
                                         alpha=alpha, fillalpha=fillalpha,
                                         x=x, y=y, radius=radius)
        self.kind = 'circle'

    def contains(self, x, y):
        radius = math.sqrt(math.fabs(x - self.x)**2 + math.fabs(y - self.y)**2)
        if radius <= self.radius:
            return True
        return False

    def rotate(self, theta, xoff=0, yoff=0):
        self.x, self.y = self.rotate_pt(self.x, self.y, theta,
                                        xoff=xoff, yoff=yoff)

    def edit_points(self):
        return [(self.x, self.y)]


class EllipseBase(CanvasObjectBase):
    """Draws an ellipse on a ImageViewCanvas.
    Parameters are:
    x, y: 0-based coordinates of the center in the data space
    xradius, yradius: radii based on the number of pixels in data space
    Optional parameters for linesize, color, etc.
    """

    def __init__(self, x, y, xradius, yradius, color='yellow',
                 linewidth=1, linestyle='solid', cap=None,
                 fill=False, fillcolor=None, alpha=1.0, fillalpha=1.0,
                 rot_deg=0.0):
        super(EllipseBase, self).__init__(color=color,
                                          linewidth=linewidth, cap=cap,
                                          linestyle=linestyle,
                                          fill=fill, fillcolor=fillcolor,
                                          alpha=alpha, fillalpha=fillalpha,
                                          x=x, y=y, xradius=xradius,
                                          yradius=yradius, rot_deg=0.0)
        self.kind = 'ellipse'

    def get_center_radii_rot(self):
        scale_x, scale_y = self.viewer.get_scale_xy()
        rot_deg = self.viewer.get_rotation() + self.rot_deg

        # calculate center of ellipse and radii in canvas coordinates
        cx, cy = self.canvascoords(self.x, self.y)
        cxr, cyr = scale_x * self.xradius, scale_y * self.yradius

        # swap scale if axes are swapped in transform
        flipx, flipy, swapxy = self.viewer.get_transforms()
        if swapxy:
            cxr, cyr = cyr, cxr

        return (cx, cy, cxr, cyr, rot_deg)
            
    def contains(self, x, y):
        # rotate point back to cartesian alignment for test
        xp, yp = self.rotate_pt(x, y, -self.rot_deg,
                                xoff=self.x, yoff=self.y)
        # See http://math.stackexchange.com/questions/76457/check-if-a-point-is-within-an-ellipse
        res = (((xp - self.x)**2) / self.xradius**2 + 
               ((yp - self.y)**2) / self.yradius**2)
        if res <= 1.0:
            return True
        return False

    def rotate(self, theta, xoff=0, yoff=0):
        self.x, self.y = self.rotate_pt(self.x, self.y, theta,
                                        xoff=xoff, yoff=yoff)

    def edit_points(self):
        return [(self.x, self.y)]


class PointBase(CanvasObjectBase):
    """Draws a point on a ImageViewCanvas.
    Parameters are:
    x, y: 0-based coordinates of the center in the data space
    radius: radius based on the number of pixels in data space
    Optional parameters for linesize, color, style, etc.
    Currently the only styles are 'cross' and 'plus'.
    """

    def __init__(self, x, y, radius, style='cross', color='yellow',
                 linewidth=1, linestyle='solid', alpha=1.0, cap=None):
        self.kind = 'point'
        super(PointBase, self).__init__(color=color, alpha=alpha,
                                        linewidth=linewidth,
                                        linestyle=linestyle,
                                        x=x, y=y, radius=radius,
                                        cap=cap, style=style)
        
    def contains(self, x, y):
        if (x == self.x) and (y == self.y):
            return True
        return False

    def rotate(self, theta, xoff=0, yoff=0):
        self.x, self.y = self.rotate_pt(self.x, self.y, theta,
                                        xoff=xoff, yoff=yoff)
    def edit_points(self):
        return [(self.x, self.y)]


class LineBase(CanvasObjectBase):
    """Draws a line on a ImageViewCanvas.
    Parameters are:
    x1, y1: 0-based coordinates of one end in the data space
    x2, y2: 0-based coordinates of the opposing end in the data space
    Optional parameters for linesize, color, etc.
    """

    def __init__(self, x1, y1, x2, y2, color='red',
                 linewidth=1, linestyle='solid', alpha=1.0,
                 cap=None):
        self.kind = 'line'
        super(LineBase, self).__init__(color=color, alpha=alpha,
                                       linewidth=linewidth, cap=cap,
                                       linestyle=linestyle,
                                       x1=x1, y1=y1, x2=x2, y2=y2)
        
    def rotate(self, theta, xoff=0, yoff=0):
        self.x1, self.y1 = self.rotate_pt(self.x1, self.y1, theta,
                                          xoff=xoff, yoff=yoff)
        self.x2, self.y2 = self.rotate_pt(self.x2, self.y2, theta,
                                          xoff=xoff, yoff=yoff)

    def edit_points(self):
        return [(self.x1, self.y1), (self.x2, self.y2)]

    def get_reference_pt(self):
        # calculate center point of line
        x = (self.x2 - self.x1) / 2.0 + self.x1
        y = (self.y2 - self.y1) / 2.0 + self.y1
        return (x, y)


class PathBase(CanvasObjectBase):
    """Draws a path on a ImageViewCanvas.
    Parameters are:
    List of (x, y) points in the polygon.  
    Optional parameters for linesize, color, etc.
    """

    def __init__(self, points, color='red',
                 linewidth=1, linestyle='solid', cap=None,
                 alpha=1.0):
        self.kind = 'path'
        
        super(PathBase, self).__init__(points=points, color=color,
                                       linewidth=linewidth, cap=cap,
                                       linestyle=linestyle, alpha=alpha)
        
    def rotate(self, theta, xoff=0, yoff=0):
        newpts = list(map(lambda p: self.rotate_pt(p[0], p[1], theta,
                                              xoff=xoff, yoff=yoff),
                          self.points))
        self.points = newpts

    def edit_points(self):
        return self.points


class CompassBase(CanvasObjectBase):
    """Draws a WCS compass on a ImageViewCanvas.
    Parameters are:
    x1, y1: 0-based coordinates of the center in the data space
    x2, y2: 0-based coordinates of the 'North' end in the data space
    x3, y3: 0-based coordinates of the 'East' end in the data space
    Optional parameters for linesize, color, etc.
    """

    def __init__(self, x1, y1, x2, y2, x3, y3, color='skyblue',
                 linewidth=1, fontsize=None, font='Sans Serif',
                 alpha=1.0, linestyle='solid', cap='ball'):
        self.kind = 'compass'
        super(CompassBase, self).__init__(color=color, alpha=alpha,
                                          linewidth=linewidth, cap=cap,
                                          linestyle=linestyle,
                                          x1=x1, y1=y1, x2=x2, y2=y2, x3=x3, y3=y3,
                                          font=font, fontsize=fontsize)
    def edit_points(self):
        return [(self.x, self.y)]

        
class RightTriangleBase(CanvasObjectBase):
    """Draws a right triangle on a ImageViewCanvas.
    Parameters are:
    x1, y1: 0-based coordinates of one end of the diagonal in the data space
    x2, y2: 0-based coordinates of the opposite end of the diagonal
    Optional parameters for linesize, color, etc.
    """

    def __init__(self, x1, y1, x2, y2, color='pink',
                 linewidth=1, linestyle='solid', cap=None,
                 fill=False, fillcolor=None, alpha=1.0, fillalpha=1.0):
        self.kind='righttriangle'
        super(RightTriangleBase, self).__init__(color=color, alpha=alpha,
                                                linewidth=linewidth, cap=cap,
                                                linestyle=linestyle,
                                                fill=fill, fillcolor=fillcolor,
                                                fillalpha=fillalpha,
                                                x1=x1, y1=y1, x2=x2, y2=y2)

    def edit_points(self):
        return [(self.x1, self.y1), (self.x2, self.y2)]


class TriangleBase(CanvasObjectBase):
    """Draws a triangle on a ImageViewCanvas.
    Parameters are:
    x, y: 0-based coordinates of the center in the data space
    xradius, yradius: radii based on the number of pixels in data space
    Optional parameters for linesize, color, etc.
    """

    def __init__(self, x, y, xradius, yradius, color='pink',
                 linewidth=1, linestyle='solid', cap=None,
                 fill=False, fillcolor=None, alpha=1.0, fillalpha=1.0,
                 rot_deg=0.0):
        self.kind='triangle'
        super(TriangleBase, self).__init__(color=color, alpha=alpha,
                                           linewidth=linewidth, cap=cap,
                                           linestyle=linestyle,
                                           fill=fill, fillcolor=fillcolor,
                                           fillalpha=fillalpha,
                                           x=x, y=y, xradius=xradius,
                                           yradius=yradius, rot_deg=rot_deg)

    def get_points(self):
        return ((self.x - 2*self.xradius, self.y - self.yradius),
                (self.x + 2*self.xradius, self.y - self.yradius),
                (self.x, self.y + self.yradius))
    
    def get_center_pt(self):
        P = numpy.array(self.get_points())
        x = P[:, 0]
        y = P[:, 1]
        Cx = numpy.sum(x) / 3.
        Cy = numpy.sum(y) / 3.
        return (Cx, Cy)

    def get_cpoints(self):
        cx, cy = self.get_center_pt()
        # rotate corners according to triangle rotation
        rpoints = tuple(map(lambda p: self.rotate_pt(p[0], p[1], self.rot_deg,
                                                     xoff=cx, yoff=cy),
                            self.get_points()))
        # calculate canvas positions of corners
        cpoints = tuple(map(lambda p: self.canvascoords(p[0], p[1]),
                            rpoints))
        return cpoints
    
    def contains(self, x, y):
        # rotate point back to cartesian alignment for test
        xp, yp = self.rotate_pt(x, y, -self.rot_deg,
                                xoff=self.x, yoff=self.y)
        # calculate vertices
        ax, ay = self.x - self.xradius, self.y - self.yradius
        bx, by = self.x + self.xradius, self.y - self.yradius
        cx, cy = self.x, self.y + self.yradius

        as_x, as_y = xp - ax, yp - ay
        s_ab = (bx - ax)*as_y - (by - ay)*as_x > 0
        
        if (cx - ax)*as_y - (cy - ay)*as_x > 0 == s_ab:
            return False
        if (cx - bx)*(yp - by) - (cy - by)*(xp - bx) > 0 != s_ab:
            return False

        return True
    
    def edit_points(self):
        return [(self.x, self.y)]

    def rotate(self, theta, xoff=0, yoff=0):
        self.x, self.y = self.rotate_pt(self.x, self.y, theta,
                                        xoff=xoff, yoff=yoff)


class RulerBase(CanvasObjectBase):
    """Draws a WCS ruler (like a right triangle) on a ImageViewCanvas.
    Parameters are:
    x1, y1: 0-based coordinates of one end of the diagonal in the data space
    x2, y2: 0-based coordinates of the opposite end of the diagonal
    Optional parameters for linesize, color, etc.
    """

    def __init__(self, x1, y1, x2, y2, color='red', color2='yellow',
                 alpha=1.0, linewidth=1, linestyle='solid',
                 cap='ball', units='arcsec',
                 font='Sans Serif', fontsize=None,
                 text_x='kon', text_y='ban', text_h='wa'):
        self.kind = 'ruler'
        super(RulerBase, self).__init__(color=color, color2=color2,
                                        alpha=alpha,
                                        linewidth=linewidth, cap=cap,
                                        linestyle=linestyle,
                                        x1=x1, y1=y1, x2=x2, y2=y2,
                                        font=font, fontsize=fontsize,
                                        text_x=text_x, text_y=text_y,
                                        text_h=text_h)

    def edit_points(self):
        return [(self.x1, self.y1), (self.x2, self.y2)]


class Image(CanvasObjectBase):
    """Draws an image on a ImageViewCanvas.
    Parameters are:
    x, y: 0-based coordinates of one corner in the data space
    image: the image, which must be an RGBImage object
    """

    def __init__(self, x, y, image, alpha=None, flipy=False, optimize=True):
        self.kind = 'image'
        super(Image, self).__init__(x=x, y=y, image=image, alpha=alpha,
                                    flipy=flipy)

        self._drawn = False
        self._optimize = optimize
        # these hold intermediate step results. Depending on value of
        # `whence` they may not need to be recomputed.
        self._cutout = None
        # calculated location of overlay on canvas
        self._cvs_x = 0
        self._cvs_y = 0

    def get_coords(self):
        x1, y1 = self.x, self.y
        x2, y2 = x1 + self.image.width, y1 + self.image.height
        return (x1, y1, x2, y2)

    def contains(self, x, y):
        x2, y2 = self.x + self.image.width, self.y + self.image.height
        if ((x >= self.x) and (x <= x2) and
            (y >= self.y) and (y <= y2)):
            return True
        return False

    ## def rotate(self, theta, xoff=0, yoff=0):
    ##     x, y = self.rotate_pt(self.x, self.y, theta,
    ##                             xoff=xoff, yoff=yoff)
    ##     self.x, self.y = x, y

    def draw(self):
        if not self._drawn:
            self._drawn = True
            self.viewer.redraw(whence=2)
    
    def draw_image(self, dstarr, whence=0.0):
        #print("redraw whence=%f" % (whence))
        dst_order = self.viewer.get_rgb_order()
        image_order = self.image.get_order()

        if (whence <= 0.0) or (self._cutout == None) or (not self._optimize):
            # get extent of our data coverage in the window
            ((x0, y0), (x1, y1), (x2, y2), (x3, y3)) = self.viewer.get_pan_rect()
            xmin = int(min(x0, x1, x2, x3))
            ymin = int(min(y0, y1, y2, y3))
            xmax = int(max(x0, x1, x2, x3))
            ymax = int(max(y0, y1, y2, y3))

            # destination location in data_coords
            #dst_x, dst_y = self.x, self.y + ht
            dst_x, dst_y = self.x, self.y

            a1, b1, a2, b2 = 0, 0, self.image.width, self.image.height

            # calculate the cutout that we can make and scale to merge
            # onto the final image--by only cutting out what is necessary
            # this speeds scaling greatly at zoomed in sizes
            dst_x, dst_y, a1, b1, a2, b2 = \
                   trcalc.calc_image_merge_clip(xmin, ymin, xmax, ymax,
                                                dst_x, dst_y, a1, b1, a2, b2)

            # is image completely off the screen?
            if (a2 - a1 <= 0) or (b2 - b1 <= 0):
                # no overlay needed
                #print "no overlay needed"
                return

            # cutout and scale the piece appropriately
            scale_x, scale_y = self.viewer.get_scale_xy()
            res = self.image.get_scaled_cutout(a1, b1, a2, b2,
                                               scale_x, scale_y,
                                               #flipy=self.flipy,
                                               method='basic')

            # don't ask for an alpha channel from overlaid image if it
            # doesn't have one
            dst_order = self.viewer.get_rgb_order()
            image_order = self.image.get_order()
            ## if ('A' in dst_order) and not ('A' in image_order):
            ##     dst_order = dst_order.replace('A', '')

            ## if dst_order != image_order:
            ##     # reorder result to match desired rgb_order by backend
            ##     self._cutout = trcalc.reorder_image(dst_order, res.data,
            ##                                         image_order)
            ## else:
            ##     self._cutout = res.data
            self._cutout = res.data

            # calculate our offset from the pan position
            pan_x, pan_y = self.viewer.get_pan()
            #print "pan x,y=%f,%f" % (pan_x, pan_y)
            off_x, off_y = dst_x - pan_x, dst_y - pan_y
            # scale offset
            off_x *= scale_x
            off_y *= scale_y
            #print "off_x,y=%f,%f" % (off_x, off_y)

            # dst position in the pre-transformed array should be calculated
            # from the center of the array plus offsets
            ht, wd, dp = dstarr.shape
            self._cvs_x = int(round(wd / 2.0  + off_x))
            self._cvs_y = int(round(ht / 2.0  + off_y))

        # composite the image into the destination array at the
        # calculated position
        trcalc.overlay_image(dstarr, self._cvs_x, self._cvs_y, self._cutout,
                             dst_order=dst_order, src_order=image_order,
                             alpha=self.alpha, flipy=False)

    def edit_points(self):
        return [(self.x, self.y)]

    def set_image(self, image):
        self.image = image
        self._drawn = False
        self._cutout = None


class NormImage(Image):
    """Draws an image on a ImageViewCanvas.

    Parameters are:
    x, y: 0-based coordinates of one corner in the data space
    image: the image, which must be an RGBImage object
    """

    def __init__(self, x, y, image, alpha=None, 
                 optimize=True, rgbmap=None, autocuts=None):
        self.kind = 'normimage'
        super(NormImage, self).__init__(x=x, y=y, image=image, alpha=alpha,
                                        optimize=optimize)
        self.rgbmap = rgbmap
        self.autocuts = autocuts

        # these hold intermediate step results. Depending on value of
        # `whence` they may not need to be recomputed.
        self._prergb = None
        self._rgbarr = None

    def draw_image(self, dstarr, whence=0.0):
        #print("redraw whence=%f" % (whence))

        if (whence <= 0.0) or (self._cutout == None) or (not self._optimize):
            # get extent of our data coverage in the window
            ((x0, y0), (x1, y1), (x2, y2), (x3, y3)) = self.viewer.get_pan_rect()
            xmin = int(min(x0, x1, x2, x3))
            ymin = int(min(y0, y1, y2, y3))
            xmax = int(max(x0, x1, x2, x3))
            ymax = int(max(y0, y1, y2, y3))

            # destination location in data_coords
            dst_x, dst_y = self.x, self.y

            a1, b1, a2, b2 = 0, 0, self.image.width, self.image.height

            # calculate the cutout that we can make and scale to merge
            # onto the final image--by only cutting out what is necessary
            # this speeds scaling greatly at zoomed in sizes
            dst_x, dst_y, a1, b1, a2, b2 = \
                   trcalc.calc_image_merge_clip(xmin, ymin, xmax, ymax,
                                                dst_x, dst_y, a1, b1, a2, b2)

            # is image completely off the screen?
            if (a2 - a1 <= 0) or (b2 - b1 <= 0):
                # no overlay needed
                #print "no overlay needed"
                return

            # cutout and scale the piece appropriately
            scale_x, scale_y = self.viewer.get_scale_xy()
            res = self.image.get_scaled_cutout(a1, b1, a2, b2,
                                                scale_x, scale_y)
            self._cutout = res.data

            # calculate our offset from the pan position
            pan_x, pan_y = self.viewer.get_pan()
            #print "pan x,y=%f,%f" % (pan_x, pan_y)
            off_x, off_y = dst_x - pan_x, dst_y - pan_y
            # scale offset
            off_x *= scale_x
            off_y *= scale_y
            #print "off_x,y=%f,%f" % (off_x, off_y)

            # dst position in the pre-transformed array should be calculated
            # from the center of the array plus offsets
            ht, wd, dp = dstarr.shape
            self._cvs_x = int(round(wd / 2.0  + off_x))
            self._cvs_y = int(round(ht / 2.0  + off_y))

        if self.rgbmap != None:
            rgbmap = self.rgbmap
        else:
            rgbmap = self.viewer.get_rgbmap()

        if (whence <= 1.0) or (self._prergb == None) or (not self._optimize):
            # apply visual changes prior to color mapping (cut levels, etc)
            vmax = rgbmap.get_hash_size() - 1
            newdata = self.apply_visuals(self._cutout, 0, vmax)

            # result becomes an index array fed to the RGB mapper
            if not numpy.issubdtype(newdata.dtype, numpy.dtype('uint')):
                newdata = newdata.astype(numpy.uint)
            idx = newdata

            self.logger.debug("shape of index is %s" % (str(idx.shape)))
            self._prergb = idx

        dst_order = self.viewer.get_rgb_order()
        image_order = self.image.get_order()
        get_order = dst_order
        if ('A' in dst_order) and not ('A' in image_order):
            get_order = dst_order.replace('A', '')

        if (whence <= 2.5) or (self._rgbarr == None) or (not self._optimize):
            # get RGB mapped array
            rgbobj = rgbmap.get_rgbarray(self._prergb, order=dst_order,
                                         image_order=image_order)
            self._rgbarr = rgbobj.get_array(get_order)

        # composite the image into the destination array at the
        # calculated position
        trcalc.overlay_image(dstarr, self._cvs_x, self._cvs_y, self._rgbarr,
                             dst_order=dst_order, src_order=get_order,
                             alpha=self.alpha, flipy=False)

    def apply_visuals(self, data, vmin, vmax):
        if self.autocuts != None:
            autocuts = self.autocuts
        else:
            autocuts = self.viewer.autocuts

        # Apply cut levels
        loval, hival = self.viewer.t_['cuts']
        newdata = autocuts.cut_levels(data, loval, hival,
                                      vmin=vmin, vmax=vmax)
        return newdata

    def set_image(self, image):
        self.image = image
        self._drawn = False
        self._cutout = None
        self._prergb = None
        self._rgbarr = None

class CompoundObject(CompoundMixin, CanvasObjectBase):
    """Compound object on a ImageViewCanvas.
    Parameters are:
    the child objects making up the compound object.  Objects are drawn
    in the order listed.
    Example:
      CompoundObject(Point(x, y, radius, ...),
      Circle(x, y, radius, ...))
    This makes a point inside a circle.
    """

    def __init__(self, *objects):
        CanvasObjectBase.__init__(self)
        CompoundMixin.__init__(self)
        self.kind = 'compound'
        self.objects = list(objects)

class Canvas(CanvasMixin, CompoundObject, CanvasObjectBase):
    def __init__(self, *objects):
        CanvasObjectBase.__init__(self)
        CompoundObject.__init__(self, *objects)
        CanvasMixin.__init__(self)
        self.kind = 'canvas'


# END
