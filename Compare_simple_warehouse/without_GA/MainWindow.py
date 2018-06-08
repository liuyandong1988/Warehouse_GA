#!/usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import WorldController
import random
from param import *
import wx.gizmos as gizmos
import Graph
import math
import time

class PaintWindow(wx.Window):

    def __init__(self, parent, myId):

        # setup window
        wx.Window.__init__(self, parent, myId)
        self.PhotoMaxSize = 1750
        # setup painter
        self.SetBackgroundColour("Black")  # window background color
        self.pen = wx.Pen("??")  # instance pen property
        self.brush = wx.Brush("??")  # fill the color block property
        # setup timer
        self.controller = WorldController.Controller()
        self.timer = wx.Timer(self)  # make the timer
        # bind the processing event self.update
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.timer.Start(REFRESH_INTERVAL)  # refresh the window

    def updateBuffer(self):
        size = self.GetClientSize()  # get the size of the client window
        # make the buffer context
        self.buffer = wx.EmptyBitmap(size.width , size.height)
        self.dc = wx.BufferedDC(None, self.buffer)
        # use the buffer context
        self.dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        self.dc.Clear()

        self.drawGround()
        self.drawchargePoints()
        self.drawendPoints()
        self.drawShelves()
        self.drawAgents()
        self.drawboxes()
        #self.buffer = self.multiScale()  # scale the image
        self.dc = wx.BufferedPaintDC(self, self.buffer)  # draw the buffer data

    def multiScale(self):
        img = self.buffer.ConvertToImage()

        # scale the image, preserving the aspect ratio
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW = self.PhotoMaxSize
            NewH = self.PhotoMaxSize * H / W
        else:
            NewH = self.PhotoMaxSize
            NewW = self.PhotoMaxSize * W / H
        img = img.Scale(NewW, NewH)
        return img.ConvertToBitmap()

    def drawGround(self):
        # draw the warehouse
        self.pen.SetWidth(2)
        self.pen.Colour = "White"
        self.dc.SetPen(self.pen)
        self.dc.DrawLine(
            margin_left, margin_top, margin_left, world_height - margin_bottom)

        for i in range(7):
            self.dc.DrawLine(
                margin_left + (3 * i + 1) * L,
                margin_top, margin_left + (3 * i + 3) * L, margin_top)

        self.dc.DrawLine(world_width - margin_right, margin_top,
                         world_width - margin_right,
                         world_height - margin_bottom)

        for i in range(2):
            self.dc.DrawLine(
                margin_left +  (12 * i + 1) *L, world_height - margin_bottom,
                margin_left + (12 * i + 9)  * L, world_height - margin_bottom)

        self.dc.DrawLine(
            margin_left +  10 *L, world_height - margin_bottom,
            margin_left + 12 * L, world_height - margin_bottom)


    def drawShelves(self):
        for g in self.controller.shelves:
            self.drawEachShelf(g)

    def drawEachShelf(self, shelf):
        self.pen.Colour = "white"
        self.pen.SetWidth(2)
        self.dc.SetPen(self.pen)
        self.dc.SetBrush(wx.Brush(shelf.shelf_color, wx.SOLID))
        self.dc.DrawRectangle(shelf.x, shelf.y, L, L)

    def drawAgents(self):
        for i in self.controller.agents:
            self.drawAgent(i)

    def drawAgent(self, agent):
        self.brush.SetStyle(wx.SOLID)
        if agent.color == 0:  # idle
            self.brush.SetColour("Green")
        elif agent.color == 1:  # moving to good
            self.brush.SetColour("Blue")
        elif agent.color == 2:  # carrying good
            self.brush.SetColour("Red")
        elif agent.color == 3:  # dead
            self.brush.SetColour("Black")
        elif agent.color == 4:  # charging
            self.brush.SetColour("Orange")
        elif agent.color == 5:  # supplement
            self.brush.SetColour("Pink")
        self.pen.Colour = "Yellow"
        self.pen.SetWidth(1)
        self.dc.SetPen(self.pen)
        self.dc.SetBrush(self.brush)
        self.dc.DrawCircle(agent.x, agent.y, agent.r)
        self.dc.DrawLine(agent.x, agent.y,
                         agent.x + agent.r * agent.angle.cos(),
                         agent.y - agent.r * agent.angle.sin())



        # draw battery
        if agent.battery_status == 1:
            self.brush.SetColour("Green")
            self.pen.Colour = "Green"

        elif agent.battery_status == 2:
            self.brush.SetColour("Orange")
            self.pen.Colour = "Orange"

        elif agent.battery_status == 3:
            self.brush.SetColour("red")
            self.pen.Colour = "red"

        self.pen.SetWidth(1)
        self.dc.SetPen(self.pen)
        self.brush.SetStyle(wx.SOLID)
        self.dc.SetBrush(self.brush)

        if agent.angle.theta == 90 or agent.angle.theta == -90:
            self.dc.DrawRectangle(
                agent.x + 2 * agent.r * agent.battery_angle2.cos(),
                agent.y - 3 * agent.r * agent.battery_angle2.sin(),
                agent.battery_pos,  agent.width)
        elif agent.angle.theta == 0 or agent.angle.theta == 180:
            self.dc.DrawRectangle(
                agent.x + 3 * agent.r * agent.battery_angle2.cos(),
                agent.y - 2 * agent.r * agent.battery_angle2.sin(),
                agent.width, agent.battery_pos)

        # add battery bar
        self.pen.Colour = "White"
        self.pen.SetWidth(2)
        self.dc.SetPen(self.pen)
        if agent.angle.theta == 90 or agent.angle.theta == -90:
            self.dc.DrawLine(
                agent.x + 2 * agent.r * agent.battery_angle1.cos(),
                agent.y - 3 * agent.r * agent.battery_angle1.sin(),
                agent.x + 2 * agent.r * agent.battery_angle2.cos(),
                agent.y - 3 * agent.r * agent.battery_angle2.sin())

            self.dc.DrawLine(
                agent.x + 2 * agent.r * agent.battery_angle1.cos(),
                agent.y - 2 * agent.r * agent.battery_angle1.sin(),
                agent.x + 2 * agent.r * agent.battery_angle2.cos(),
                agent.y - 2 * agent.r * agent.battery_angle2.sin())

            self.dc.DrawLine(
                agent.x + 2 * agent.r * agent.battery_angle1.cos(),
                agent.y - 3 * agent.r * agent.battery_angle1.sin(),
                agent.x + 2 * agent.r * agent.battery_angle1.cos(),
                agent.y - 2 * agent.r * agent.battery_angle1.sin())

            self.dc.DrawLine(
                agent.x + 2 * agent.r * agent.battery_angle2.cos(),
                agent.y - 3 * agent.r * agent.battery_angle2.sin(),
                agent.x + 2 * agent.r * agent.battery_angle2.cos(),
                agent.y - 2 * agent.r * agent.battery_angle2.sin())
        elif agent.angle.theta == 0 or agent.angle.theta == 180:
            self.dc.DrawLine(
                agent.x + 3 * agent.r * agent.battery_angle1.cos(),
                agent.y - 2 * agent.r * agent.battery_angle1.sin(),
                agent.x + 3 * agent.r * agent.battery_angle2.cos(),
                agent.y - 2 * agent.r * agent.battery_angle2.sin())

            self.dc.DrawLine(
                agent.x + 2 * agent.r * agent.battery_angle1.cos(),
                agent.y - 2 * agent.r * agent.battery_angle1.sin(),
                agent.x + 2 * agent.r * agent.battery_angle2.cos(),
                agent.y - 2 * agent.r * agent.battery_angle2.sin())

            self.dc.DrawLine(
                agent.x + 3 * agent.r * agent.battery_angle1.cos(),
                agent.y - 2 * agent.r * agent.battery_angle1.sin(),
                agent.x + 2 * agent.r * agent.battery_angle1.cos(),
                agent.y - 2 * agent.r * agent.battery_angle1.sin())

            self.dc.DrawLine(
                agent.x + 3 * agent.r * agent.battery_angle2.cos(),
                agent.y - 2 * agent.r * agent.battery_angle2.sin(),
                agent.x + 2 * agent.r * agent.battery_angle2.cos(),
                agent.y - 2 * agent.r * agent.battery_angle2.sin())

    def drawchargePoints(self):
        for i in self.controller.chargePoints:
            self.drawchargePoint(i)

    def drawchargePoint(self, chargepoint):
        self.pen.Colour = "Green"
        self.pen.SetWidth(1)
        self.dc.SetPen(self.pen)

        self.brush.SetStyle(wx.SOLID)
        self.brush.SetColour("Black")
        self.dc.SetBrush(self.brush)
        self.dc.DrawCircle(
            chargepoint.x, chargepoint.y, chargepoint.r)

        x1 = chargepoint.x + chargepoint.r * math.cos(45 * math.pi / 180.0)
        y1 = chargepoint.y + chargepoint.r * math.sin(45 * math.pi / 180.0)
        x2 = chargepoint.x - chargepoint.r * math.cos(45 * math.pi / 180.0)
        y2 = chargepoint.y - chargepoint.r * math.sin(45 * math.pi / 180.0)
        x3 = chargepoint.x - chargepoint.r * math.cos(45 * math.pi / 180.0)
        y3 = chargepoint.y + chargepoint.r * math.sin(45 * math.pi / 180.0)
        x4 = chargepoint.x + chargepoint.r * math.cos(45 * math.pi / 180.0)
        y4 = chargepoint.y - chargepoint.r * math.sin(45 * math.pi / 180.0)
        self.dc.DrawLine(x1, y1, x3, y3)
        self.dc.DrawLine(x1, y1, x4, y4)
        self.dc.DrawLine(x2, y2, x3, y3)
        self.dc.DrawLine(x2, y2, x4, y4)

    def drawendPoints(self):
        for i in self.controller.orderPoints:
            self.drawendPoint(i)

    def drawendPoint(self, endpoint):
        self.pen.Colour = "red"
        self.pen.SetWidth(1)
        self.dc.SetPen(self.pen)

        self.brush.SetStyle(wx.SOLID)
        self.brush.SetColour("Black")
        self.dc.SetBrush(self.brush)
        self.dc.DrawCircle(
            endpoint.x, endpoint.y, endpoint.r)

        x1 = endpoint.x + endpoint.r * math.cos(45 * math.pi / 180.0)
        y1 = endpoint.y + endpoint.r * math.sin(45 * math.pi / 180.0)
        x2 = endpoint.x - endpoint.r * math.cos(45 * math.pi / 180.0)
        y2 = endpoint.y - endpoint.r * math.sin(45 * math.pi / 180.0)
        x3 = endpoint.x - endpoint.r * math.cos(45 * math.pi / 180.0)
        y3 = endpoint.y + endpoint.r * math.sin(45 * math.pi / 180.0)
        x4 = endpoint.x + endpoint.r * math.cos(45 * math.pi / 180.0)
        y4 = endpoint.y - endpoint.r * math.sin(45 * math.pi / 180.0)

        self.dc.DrawLine(x1, y1, x2, y2)
        self.dc.DrawLine(x3, y3, x4, y4)
        
    def drawboxes(self):
        for i in self.controller.orderBoxes:
            self.drawbox(i)
    
    def drawbox(self, box):
        # draw boxes (goods)
        self.pen.Colour = "black"
        self.pen.SetWidth(1)
        self.dc.SetPen(self.pen)
        self.brush.SetStyle(wx.SOLID)
        for i in xrange(15):
            if (i + 1) <= box.boxes_num:
                self.brush.SetColour(box.box_color[i])
            else:
                self.brush.SetColour("Black")
            self.dc.SetBrush(self.brush)
            self.dc.DrawRectangle(
                box.box_x + i * int(20), box.box_y, int(20), int(20))

    def update(self, event):
        #         self.onTimer()
        self.updateBuffer()
        self.controller.update()  


class PaintFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(
            self, parent, -1, "Quad", size=(world_width + 100 , world_height + 100))
        self.paint = PaintWindow(self, -1)


if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = PaintFrame(None)
    frame.SetPosition((0, 0))
    frame.Show(True)
    app.MainLoop()
