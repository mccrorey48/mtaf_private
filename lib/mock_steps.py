import re
from lib.user_exception import UserException as Ux
import os

step_re = re.compile('''@[^(]+\(['"](.+)['"]\)''')
def_re = re.compile('\s*def\s')
pass_re = re.compile('\s*pass')
comment_re = re.compile('\s*#')
exec_steps_re = re.compile('\s*context\.execute_steps')
end_exec_steps_re = re.compile("\s*'''\)")
fake_re = re.compile("\s*'''\)")

class MockDetector:
    def __init__(self, step_directory, fake_tag=False):
        is_mock = {}
        current_key = None
        quoted = False
        fake = False
        for filename in [name for name in os.listdir(step_directory) if name.endswith('.py')]:
            with open(os.path.join(step_directory, filename)) as f:
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
        self.splits = []
        for text in self.mock_steps:
            items = re_split.split(text)
            if len(items) > 1:
                # only add to self.splits if the text contains a match for re_split
                # but first escape '[' and ']' since we use it in a regex later
                new_split = []
                for item in items:
                    item = '\]'.join(item.split(']'))
                    item = '\['.join(item.split('['))
                    new_split.append(item)
                self.splits.append(new_split)

    def match(self, step_name):
        if step_name.lower() in self.mock_steps:
            return True
        for split in self.splits:
            if re.match('.*'.join(split), step_name.lower()):
                return True
        else:
            print step_name
            return False


