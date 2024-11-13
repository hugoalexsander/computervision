import configparser
import frameedge as fe
import frameedgefilter as fef

class Controller:
    def __init__(self, cap):
        self.fmed = fe.FrameEdge(cap)
        self.fmedf = fef.FrameEdgeFilter(cap)
        self.target = self.fmed
        self.rendering = "frame"
        self.filtering = "no"
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

    def render(self):
        if self.filtering == "no": self.target = self.fmed
        else: self.target = self.fmedf
        if self.rendering == "frame": self.target.render_frame()
        elif self.rendering == "edge": self.target.render_edge()
        elif self.rendering == "contour": self.target.render_contour()
        elif self.rendering == "square": self.target.render_square()
        elif self.rendering == "face": self.target.render_face()

    def config_update(self):
        self.config.read('config.ini')
        self.rendering = self.config["settings"]["rendering"]
        self.filtering = self.config["settings"]["filtering"]
        lower = int(self.config["settings"]["thresholdlower"])
        upper = int(self.config["settings"]["thresholdupper"])
        self.fmed.set_threshold(lower, upper)
        self.fmedf.set_threshold(lower, upper)
        lower = int(self.config["settings"]["arealower"])
        upper = int(self.config["settings"]["areaupper"])
        self.fmed.set_area(lower, upper)
        self.fmedf.set_area(lower, upper)
