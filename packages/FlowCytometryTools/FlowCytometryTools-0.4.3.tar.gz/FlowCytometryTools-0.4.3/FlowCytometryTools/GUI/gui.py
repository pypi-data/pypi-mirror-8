#!/usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import matplotlib
matplotlib.use('wxagg')
from wireframe import GeneratedWireframe
import fc_widget

class GUIEmbedded(GeneratedWireframe):
    def __init__(self, *args, **kwargs):
        GeneratedWireframe.__init__(self, *args, **kwargs)
        self.fig = self.canvas.figure
        self.ax = self.fig.add_subplot(111)
        self.fc_toolbar = fc_widget.FCToolBar(self.ax)
        self._update_axes()

    def load_measurement(self, measurement):
        self.fc_toolbar.load_measurement(measurement)
        self._update_axes()

    def load_fcs(self, filepath=None):
        self.fc_toolbar.load_fcs(filepath=filepath, parent=self)
        self._update_axes()

    def btnLoadFCS(self, event):
        self.load_fcs()

    def btnQuitApp(self, event):
        self.fc_toolbar.close()
        self.Close(1)

    def _change_channel(self, event, axis):
        """
        Parameters
        -------------
        axis : 'x' or 'y'
        event : pick of list text
        """
        if event.GetExtraLong(): # Quick hack
            sel = event.GetString().encode("UTF-8")
            current_channels = self.fc_toolbar.current_channels

            if len(current_channels) == 1:
                ch = current_channels[0] # Current channel
            else:
                if axis == 'x':
                    ch = current_channels[1]
                elif axis == 'y':
                    ch = current_channels[0]

            if sel == ch:
                new_channels = ch,
            elif axis == 'x':
                new_channels = sel, ch
            else:
                new_channels = ch, sel

            self.fc_toolbar.set_axis(new_channels, self.ax)

    def btn_choose_x_channel(self, event):
        self._change_channel(event, 'x')

    def btn_choose_y_channel(self, event):
        self._change_channel(event, 'y')

    def btn_create_poly_gate(self, event):
        self.fc_toolbar.create_gate_widget('poly')

    def btn_create_quad_gate(self, event):
        self.fc_toolbar.create_gate_widget('quad')

    def btn_create_horizontal_threshold_gate(self, event):
        self.fc_toolbar.create_gate_widget('horizontal threshold')

    def btn_create_vertical_threshold_gate(self, event):
        self.fc_toolbar.create_gate_widget('vertical threshold')

    def btn_delete_gate(self, event):
        self.fc_toolbar.remove_active_gate()

    def btn_gen_code(self, event):
        generated_code = self.fc_toolbar.get_generation_code()
        self.tb_gen_code.SetValue(generated_code)

    def _update_axes(self):
        if self.fc_toolbar.sample is not None:
            options = list(self.fc_toolbar.sample.channel_names)
        else:
            options = list(['d1', 'd2', 'd3']) # Just a seed
        self.x_axis_list.Clear()
        self.x_axis_list.InsertItems(options, 0)
        self.y_axis_list.Clear()
        self.y_axis_list.InsertItems(options, 0)
        self.fc_toolbar.current_channels = options[0], options[1]

class FCGUI(object):
    """ Use this to launch the wx-based fdlow cytometry app """
    def __init__(self, filepath=None, measurement=None):
        if filepath is not None and measurement is not None:
            raise ValueError('You can only specify either filepath or measurement, but not both.')

        self.app = wx.PySimpleApp(0)
        wx.InitAllImageHandlers()
        self.main = GUIEmbedded(None, -1, "")
        self.app.SetTopWindow(self.main)
        if filepath is not None:
            self.main.load_fcs(filepath)
        if measurement is not None:
            self.main.load_measurement(measurement)
        self.run()

    def run(self):
        self.main.Show()
        self.app.MainLoop()

if __name__ == "__main__":
    app = FCGUI('../tests/data/FlowCytometers/FACSCaliburHTS/Sample_Well_A02.fcs')
