def del_new_lines(book):
    context = book.read().replace("\n", "")
    return context
