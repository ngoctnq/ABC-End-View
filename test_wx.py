#!/usr/bin/env python2
from wx import *

class MainWindow(wx.Frame):
	''' New class of Frame. '''
	# default setup
	dim = None
	choices = None
	diag = None
	board = None
	constraint = None
	sorted_board = None
	sorted_constraint = None

	def __init__(self, parent, title):
		# may add size
		wx.Frame.__init__(self, parent, title = title)
		self.statusbar = self.CreateStatusBar()
		self.statusbar.SetStatusText('Input problem.')
		
		self.toolbar = \
			self.CreateToolBar(style = (wx.TB_TEXT | wx.TB_NOICONS))
		dgn = self.toolbar.AddCheckTool(3, 'Diagonal', None)

app = wx.App(False)
frame = MainWindow(None, 'ABC Endview Puzzle Tools')
app.MainLoop()