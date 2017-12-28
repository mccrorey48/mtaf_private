from mtaf import inspector

cfg = {
    'csv_dir': 'csv',
    'xml_dir': 'xml',
    'screenshot_dir': 'screenshot',
    'log_dir': 'log',
    'tmp_dir': 'tmp'
}

inspector.start(cfg)
