def get_filter(method, *args, **kwargs):

    def by_text_start(elem):
        return elem.text[:len(args[0])] == kwargs['text']

    def by_text_all(elem):
        return elem.text == kwargs['text']

    def by_within_frame(elem):
        e = elem
        f = kwargs['frame']
        f_loc = f.loc
        f_size = f.size
        f_x1 = f_loc['x']
        f_x2 = f_loc['x'] + f_size['width']
        f_y1 = f_loc['y']
        f_y2 = f_loc['y'] + f_size['height']
        e_loc = e.loc
        e_size = e.size
        e_x1 = e_loc['x']
        e_x2 = e_loc['x'] + e_size['width']
        e_y1 = e_loc['y']
        e_y2 = e_loc['y'] + e_size['height']
        return e_x1 >= f_x1 and e_x2 <= f_x2 and e_y1 >= f_y1 and e_y2 <= f_y2

    if method == 'text_start':
        return by_text_start
    elif method == 'text_all':
        return by_text_all
    elif method == 'within_frame':
        return by_within_frame
