"""
    pyexcel.readers
    ~~~~~~~~~~~~~~~~~~~

    Uniform interface for describing a excel book

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""
import os
import uuid
from .iterators import SheetIterator
from .sheets import Sheet
from .utils import to_dict
from .io import load_file
from ._compact import OrderedDict


def load_book(file, **keywords):
    """Load content from physical file

    :param str file: the file name
    :param any keywords: additional parameters
    """
    path, filename = os.path.split(file)
    book = load_file(file, **keywords)
    sheets = book.sheets()
    return Book(sheets, filename, path, **keywords)


def load_book_from_memory(file_type, file_content, **keywords):
    """Load content from memory content

    :param tuple the_tuple: first element should be file extension,
    second element should be file content
    :param any keywords: additional parameters
    """
    book = load_file((file_type, file_content), **keywords)
    sheets = book.sheets()
    return Book(sheets, **keywords)


class Book:
    """Read an excel book that has mutliple sheets

    For csv file, there will be just one sheet
    """
    def __init__(self, sheets={}, filename="memory", path=None, **keywords):
        """
        Book constructor

        Selecting a specific book according to filename extension
        """
        self.path = path
        self.filename = filename
        self.name_array = []
        self.load_from_sheets(sheets)

    def load_from_sheets(self, sheets):
        """Load content from existing sheets

        :param dict sheets: a dictionary of sheets. Each sheet is a list of lists
        """
        self.sheets = OrderedDict()
        keys = sheets.keys()
        if not isinstance(sheets, OrderedDict):
            #if the end user does not care about the order
            #we put alphatical order
            keys = sorted(keys)
        for name in keys:
            self.sheets[name] = self.get_sheet(sheets[name], name)
        self.name_array = list(self.sheets.keys())

    def get_sheet(self, array, name):
        """Create a sheet from a list of lists"""
        return Sheet(array, name)

    def __iter__(self):
        return SheetIterator(self)

    def number_of_sheets(self):
        """Return the number of sheets"""
        return len(self.name_array)

    def sheet_names(self):
        """Return all sheet names"""
        return self.name_array

    def sheet_by_name(self, name):
        """Get the sheet with the specified name"""
        return self.sheets[name]

    def sheet_by_index(self, index):
        """Get the sheet with the specified index"""
        if index < len(self.name_array):
            sheet_name = self.name_array[index]
            return self.sheets[sheet_name]

    def remove_sheet(self, sheet):
        if isinstance(sheet, int):
            if sheet < len(self.name_array):
                sheet_name = self.name_array[sheet]
                del self.sheets[sheet_name]
                self.name_array = list(self.sheets.keys())
            else:
                raise IndexError
        elif isinstance(sheet, str):
            if sheet in self.name_array:
                del self.sheets[sheet]
                self.name_array = list(self.sheets.keys())
            else:
                raise KeyError
        else:
            raise TypeError

    def __getitem__(self, key):
        if type(key) == int:
            return self.sheet_by_index(key)
        else:
            return self.sheet_by_name(key)

    def __delitem__(self, other):
        self.remove_sheet(other)
        return self

    def __add__(self, other):
        """Operator overloading

        example::

            book3 = book1 + book2
            book3 = book1 + book2["Sheet 1"]

        """
        content = {}
        a = to_dict(self)
        for k in a.keys():
            new_key = k
            if len(a.keys()) == 1:
                new_key = "%s_%s" % (self.filename, k)
            content[new_key] = a[k]
        if isinstance(other, Book):
            b = to_dict(other)
            for l in b.keys():
                new_key = l
                if len(b.keys()) == 1:
                    new_key = other.filename
                if new_key in content:
                    uid = uuid.uuid4().hex
                    new_key = "%s_%s" % (l, uid)
                content[new_key] = b[l]
        elif isinstance(other, Sheet):
            new_key = other.name
            if new_key in content:
                uid = uuid.uuid4().hex
                new_key = "%s_%s" % (other.name, uid)
            content[new_key] = other.array
        else:
            raise TypeError
        c = Book()
        c.load_from_sheets(content)
        return c

    def __iadd__(self, other):
        """Operator overloading +=

        example::

            book += book2
            book += book2["Sheet1"]
        
        """
        if isinstance(other, Book):
            names = other.sheet_names()
            for name in names:
                new_key = name
                if len(names) == 1:
                    new_key = other.filename
                if new_key in self.name_array:
                    uid = uuid.uuid4().hex
                    new_key = "%s_%s" % (name, uid)
                self.sheets[new_key] = self.get_sheet(other[name].array,
                                                      new_key)
        elif isinstance(other, Sheet):
            new_key = other.name
            if new_key in self.name_array:
                uid = uuid.uuid4().hex
                new_key = "%s_%s" % (other.name, uid)
            self.sheets[new_key] = self.get_sheet(other.array, new_key)
        else:
            raise TypeError
        self.name_array = list(self.sheets.keys())
        return self

    def save_as(self, filename):
        """Save the content to a new file

        :param str filename: a file path
        """
        from .writers import BookWriter
        writer = BookWriter(filename)
        writer.write_book_reader(self)
        writer.close()

    def save_to_memory(self, file_type, stream):
        """Save the content to a memory stream

        :param iostream stream: a memory stream
        """
        from .writers import BookWriter
        writer = BookWriter((file_type, stream))
        writer.write_book_reader(self)
        writer.close()

    def to_dict(self):
        """Convert the book to a dictionary"""
        from .utils import to_dict
        return to_dict(self)


def BookReader(file, **keywords):
    """For backward compatibility
    """
    return load_book(file, **keywords)


def load(file, sheetname=None, name_columns_by_row=-1, name_rows_by_column=-1, **keywords):
    """Constructs an instance :class:`Sheet` from a sheet of an excel file

    except csv, most excel files has more than one sheet.
    Hence sheetname is required here to indicate from which sheet the instance
    should be constructed. If this parameter is omitted, the first sheet, which
    is indexed at 0, is used. For csv, sheetname is always omitted because csv
    file contains always one sheet.
    :param str sheetname: which sheet to be used for construction
    :param int name_colmns_by_row: which row to give column names
    :param int name_rows_by_column: which column to give row names
    :param dict keywords: other parameters
    """
    book = load_file(file, **keywords)
    sheets = book.sheets()
    if sheetname:
        if sheetname not in sheets:
            raise KeyError("%s is not found" % sheetname)
    else:
        keys = list(sheets.keys())
        sheetname = keys[0]
    return Sheet(sheets[sheetname],
                 sheetname,
                 name_columns_by_row=name_columns_by_row,
                 name_rows_by_column=name_rows_by_column)


def load_from_memory(file_type, file_content, sheetname=None, **keywords):
    """Constructs an instance :class:`Sheet` from memory

    :param str file_type: one value of these: 'csv', 'xls', 'xlsm', 'xslm', 'ods'
    :param iostream file_content: file content
    :param str sheetname: which sheet to be used for construction
    :param dict keywords: any other parameters
    """
    return load((file_type, file_content), sheetname, **keywords)


def Reader(file=None, sheetname=None, **keywords):
    """
    A single sheet excel file reader

    Default is the sheet at index 0. Or you specify one using sheet index
    or sheet name. The short coming of this reader is: column filter is
    applied first then row filter is applied next

    use as class would fail though
    changed since 0.0.7
    """
    return load(file, sheetname, **keywords)


def SeriesReader(file=None, sheetname=None, series=0, **keywords):
    """A single sheet excel file reader and it has column headers in a selected row

    use as class would fail
    changed since 0.0.7
    """
    return load(file, sheetname, name_columns_by_row=series, **keywords)


def ColumnSeriesReader(file=None, sheetname=None, series=0, **keywords):
    """A single sheet excel file reader and it has row headers in a selected column

    use as class would fail
    changed since 0.0.7
    """
    return load(file, sheetname, name_rows_by_column=series, **keywords)


def PlainReader(file, sheetname=None, **keywords):
    """PlainReader exists for speed over Reader and also for testing purposes

    use as class would fail
    changed since 0.0.7
    """
    return load(file, sheetname, **keywords)


def FilterableReader(file, sheetname=None, **keywords):
    """FiltableReader lets you use filters at the sequence of your choice
    
    use as class would fail
    changed since 0.0.7
    """
    return load(file, sheetname, **keywords)