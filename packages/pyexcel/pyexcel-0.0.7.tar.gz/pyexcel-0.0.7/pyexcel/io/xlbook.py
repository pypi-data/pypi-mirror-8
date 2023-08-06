"""
    pyexcel.io.xlbook
    ~~~~~~~~~~~~~~~~~~~

    The lower level xls/xlsx/xlsm file format handler using xlrd/xlwt

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""
import datetime
import xlrd
from xlwt import Workbook, XFStyle
from .._compact import OrderedDict


XLS_FORMAT_CONVERSION = {
    xlrd.XL_CELL_TEXT: str,
    xlrd.XL_CELL_EMPTY: None,
    xlrd.XL_CELL_DATE: datetime.datetime,
    xlrd.XL_CELL_NUMBER: float,
    xlrd.XL_CELL_BOOLEAN: int,
    xlrd.XL_CELL_BLANK: None,
    xlrd.XL_CELL_ERROR: None
}


def xldate_to_python_date(value):
    """
    convert xl date to python date
    """
    date_tuple = xlrd.xldate_as_tuple(value, 0)
    ret = None
    if date_tuple == (0, 0, 0, 0, 0, 0):
        ret = datetime.datetime(1900, 1, 1, 0, 0, 0)
    elif date_tuple[0:3] == (0, 0, 0):
        ret = datetime.time(date_tuple[3],
                            date_tuple[4],
                            date_tuple[5])
    elif date_tuple[3:6] == (0, 0, 0):
        ret = datetime.date(date_tuple[0],
                            date_tuple[1],
                            date_tuple[2])
    return ret


class XLSheet:
    """
    xls sheet

    Currently only support first sheet in the file
    """
    def __init__(self, sheet):
        self.worksheet = sheet

    def number_of_rows(self):
        """
        Number of rows in the xls sheet
        """
        return self.worksheet.nrows

    def number_of_columns(self):
        """
        Number of columns in the xls sheet
        """
        return self.worksheet.ncols

    def cell_value(self, row, column):
        """
        Random access to the xls cells
        """
        cell_type = self.worksheet.cell_type(row, column)
        my_type = XLS_FORMAT_CONVERSION[cell_type]
        value = self.worksheet.cell_value(row, column)
        if my_type == datetime.datetime:
            value = xldate_to_python_date(value)
        return value


def to_array(sheet):
    array = []
    for r in range(0, sheet.number_of_rows()):
        row = []
        for c in range(0, sheet.number_of_columns()):
            row.append(sheet.cell_value(r, c))
        array.append(row)
    return array


class XLBook:
    """
    XLSBook reader

    It reads xls, xlsm, xlsx work book
    """

    def __init__(self, filename, file_content=None, **keywords):
        self.workbook = xlrd.open_workbook(filename, file_contents=file_content)
        self.mysheets = OrderedDict()
        for name in self.workbook.sheet_names():
            data = to_array(XLSheet(
                self.workbook.sheet_by_name(name)))
            self.mysheets[name] = data

    def sheets(self):
        """Get sheets in a dictionary"""
        return self.mysheets


class XLSheetWriter:
    """
    xls, xlsx and xlsm sheet writer
    """
    def __init__(self, wb, name):
        self.wb = wb
        if name:
            sheet_name = name
        else:
            sheet_name = "pyexcel_sheet1"
        self.ws = self.wb.add_sheet(sheet_name)
        self.current_row = 0

    def set_size(self, size):
        pass

    def write_row(self, array):
        """
        write a row into the file
        """
        for i in range(0, len(array)):
            value = array[i]
            style = None
            tmp_array = []
            if isinstance(value, datetime.date) or isinstance(value, datetime.datetime):
                tmp_array = [value.year, value.month, value.day]
                value = xlrd.xldate.xldate_from_date_tuple(tmp_array, 0)
                style = XFStyle()
                style.num_format_str = "DD/MM/YY"
            elif isinstance(value, datetime.time):
                tmp_array = [value.hour, value.minute, value.second]
                value = xlrd.xldate.xldate_from_time_tuple(tmp_array)
                style = XFStyle()
                style.num_format_str = "HH:MM:SS"
            if style:
                self.ws.write(self.current_row, i, value, style)
            else:
                self.ws.write(self.current_row, i, value)
        self.current_row += 1

    def close(self):
        """
        This call actually save the file
        """
        pass


class XLWriter:
    """
    xls, xlsx and xlsm writer
    """
    def __init__(self, file):
        self.file = file
        self.wb = Workbook()
        self.current_row = 0

    def create_sheet(self, name):
        return XLSheetWriter(self.wb, name)

    def close(self):
        """
        This call actually save the file
        """
        self.wb.save(self.file)
