import re
from lib.user_exception import UserException as Ux
import os

step_re = re.compile('''@[^(]+\(['"](.+)['"]\)''')
def_re = re.compile('\s*def\s')
nonspace_line_re = re.compile('(\s*)\S')
pass_re = re.compile('\s*pass')
single_quoted_re = re.compile("(?ms)[ \t]*'''.*?'''\n?")
double_quoted_re = re.compile('(?ms)[ \t]*""".*?"""\n?')
comment_re = re.compile('\s*#')
fake_re = re.compile("(\s*)if ['\"]fake['\"] not in str")

class MockDetector:
    def __init__(self, step_directory, fake_tag=False):
        is_mock = {}
        # fake_indent = None
        # skip_fake_block = False
        step_is_fake = False
        for filename in [name for name in os.listdir(step_directory) if name.endswith('.py')]:
            with open(os.path.join(step_directory, filename)) as f:
                current_key = None
                text = f.read()
                # remove triple-quoted text
                text = ''.join(single_quoted_re.split(text))
                text = ''.join(double_quoted_re.split(text))
                lines = text.split('\n')
                for lnum, line in enumerate(lines):
                    m = step_re.match(line)
                    if m:
                        step_key = m.group(1).lower()
                        # print step_key
                        if step_key in is_mock:
                            raise Ux("duplicate step name on line %s" % (lnum + 1) )
                        else:
                            is_mock[step_key] = True
                        # any "if fake" blocks ended when a new step started
                        # skip_fake_block = False
                        step_is_fake = False
                        current_key = step_key
                    else:
                        # when "fake" is one of the tags passed to behave,
                        # and the word "fake" is mentioned in the executable code of a step,
                        # assume that the entire step is adequately faked (no real AUT interaction)
                        m = fake_re.match(line)
                        if m:
                            if fake_tag:
                                # skip_fake_block = True
                                # fake_indent = len(m.group(1))
                                step_is_fake = True
                            continue
                        # if this step is assumed to be adequately faked, skip lines until another step match occurs
                        if step_is_fake:
                            continue
                        # for steps that don't mention "fake", see if there are any lines that should be
                        # counted as implementation, and if so, set is_mock[current_key] to False
                        m = nonspace_line_re.match(line)
                        if m:
                            if comment_re.match(line):
                                continue
                            if 'def' in line or 'pass' in line:
                                continue
                            if 'run_substep' in line:
                                continue
                            # if it gets to here, this should be an actual non-fake executable line
                            if current_key is not None:
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


