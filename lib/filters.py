def get_filter(method, *args, **kwargs):

    def by_text_start(elems):
        return [elem for elem in elems if elem.text[:len(args[0])] == args[0]]

    def by_text_all(elems):
        return [elem for elem in elems if elem.text == args[0]]

    if method == 'text_start':
        return by_text_start
    elif method == 'text_all':
        return by_text_all
