from inspector import run_inspector

default_cfg = {
    'csv_dir': '.',
    'xml_dir': '.',
    'screenshot_dir': '.',
    'log_dir': '.',
    'tmp_dir': '.'
}


def start(cfg=default_cfg):
    run_inspector(cfg)
