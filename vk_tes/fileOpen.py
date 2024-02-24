
import openpyxl


def take_groups(file='/Users/a.sagitovich/programming/BFU/TES/vk_tes/list_one.xlsx'):

    book = openpyxl.load_workbook(file)
    page = book.active

    list_ = []
    for i in page['A']:
        if i.value is not None:
            list_.append(i.value)
    return list_
