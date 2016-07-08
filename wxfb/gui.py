# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"ABC Endview Tools", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.Size( 500,500 ), wx.DefaultSize )
		
		self.status_bar = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
		parent_sizer = wx.BoxSizer( wx.VERTICAL )
		
		self.option_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.option_panel.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INACTIVECAPTIONTEXT ) )
		self.option_panel.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ) )
		self.option_panel.SetMaxSize( wx.Size( -1,50 ) )
		
		option_sizer = wx.BoxSizer( wx.HORIZONTAL )
		
		self.change_button = wx.Button( self.option_panel, wx.ID_ANY, u"Change board", wx.DefaultPosition, wx.DefaultSize, 0 )
		option_sizer.Add( self.change_button, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.reset_button = wx.Button( self.option_panel, wx.ID_ANY, u"Reset board", wx.DefaultPosition, wx.DefaultSize, 0 )
		option_sizer.Add( self.reset_button, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.convert_toggle = wx.CheckBox( self.option_panel, wx.ID_ANY, u"Convert? ", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.convert_toggle.SetFont( wx.Font( 9, 74, 90, 90, False, "Segoe UI" ) )
		
		option_sizer.Add( self.convert_toggle, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.option_panel.SetSizer( option_sizer )
		self.option_panel.Layout()
		option_sizer.Fit( self.option_panel )
		parent_sizer.Add( self.option_panel, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.board_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.board_panel.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ) )
		self.board_panel.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ) )
		
		board_sizer = wx.BoxSizer( wx.VERTICAL )
		
		self.m_grid2 = wx.grid.Grid( self.board_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		# Grid
		self.m_grid2.CreateGrid( 5, 5 )
		self.m_grid2.EnableEditing( True )
		self.m_grid2.EnableGridLines( True )
		self.m_grid2.EnableDragGridSize( False )
		self.m_grid2.SetMargins( 0, 0 )
		
		# Columns
		self.m_grid2.EnableDragColMove( False )
		self.m_grid2.EnableDragColSize( True )
		self.m_grid2.SetColLabelSize( 30 )
		self.m_grid2.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		self.m_grid2.EnableDragRowSize( True )
		self.m_grid2.SetRowLabelSize( 80 )
		self.m_grid2.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.m_grid2.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		board_sizer.Add( self.m_grid2, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.board_panel.SetSizer( board_sizer )
		self.board_panel.Layout()
		board_sizer.Fit( self.board_panel )
		parent_sizer.Add( self.board_panel, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( parent_sizer )
		self.Layout()
		parent_sizer.Fit( self )
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

###########################################################################
## Class InputDialog
###########################################################################

class InputDialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Edit board configuration", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		input_box_sizer = wx.BoxSizer( wx.VERTICAL )
		
		input_grid_sizer = wx.GridSizer( 3, 2, 5, 5 )
		
		self.dim_text = wx.StaticText( self, wx.ID_ANY, u"Dimension (n x n)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.dim_text.Wrap( -1 )
		input_grid_sizer.Add( self.dim_text, 0, wx.ALL, 5 )
		
		self.dim_box = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		input_grid_sizer.Add( self.dim_box, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.choices_text = wx.StaticText( self, wx.ID_ANY, u"Choices", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.choices_text.Wrap( -1 )
		input_grid_sizer.Add( self.choices_text, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.choices_box = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		input_grid_sizer.Add( self.choices_box, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.diagonal_text = wx.StaticText( self, wx.ID_ANY, u"Experimental!", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.diagonal_text.Wrap( -1 )
		input_grid_sizer.Add( self.diagonal_text, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.diagonal_toggle = wx.CheckBox( self, wx.ID_ANY, u"Diagonal", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		input_grid_sizer.Add( self.diagonal_toggle, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		input_box_sizer.Add( input_grid_sizer, 1, wx.EXPAND, 5 )
		
		self.ok_button = wx.Button( self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.ok_button.SetDefault() 
		input_box_sizer.Add( self.ok_button, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( input_box_sizer )
		self.Layout()
		input_box_sizer.Fit( self )
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass