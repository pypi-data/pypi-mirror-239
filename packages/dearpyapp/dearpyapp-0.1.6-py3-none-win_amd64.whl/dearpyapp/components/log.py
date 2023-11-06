import asyncio
import typing as t

import dearpygui.dearpygui as dpg
from dearpyapp import *
import pyperclip


class TableLog:
    # TODO callumns_info in dataclass, wrap parameter
    # TODO для скрытия колнки dpg.configure_item(col, show=True, enabled=False)
    # TODO передавать теги стиля текста, как в html
    # TODO не обновлять лог, если таблица не отрисовывалась (get_available_content_region(table_window) == [0, 0])
    # TODO не обновлять лог, если таблица не видна
    # TODO если строк в таблице больше ~900 и ее видно, то ctrl-c на любом input_text приводит к
    #  зависанию(коллбэки не обрабатываются, буфер обмена в других приложениях не работает), если установить в
    #  таблице clipper=True, то все ок, сейчас при больше 900, включается клиппер
    # TODO dpg.clipper для таблиц, так как если таблица видна, то на обновление тратится много ресурсов
    # TODO horizontal scroll + autofit all
    # TODO сделать скрываемые колонки, попробовать использовать нативные хедеры
    # TODO self.rows to list?

    columns = []
    scroll_size = 20

    def __init__(self, *, log_size=100):
        self.gui = self._Gui()
        self.log_size = log_size
        self.column_widths = [0] * len(self.columns)
        self.wrap_text = True
        self.rows: dict[int, list[int]] = {}
        self.show_scroll_to_end_btn = False
        self._selected_row_index = -1
        self._input_text_row = None
        self._input_text_cell = None

    # TODO сделать по-нормальному
    async def _task(self):
        while True:
            try:
                self._width_changed()
            except SystemError:
                break
            else:
                await asyncio.sleep(0.2)

    def _width_changed(self):
        gui = self.gui
        if not dpg.is_item_visible(gui.group):
            return

        dpg.configure_item(gui.table_group,
                           width=dpg.get_available_content_region(gui.table_window)[0])
        len_columns = len(self.columns)
        group = 0
        for group, column, index in zip(dpg.get_item_children(dpg.get_item_children(gui.header, 1)[0], 1),
                                        dpg.get_item_children(gui.table, 0), range(len_columns)):
            actual_width = dpg.get_available_content_region(group)[0] - 4
            actual_width = actual_width if index != len_columns - 1 else \
                actual_width - self.scroll_size
            if self.column_widths[index] != actual_width:
                self._input_text_cleanup()
                self.column_widths[index] = actual_width
                dpg.configure_item(column, init_width_or_weight=actual_width + 4,)
                # TODO нормально сделать колонки, где нужно wrap делать
                if self.wrap_text:
                    for row in dpg.get_item_children(gui.table, 1):
                        fields = dpg.get_item_children(row, 1)
                        if len(fields) - 1 < index or dpg_get_item_type(fields[index]) != dpg.mvText:
                            continue
                        dpg.configure_item(fields[index], wrap=actual_width)

        if group != 0 and self.show_scroll_to_end_btn:
            x, y = dpg.get_item_pos(group)
            dpg.configure_item(
                gui.scroll_to_end_btn,
                pos=(x + dpg.get_item_rect_size(group)[0] - 20, y),
                show=dpg.get_y_scroll_max(gui.table_window) != dpg.get_y_scroll(gui.table_window))

    def append(self, data):
        self.extend((data, ))

    def extend(self, iterable: t.Iterable):
        if not dpg.does_item_exist(self.gui.group):
            return

        with dpg.mutex():
            with dpg_container(self.gui.table):
                for data in iterable:
                    if not (data := self._process_data(data)):
                        continue
                    with dpg.table_row() as row:
                        fields = []
                        for index, field in enumerate(data):
                            if isinstance(field, t.Callable):
                                fields.append(field())
                                continue

                            color = c.NONE
                            if not isinstance(field, str):
                                field, color = field
                            fields.append(dpg.add_text(field, color=color,
                                                       wrap=self.column_widths[index] if self.wrap_text else -1))
                    self.rows.update({row: fields})
            self._delete_rows()

    def _process_data(self, data) -> t.Iterable:
        ...

    def clear(self):
        gui = self.gui
        self._input_text_row and self._input_text_cleanup()
        dpg.delete_item(gui.table, slot=1, children_only=True)
        dpg.set_y_scroll(gui.table_window, -1)
        self._selected_row_index = -1
        self.rows.clear()

    def set_y_scroll_to_end(self):
        dpg.set_y_scroll(self.gui.table_window, -1)

    def _delete_rows(self):
        gui = self.gui
        scroll_max = dpg.get_y_scroll_max(gui.table_window)
        scroll_pos = dpg.get_y_scroll(gui.table_window)
        rows = dpg.get_item_children(self.gui.table, slot=1)
        len_rows = len(rows)
        if (scroll_pos == scroll_max or scroll_pos < 0 or len_rows > self.log_size * 2) and\
                (rows_to_delete := len_rows - self.log_size) > 0:
            for row_index in range(rows_to_delete):
                row = rows[row_index]
                (row in self.rows) and self.rows.pop(row)
                (row == self._input_text_row) and self._input_text_cleanup()
                dpg.delete_item(row)
            self.select_row(self._selected_row_index - rows_to_delete)

        if scroll_pos == scroll_max:
            self.set_y_scroll_to_end()

    def _clipboard_copy(self):
        if dpg.is_key_down(dpg.mvKey_Control) and dpg.is_item_focused(self.gui.input_text):
            pyperclip.copy(str.replace(
                pyperclip.paste() or '', '\r\n', ''
            ))

    def _input_text_cleanup(self):
        gui = self.gui
        self._input_text_cell and dpg.move_item(self._input_text_cell, before=gui.input_text)
        dpg.move_item(gui.input_text, parent=gui.input_text_stage)
        self._input_text_row = None
        self._input_text_cell = None

    def _cell_clicked(self):
        gui = self.gui
        if not self.rows or dpg.is_item_hovered(gui.input_text):
            return

        # TODO to function
        container = gui.table_window
        width_offset = height_offset = 0
        while container:
            width, height = dpg.get_item_pos(container)
            width_offset += width
            height_offset += height
            container = dpg_get_item_container(container, dpg.mvChildWindow) or \
                dpg_get_item_container(container)

        mouse_pos = dpg.get_mouse_pos(local=False)
        mouse_pos = (dpg.get_x_scroll(gui.table_window) + mouse_pos[0] - width_offset,
                     dpg.get_y_scroll(gui.table_window) + mouse_pos[1] - height_offset)  # + 15

        rows = tuple(self.rows.values())
        _, row_index = dpg_get_item_by_pos([cells[0] for cells in rows], mouse_pos, return_index=True)
        cell, cell_index = dpg_get_item_by_pos(rows[row_index], mouse_pos, horizontal=True, return_index=True)
        text, width, height = dpg_get_text_from_cell(cell, wrap=self.column_widths[cell_index])
        if text is None:
            self._input_text_cleanup()
        else:
            self._input_text_cell and dpg.move_item(self._input_text_cell, before=gui.input_text)
            self._input_text_row = tuple(self.rows)[row_index]
            self._input_text_cell = cell
            dpg.configure_item(gui.input_text, default_value=text,
                               width=width + 2, height=height)  # width + 2 prevent input_text to scrolling
            dpg.move_item(gui.input_text, before=cell)
            dpg.move_item(cell, parent=gui.input_text_stage)

        self.select_row(row_index)

    def select_row(self, index: int = None):
        try:
            if self._selected_row_index >= 0:
                dpg.unset_table_row_color(self.gui.table, self._selected_row_index)
            if index is not None:
                self._selected_row_index = index
            if self._selected_row_index >= 0:
                dpg.set_table_row_color(self.gui.table, self._selected_row_index, c.BLUE_4)
        except SystemError:
            self._selected_row_index = -1

    # TODO implement delete method
    # def close(self):
    #     # get_running_app().size_subscribers.remove(self._width_changed)
    #     # dpg.delete_item(self.gui.handler_reg)
    #     dpg.delete_item(self.gui.group)

    def create_gui(self):
        gui = self.gui
        get_running_app().loop.create_task(self._task())

        header_buttons_theme = dpg_get_color_theme((c.TRANSPARENT, c.TRANSPARENT, c.TRANSPARENT),
                                                   text_color=c.BLUE_18, text_align=(0, 0.5))

        with dpg.theme() as table_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_style(dpg.mvStyleVar_CellPadding, 4, 4)
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0, 0)
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, 0)

                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, c.GRAY_2)
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, c.GRAY_5)
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, c.GRAY_6)
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, c.BLUE_9)

                dpg.add_theme_color(dpg.mvThemeCol_TableBorderLight, c.GRAY_4)
                dpg.add_theme_color(dpg.mvThemeCol_TableBorderStrong, c.GRAY_4)

                dpg.add_theme_color(dpg.mvThemeCol_Text, c.GRAY_22)

            with dpg.theme_component(dpg.mvInputText):
                dpg.add_theme_color(dpg.mvThemeCol_Text, c.GRAY_25)
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, c.BLUE_4)
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, c.BLUE_4)

        with dpg.handler_registry():
            dpg.add_key_press_handler(dpg.mvKey_C, callback=lambda *_: self._clipboard_copy())

        with dpg.item_handler_registry() as table_handler_reg:
            dpg.add_item_clicked_handler(dpg.mvMouseButton_Left, callback=lambda *_: self._cell_clicked())

        with dpg.group(tag=gui.group):
            dpg.bind_item_theme(dpg.last_container(), table_theme)
            dpg.bind_item_theme(
                dpg.add_button(tag=gui.scroll_to_end_btn, label='\u25BC', height=20, width=20, pos=(0, 0), show=False,
                               callback=lambda *_: self.set_y_scroll_to_end()),
                dpg_get_color_theme(colors=(c.TRANSPARENT, c.GRAY_5, c.TRANSPARENT),
                                    text_color=c.YELLOW_19))

            # TODO cleanup_stage after close in delete method
            with dpg.stage(tag=gui.input_text_stage):
                dpg.add_input_text(readonly=True, multiline=True, tag=gui.input_text)
            with dpg.table(header_row=False, borders_innerH=False, borders_outerH=False,
                           borders_innerV=True, borders_outerV=False, tag=gui.header,
                           resizable=True, reorderable=True):
                for name, width, fixed in self.columns:
                    dpg.add_table_column(width_fixed=fixed, width_stretch=not fixed, init_width_or_weight=width)
                with dpg.table_row():
                    for name, width, fixed in self.columns:
                        btn = dpg.add_button(label=name, width=-1)
                        dpg.bind_item_theme(btn, header_buttons_theme)
            with dpg.child_window(border=False, tag=gui.table_window, height=-2):
                with dpg.group(tag=gui.table_group):
                    dpg.bind_item_handler_registry(gui.table_group, table_handler_reg)
                    with dpg.table(policy=dpg.mvTable_SizingFixedFit, borders_innerH=True, borders_outerH=False,
                                   borders_innerV=True, borders_outerV=False, tag=gui.table, header_row=False,
                                   resizable=False, reorderable=True, freeze_rows=1, hideable=True,
                                   clipper=self.log_size > 900):
                        for name, width, fixed in self.columns:
                            dpg.add_table_column(width_fixed=True, init_width_or_weight=width)

    def create_themes(self):
        ...

    @dpg_uuid
    class _Gui:
        group: int
        header: int
        input_text: int
        input_text_stage: int
        table_window: int
        table_group: int
        table: int
        scroll_to_end_btn: int
        # handler_reg: int

