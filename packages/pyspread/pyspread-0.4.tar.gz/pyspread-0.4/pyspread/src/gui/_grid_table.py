#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Martin Manns
# Distributed under the terms of the GNU General Public License

# --------------------------------------------------------------------
# pyspread is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyspread is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyspread.  If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------


"""
_grid_table
===========

Provides
--------

1) GridTable: Handles interaction to data_array

"""

import wx
import wx.grid

from src.config import config


class GridTable(wx.grid.PyGridTableBase):
    """Table base class that handles interaction between Grid and data_array"""

    def __init__(self, grid, data_array):
        self.grid = grid
        self.data_array = data_array

        wx.grid.PyGridTableBase.__init__(self)

        # we need to store the row length and column length to
        # see if the table has changed size
        self._rows = self.GetNumberRows()
        self._cols = self.GetNumberCols()

    def GetNumberRows(self):
        """Return the number of rows in the grid"""

        return self.data_array.shape[0]

    def GetNumberCols(self):
        """Return the number of columns in the grid"""

        return self.data_array.shape[1]

    def GetRowLabelValue(self, row):
        """Returns row number"""

        return str(row)

    def GetColLabelValue(self, col):
        """Returns column number"""

        return str(col)

    def GetSource(self, row, col, table=None):
        """Return the source string of a cell"""

        if table is None:
            table = self.grid.current_table

        value = self.data_array((row, col, table))

        if value is None:
            return u""
        else:
            return value

    def GetValue(self, row, col, table=None):
        """Return the result value of a cell, line split if too much data"""

        if table is None:
            table = self.grid.current_table

        try:
            cell_code = self.data_array((row, col, table))
        except IndexError:
            cell_code = None

        # Put EOLs into result if it is too long
        maxlength = int(config["max_textctrl_length"])

        if cell_code is not None and len(cell_code) > maxlength:
            chunk = 80
            cell_code = "\n".join(cell_code[i:i + chunk]
                                  for i in xrange(0, len(cell_code), chunk))

        return cell_code

    def SetValue(self, row, col, value, refresh=True):
        """Set the value of a cell, merge line breaks"""

        # Join code that has been split because of long line issue
        value = "".join(value.split("\n"))

        key = row, col, self.grid.current_table
        self.grid.actions.set_code(key, value)

    def UpdateValues(self):
        """Update all displayed values"""

        # This sends an event to the grid table
        # to update all of the values

        msg = wx.grid.GridTableMessage(self,
                wx.grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES)
        self.grid.ProcessTableMessage(msg)

    def ResetView(self):
        """
        (Grid) -> Reset the grid view.   Call this to
        update the grid if rows and columns have been added or deleted

        """

        grid = self.grid

        grid.BeginBatch()

        for current, new, delmsg, addmsg in [
            (self._rows, self.GetNumberRows(),
             wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED,
             wx.grid.GRIDTABLE_NOTIFY_ROWS_APPENDED),
            (self._cols, self.GetNumberCols(),
             wx.grid.GRIDTABLE_NOTIFY_COLS_DELETED,
             wx.grid.GRIDTABLE_NOTIFY_COLS_APPENDED),
        ]:

            if new < current:
                msg = wx.grid.GridTableMessage(self, delmsg, new,
                                               current - new)
                grid.ProcessTableMessage(msg)
            elif new > current:
                msg = wx.grid.GridTableMessage(self, addmsg, new - current)
                grid.ProcessTableMessage(msg)
                self.UpdateValues()

        grid.EndBatch()

        self._rows = self.GetNumberRows()
        self._cols = self.GetNumberCols()

        # Reset cell sizes to standard cell size

        grid.SetDefaultRowSize(grid.GetDefaultRowSize(),
                               resizeExistingRows=True)
        grid.SetDefaultColSize(grid.GetDefaultColSize(),
                               resizeExistingCols=True)

        # Adjust rows
        row_heights = grid.code_array.row_heights
        for key in row_heights:
            if key[1] == grid.current_table and \
               key[0] < self.data_array.shape[0]:
                row = key[0]
                if row_heights[key] is None:
                    # Default row size
                    grid.SetRowSize(row, grid.GetDefaultRowSize())
                else:
                    grid.SetRowSize(row, row_heights[key])

        # Adjust columns
        col_widths = grid.code_array.col_widths
        for key in col_widths:
            if key[1] == grid.current_table and \
               key[0] < self.data_array.shape[1]:
                col = key[0]
                if col_widths[key] is None:
                    # Default row size
                    grid.SetColSize(col, grid.GetDefaultColSize())
                else:
                    grid.SetColSize(col, col_widths[key])

        # update the scrollbars and the displayed part
        # of the grid

        grid.Freeze()
        grid.AdjustScrollbars()
        grid.Refresh()
        grid.Thaw()

# end of class MainGridTable