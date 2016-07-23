#!/usr/bin/env python2
import wx
import wx.xrc
import wx.grid
from utils import *

WINDOW_SIZE = 300
process_running = 0

def reference_counting(func):
	''' Counting how many functions are being ran, to prevent data input. '''
	def wrapper(*args, **kwargs):
		global process_running
		process_running += 1
		func(*args, **kwargs)
		process_running -= 1
	return wrapper

class MainFrame ( wx.Frame ):
	
	@reference_counting
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = "ABC Endview Tools", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.Size( WINDOW_SIZE+40,WINDOW_SIZE + 150 ), wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ) )
		
		self.status_bar = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
		parent_sizer = wx.BoxSizer( wx.VERTICAL )

		self.option_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.option_panel.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ) )
		self.option_panel.SetMaxSize( wx.Size( -1,50 ) )
		
		option_sizer = wx.BoxSizer( wx.HORIZONTAL )
		self.change_button = wx.Button( self.option_panel, wx.ID_ANY, "Change board", wx.DefaultPosition, wx.DefaultSize, 0 )
		option_sizer.Add( self.change_button, 0, wx.ALL|wx.EXPAND, 5 )
		self.reset_button = wx.Button( self.option_panel, wx.ID_ANY, "Reset board", wx.DefaultPosition, wx.DefaultSize, 0 )
		option_sizer.Add( self.reset_button, 0, wx.ALL|wx.EXPAND, 5 )
		self.convert_toggle = wx.CheckBox( self.option_panel, wx.ID_ANY, "Convert? ", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		option_sizer.Add( self.convert_toggle, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.option_panel.SetSizer( option_sizer )
		self.option_panel.Layout()
		option_sizer.Fit( self.option_panel )
		parent_sizer.Add( self.option_panel, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.board_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.board_panel.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ) )
		self.board_panel.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ) )
		
		self.board_sizer = wx.BoxSizer( wx.VERTICAL )
		self.board_table = wx.grid.Grid( self.board_panel, wx.ID_ANY, wx.DefaultPosition, (WINDOW_SIZE, 0), 0 )
		# Grid
		self.board_table.CreateGrid(1, 1)
		# THIS IS WHERE THE BOARD CODE WENT
		self.board_table.EnableEditing( True )
		self.board_table.EnableGridLines( True )
		self.board_table.SetGridLineColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ) )
		self.board_table.EnableDragGridSize( False )
		self.board_table.SetMargins( 0, 0 )
		
		# Columns
		self.board_table.EnableDragColMove( False )
		self.board_table.EnableDragColSize( False )
		self.board_table.HideColLabels()
		
		# Rows
		self.board_table.EnableDragRowSize( False )
		self.board_table.HideRowLabels()

		# Cell Defaults
		self.board_table.SetDefaultCellBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ) )
		self.board_table.SetDefaultCellAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )

		self.board_sizer.Add( self.board_table, 1, wx.ALL|wx.EXPAND, 5 )
		self.board_panel.SetSizer( self.board_sizer )
		self.board_panel.Layout()
		self.board_sizer.Fit( self.board_panel )
		parent_sizer.Add( self.board_panel, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.SetSizer( parent_sizer )
		self.Layout()
		parent_sizer.Fit( self )
		self.Centre( wx.BOTH )

		# Connect Events
		self.change_button.Bind( wx.EVT_BUTTON, self.onChange )
		self.reset_button.Bind( wx.EVT_BUTTON, self.onReset )
		self.convert_toggle.Bind( wx.EVT_CHECKBOX, self.onConvert )
		self.board_table.Bind( wx.grid.EVT_GRID_CELL_CHANGING, self.onEditBoard )

		# Cell styles
		self.cell_font_normal = self.board_table.GetCellFont(0,0)
		self.cell_font_bold = self.cell_font_normal.Bold()

		self.cell_corner = wx.grid.GridCellAttr()
		self.cell_corner.SetReadOnly()
		self.cell_corner.SetBackgroundColour(wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ))
		self.cell_constraint = wx.grid.GridCellAttr()
		self.cell_constraint.SetBackgroundColour(wx.Colour(150,150,150))
		self.cell_constraint.SetFont(self.cell_font_bold)
		self.cell_constraint.SetTextColour('WHITE')
		self.cell_normal = self.cell_constraint.Clone()
		self.cell_normal.SetTextColour('BLACK')
		self.cell_normal.SetBackgroundColour(wx.Colour(223,223,223,255))
		self.cell_prefill = self.cell_normal.Clone()
		self.cell_prefill.SetTextColour('DARK TURQUOISE')

		self.cell_normal.SetFont(self.cell_font_normal)

		# board, constraint, choices, diag
		self.board = None
		self.solution_board = None
		self.constraint = None
		self.choices = None
		self.diag = None
		self.dim = -1
		self.functions_used = None
		self.swap_order = None
		self.no_of_slns = None

		if self.board is None:
			self.onChange(wx.EVT_BUTTON)
	
		self.Show(True)

	def __del__( self ):
		pass
	
	# change content of board
	@reference_counting
	def view_board(self):
		self.status_bar.SetStatusText("Drawing the board...")
		dim = get_dim(self.board)
		
		if self.dim > -1:
			self.board_table.DeleteRows(1, self.dim + 1)
			self.board_table.DeleteCols(1, self.dim + 1)
		self.board_table.InsertRows(1, dim + 1)
		self.board_table.InsertCols(1, dim + 1)
		self.dim = dim
		div = min(int(WINDOW_SIZE / (dim + 2)), 100)
		for i in range(dim+2):
			self.board_table.SetColSize( i, div )
			self.board_table.SetRowSize( i, div )

		# formatting
		self.board_table.SetColAttr(0, self.cell_constraint.Clone())
		self.board_table.SetColAttr(dim+1, self.cell_constraint.Clone())
		self.board_table.SetRowAttr(0, self.cell_constraint.Clone())
		self.board_table.SetRowAttr(dim+1, self.cell_constraint.Clone())
		for i in range(dim):
			for j in range(dim):
				self.board_table.SetAttr(i+1, j+1, self.cell_normal.Clone())
		self.board_table.SetAttr(0, 0, self.cell_corner.Clone())
		self.board_table.SetAttr(0, dim + 1, self.cell_corner.Clone())
		self.board_table.SetAttr(dim + 1, 0, self.cell_corner.Clone())
		self.board_table.SetAttr(dim + 1, dim + 1, self.cell_corner.Clone())

		if self.board is not None:
			self.solution_board = deepcopy(self.board)
			populate_empty_board(self.solution_board, self.choices)
			for i in range(dim):
				for j in range(dim):
					if self.board[i][j] != '':
						self.solution_board[i][j] = self.board[i][j]
			self.no_of_slns = solve(self.solution_board, self.constraint, self.choices, self.diag, True)
			if self.no_of_slns == 1:
				solutions_list, throwaway = solve(self.solution_board, self.constraint, self.choices, self.diag)
				self.solution_board = solutions_list[0]
			elif self.no_of_slns > 1:
				self.solution_board = solve(self.solution_board, self.constraint, self.choices, no_trials = True)

		# showing on the screen
		for i in range(dim):
			# top
			self.board_table.SetCellValue(0, i+1, self.constraint[0][i])
			# bottom
			self.board_table.SetCellValue(dim+1, i+1, self.constraint[1][i])
			# left
			self.board_table.SetCellValue(i+1, 0, self.constraint[2][i])
			# right
			self.board_table.SetCellValue(i+1, dim+1, self.constraint[3][i])
		for i in range(dim):
			for j in range(dim):
				if self.no_of_slns == 0:
					self.board_table.SetCellValue(i+1, j+1, self.board[i][j])
				else:
					if len(self.solution_board[i][j]) == 1:
						char = self.solution_board[i][j]
						if char == 'X':
							char = '-'
						self.board_table.SetCellValue(i+1, j+1, char)
				if self.board[i][j] != '':
					self.board_table.SetAttr(i + 1, j + 1, self.cell_prefill.Clone())

		status_text = 'Grid: ' + str(dim) + ' x ' + str(dim)
		choices = self.choices
		if choices[-1] == 'X':
			choices = choices[:-1]
		status_text += ' | Choices: '
		status_text += choices
		status_text += ' | '
		if self.no_of_slns == 0:
			status_text += 'No solutions'
		elif self.no_of_slns == 1:
			status_text += '1 solution'
		elif self.no_of_slns == 2:
			status_text += '>1 solutions'
		else:
			print "ERROR!"
			print self.no_of_slns
		self.status_bar.SetStatusText(status_text)
		print stringify(self.board, self.constraint, True)

	# when the board is edited
	def onEditBoard(self, event):
		if process_running > 0:
			event.Veto()
			return

		if self.convert_toggle.GetValue():
			event.Veto()
			return
		dim = get_dim(self.board)
		new_val = event.GetString().upper()
		if len(new_val) <= 1 and new_val in self.choices:
			x = event.GetRow()
			y = event.GetCol()
			if x == 0:
				if new_val != 'X':
					self.constraint[0][y-1] = new_val
				else:
					event.Veto()
			elif x == dim + 1:
				if new_val != 'X':
					self.constraint[1][y-1] = new_val
				else:
					event.Veto()
			elif y == 0:
				if new_val != 'X':
					self.constraint[2][x-1] = new_val
				else:
					event.Veto()
			elif y == dim + 1:
				if new_val != 'X':
					self.constraint[3][x-1] = new_val
				else:
					event.Veto()
			else:
				self.board[x-1][y-1] = new_val
		else:
			event.Veto()
		self.view_board()

	# when change button is clicked
	@reference_counting
	def onChange(self, event):
		self.change_dialog = InputDialog(self)
		self.change_dialog.ShowModal()

	# when reset button is clicked
	@reference_counting
	def onReset(self, event):
		self.change_dialog.onOK(wx.EVT_BUTTON)
		self.convert_toggle.SetValue(False)

	# when convert toggle is clicked
	@reference_counting
	def onConvert(self, event):
		convert = self.convert_toggle.GetValue()
		if convert:
			self.functions_used, self.swap_order = convert_to_family_generator(self.board, self.constraint, self.choices, [])
		else:
			execute_changes(self.board, self.constraint, self.functions_used, self.swap_order, True)
		if self.solution_board is not None:
			execute_changes(self.solution_board, generate_empty_constraint(get_dim(self.board)), self.functions_used, self.swap_order, not convert)
		self.view_board()

class InputDialog ( wx.Dialog ):
	
	@reference_counting
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = "Edit board configuration", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP )
		
		self.parent = parent

		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		input_box_sizer = wx.BoxSizer( wx.VERTICAL )
		
		input_grid_sizer = wx.GridSizer( 3, 2, 5, 5 )
		
		self.dim_text = wx.StaticText( self, wx.ID_ANY, "Dimension (n x n)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.dim_text.Wrap( -1 )
		input_grid_sizer.Add( self.dim_text, 0, wx.ALL, 5 )
		
		self.dim_box = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		input_grid_sizer.Add( self.dim_box, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.choices_text = wx.StaticText( self, wx.ID_ANY, "Choices", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.choices_text.Wrap( -1 )
		input_grid_sizer.Add( self.choices_text, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.choices_box = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		input_grid_sizer.Add( self.choices_box, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.diagonal_text = wx.StaticText( self, wx.ID_ANY, "Experimental!", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.diagonal_text.Wrap( -1 )
		input_grid_sizer.Add( self.diagonal_text, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.diagonal_toggle = wx.CheckBox( self, wx.ID_ANY, "Diagonal", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		input_grid_sizer.Add( self.diagonal_toggle, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		input_box_sizer.Add( input_grid_sizer, 1, wx.EXPAND, 5 )
		
		self.ok_button = wx.Button( self, wx.ID_ANY, "OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.ok_button.SetDefault() 
		input_box_sizer.Add( self.ok_button, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( input_box_sizer )
		self.Layout()
		input_box_sizer.Fit( self )

		# Connect Events
		self.ok_button.Bind( wx.EVT_BUTTON, self.onOK )		

		if self.parent.board is not None:
			self.dim_box.SetValue(str(get_dim(self.parent.board)))
			choices = self.parent.choices
			if choices[-1] == 'X':
				choices = choices[:-1]
			self.choices_box.SetValue(choices)
			self.diagonal_toggle.SetValue(self.parent.diag)

		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass

	@reference_counting
	def onOK(self, event):
		try:
			self.Close()
			self.dim = int(self.dim_box.GetValue())
			self.choices = self.choices_box.GetValue().upper().encode('ascii','ignore')
			if not_cap_chars(self.choices):
				raise ValueError('not valid choices')
			if self.dim > len(self.choices):
				self.choices += 'X'
			if self.dim < len(self.choices):
				raise ValueError('more choices than cells')
			self.diag = self.diagonal_toggle.GetValue()
			self.board = generate_empty_board(self.dim)
			self.constraint = generate_empty_constraint(self.dim)
			self.parent.board = self.board
			self.parent.constraint = self.constraint
			self.parent.choices = self.choices
			self.parent.diag = self.diag
			self.parent.solution_board = None
			self.parent.functions_used = None
			self.parent.swap_order = None
			self.parent.no_of_slns = None
			self.parent.view_board()
		except ValueError, e:
			self.parent.status_bar.SetStatusText('Error! ' + str(e) + '.')
			raise e
	
if __name__ == '__main__':
	app = wx.App(False)
	frame = MainFrame(None)
	app.MainLoop()
