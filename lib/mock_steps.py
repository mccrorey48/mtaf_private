import re
from lib.user_exception import UserException as Ux

step_re = re.compile('''@[^(]+\(['"](.+)['"]\)''')
def_re = re.compile('\s*def\s')
pass_re = re.compile('\s*pass')
comment_re = re.compile('\s*#')
exec_steps_re = re.compile('\s*context\.execute_steps')
end_exec_steps_re = re.compile("\s*'''\)")
fake_re = re.compile("\s*'''\)")

class MockDetector:
    def __init__(self, step_filename, fake_tag=False):
        is_mock = {}
        current_key = None
        quoted = False
        fake = False
        with open(step_filename) as f:
            lines = f.readlines()
            for lnum, line in enumerate(lines):
                if '"""' in line:
                    quoted = not quoted
                    continue
                if quoted:
                    continue
                m = step_re.match(line)
                if m:
                    step_key = m.group(1).lower()
                    # print step_key
                    if step_key in is_mock:
                        raise Ux("duplicate step name on line %s" % (lnum + 1) )
                    else:
                        is_mock[step_key] = True
                    fake = False
                    current_key = step_key
                else:
                    if 'fake' in line:
                        if fake_tag:
                            fake = True
                        continue
                    if fake:
                        continue
                    if current_key and len(line.strip()):
                        if not (('def' in line) or ('pass' in line) or comment_re.match(line)):
                            is_mock[current_key] = False
        self.mock_steps = []
        for key in sorted(is_mock.keys()):
            if is_mock[key]:
                self.mock_steps.append(key)
        re_split = re.compile('{[^}]*}')
        self.splits = [re_split.split(text) for text in self.mock_steps if len(re_split.split(text)) > 1]

    def match(self, step_name):
        if step_name.lower() in self.mock_steps:
            return True
        for split in self.splits:
            if re.match('.*'.join(split), step_name.lower()):
                return True
        else:
            print step_name
            return False


