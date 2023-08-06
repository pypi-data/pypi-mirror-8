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
_grid_renderer
==============

Provides
--------

1) GridRenderer: Draws the grid
2) Background: Background drawing

"""

import wx.grid

from src.sysvars import get_color
from src.config import config
import src.lib.i18n as i18n
from src.lib._grid_cairo_renderer import GridCellCairoRenderer
import cairo

# Use ugettext instead of getttext to avoid unicode errors
_ = i18n.language.ugettext


class GridRenderer(wx.grid.PyGridCellRenderer):
    """This renderer draws borders and text at specified font, size, color"""

    selection_color_tuple = \
        tuple([c / 255.0 for c in get_color(config["selection_color"]).Get()]
              + [0.5])

    def __init__(self, data_array):

        wx.grid.PyGridCellRenderer.__init__(self)

        self.data_array = data_array

        # Cache for cell content
        self.cell_cache = {}

        # Zoom of grid
        self.zoom = 1.0

        # Old cursor position
        self.old_cursor_row_col = 0, 0

    def get_zoomed_size(self, size):
        """Returns zoomed size as Integer

        Parameters
        ----------

        font_size: Integer
        \tOriginal font size

        """

        return max(1.0, round(size * self.zoom))

    def _draw_cursor(self, dc, grid, row, col,
                     pen=wx.BLACK_PEN, brush=wx.BLACK_BRUSH):
        """Draws cursor as Rectangle in lower right corner"""

        key = row, col, grid.current_table
        rect = grid.CellToRect(row, col)
        rect = self.get_merged_rect(grid, key, rect)

        # Check if cell is invisible
        if rect is None:
            return

        size = self.get_zoomed_size(1.0)

        caret_length = int(min([rect.width, rect.height]) / 5.0)

        pen.SetWidth(size)

        # Inner right and lower borders
        border_left = rect.x
        border_right = rect.x + rect.width - size - 1
        border_upper = rect.y
        border_lower = rect.y + rect.height - size - 1

        points_lr = [
            (border_right, border_lower - caret_length),
            (border_right, border_lower),
            (border_right - caret_length, border_lower),
            (border_right, border_lower),
        ]

        points_ur = [
            (border_right, border_upper + caret_length),
            (border_right, border_upper),
            (border_right - caret_length, border_upper),
            (border_right, border_upper),
        ]

        points_ul = [
            (border_left, border_upper + caret_length),
            (border_left, border_upper),
            (border_left + caret_length, border_upper),
            (border_left, border_upper),
        ]

        points_ll = [
            (border_left, border_lower - caret_length),
            (border_left, border_lower),
            (border_left + caret_length, border_lower),
            (border_left, border_lower),
        ]

        point_list = [points_lr, points_ur, points_ul, points_ll]

        dc.DrawPolygonList(point_list, pens=pen, brushes=brush)

        self.old_cursor_row_col = row, col

    def update_cursor(self, dc, grid, row, col):
        """Whites out the old cursor and draws the new one"""

        old_row, old_col = self.old_cursor_row_col

        self._draw_cursor(dc, grid, old_row, old_col,
                          pen=wx.WHITE_PEN, brush=wx.WHITE_BRUSH)
        self._draw_cursor(dc, grid, row, col)

    def get_merging_cell(self, grid, key):
        """Returns row, col, tab of merging cell if the cell key is merged"""

        return grid.code_array.cell_attributes.get_merging_cell(key)

    def get_merged_rect(self, grid, key, rect):
        """Returns cell rect for normal or merged cells and None for merged"""

        row, col, tab = key

        # Check if cell is merged:
        cell_attributes = grid.code_array.cell_attributes
        merge_area = cell_attributes[row, col, tab]["merge_area"]

        if merge_area is None:
            return rect

        else:
            # We have a merged cell
            top, left, bottom, right = merge_area

            # Are we drawing the top left cell?
            if top == row and left == col:
                # Set rect to merge area
                ul_rect = grid.CellToRect(row, col)
                br_rect = grid.CellToRect(bottom, right)

                width = br_rect.x - ul_rect.x + br_rect.width
                height = br_rect.y - ul_rect.y + br_rect.height

                rect = wx.Rect(ul_rect.x, ul_rect.y, width, height)

                return rect

    def Draw(self, grid, attr, dc, rect, row, col, isSelected):
        """Draws the cell border and content using pycairo"""

        key = row, col, grid.current_table

        rect = self.get_merged_rect(grid, key, rect)
        if rect is None:
            # Merged cell
            if grid.is_merged_cell_drawn(key):
                row, col, __ = key = self.get_merging_cell(grid, key)
                rect = grid.CellToRect(row, col)
                rect = self.get_merged_rect(grid, key, rect)
            else:
                return

        rect_tuple = 0, 0, rect.width / self.zoom, rect.height / self.zoom

        sorted_keys = sorted(grid.code_array.cell_attributes[key].iteritems())

        # Button cells shall not be executed for preview
        if grid.code_array.cell_attributes[key]["button_cell"]:
            cell_preview = repr(grid.code_array(key))[:100]
        else:
            cell_preview = repr(grid.code_array[key])[:100]

        cell_cache_key = (rect_tuple[2], rect_tuple[3], isSelected,
                          cell_preview, tuple(sorted_keys))

        mdc = wx.MemoryDC()
        pxoffs = int(self.zoom)
        if cell_cache_key in self.cell_cache:
            mdc.SelectObject(self.cell_cache[cell_cache_key])

        else:
            bmp = wx.EmptyBitmap(rect.width + pxoffs, rect.height + pxoffs)
            mdc.SelectObject(bmp)
            mdc.SetBackgroundMode(wx.TRANSPARENT)
            mdc.SetDeviceOrigin(0, 0)
            context = wx.lib.wxcairo.ContextFromDC(mdc)

            # Set hint style off to get consistent zooming
            font_options = cairo.FontOptions()
            font_options.set_hint_metrics(cairo.HINT_METRICS_OFF)
            font_options.set_hint_style(cairo.HINT_STYLE_NONE)
            context.set_font_options(font_options)

            # Shift by 0.5 * zoom in order to avoid blurry lines
            x_shift = 0.5 * self.zoom
            y_shift = 0.5 * self.zoom
            context.translate(x_shift, y_shift)

            context.set_source_rgb(1, 1, 1)
            context.rectangle(0, 0, rect.width + pxoffs, rect.height + pxoffs)
            context.fill()
            context.stroke()

            # Zoom context
            context.scale(self.zoom, self.zoom)

            # Draw cell
            cell_renderer = GridCellCairoRenderer(context, self.data_array,
                                                  key, rect_tuple)

            cell_renderer.draw()

            # Draw selection if present
            if isSelected:
                context.set_source_rgba(*self.selection_color_tuple)
                context.rectangle(*rect_tuple)
                context.fill()

            context.scale(1.0/self.zoom, 1.0/self.zoom)
            context.translate(-x_shift, -y_shift)

            # Put resulting bmp into cache
            self.cell_cache[cell_cache_key] = bmp

        dc.Blit(rect.x-1, rect.y-1,
                rect.width + pxoffs,
                rect.height + pxoffs,
                mdc, 0, 0, wx.COPY)

        # Draw cursor
        if grid.actions.cursor[:2] == (row, col):
            self.update_cursor(dc, grid, row, col)

# end of class Draw
