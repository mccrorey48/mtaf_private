def get_filter(method, *args, **kwargs):

    def by_text_start(elems):
        return [elem for elem in elems if elem.text[:len(args[0])] == args[0]]

    def by_text_all(elems):
        return [elem for elem in elems if elem.text == args[0]]

    def by_subelement_text_all(elems):
        subelement_locator = kwargs['subelement_locator']
        view_instance = kwargs['view_instance']
        actions = view_instance.actions
        return [elem for elem in elems if actions.find_sub_element_by_locator(elem, subelement_locator).text == args[0]]
    
    if method == 'text_start':
        return by_text_start
    elif method == 'text_all':
        return by_text_all
    elif method == 'subelement_text_all':
        return by_subelement_text_all
