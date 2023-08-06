
"""
    pyexcel
    ~~~~~~~~~~~~~~~~~~~

    **pyexcel** is a wrapper library to read, manipulate and
    write data in different excel formats: csv, ods, xls, xlsx
    and xlsm. It does not support styling, charts.

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""

from .readers import (Reader,
                      BookReader,
                      Book,
                      load,
                      load_from_memory,
                      load_book,
                      load_book_from_memory)
from .writers import Writer, BookWriter
from .readers import (SeriesReader,
                      ColumnSeriesReader,
                      PlainReader,
                      FilterableReader)
from .utils import to_dict, to_array, to_records, dict_to_array, from_records
from .iterators import transpose
from .formatters import (ColumnFormatter,
                         RowFormatter,
                         SheetFormatter,
                         NamedColumnFormatter,
                         NamedRowFormatter)
from .filters import (ColumnIndexFilter,
                      ColumnFilter,
                      RowFilter,
                      EvenColumnFilter,
                      OddColumnFilter,
                      EvenRowFilter,
                      OddRowFilter,
                      RowIndexFilter,
                      SingleColumnFilter,
                      SingleRowFilter)
from .sheets import Sheet
from .cookbook import (merge_csv_to_a_book,
                       merge_all_to_a_book,
                       split_a_book,
                       extract_a_sheet_from_a_book)

__VERSION__ = '0.0.7'
