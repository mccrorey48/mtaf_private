import re
from lib.user_exception import UserException as Ux
import os

step_re = re.compile('''@[^(]+\(['"](.+)['"]\)''')
fake_wrapper_re = re.compile('''@fake''')
def_re = re.compile('\s*def\s')
nonspace_line_re = re.compile('(\s*)\S')
pass_re = re.compile('\s*pass')
triple_single_quoted_re = re.compile("(?ms)[ \t]*'''.*?'''\n?")
triple_double_quoted_re = re.compile('(?ms)[ \t]*""".*?"""\n?')
comment_re = re.compile('\s*#')
fake_re = re.compile("(\s*)if ['\"]fake['\"]")
substep_re = re.compile("\s*context\.run_substep\((\"([^\"]+)\"|\'([^\']+)\')\)")


class MockDetector:
    def __init__(self, step_directory, fake_tag=False):
        # for use by the "run_features.py" file that runs python behave feature files
        #
        # for each step defined in a *.py file in the features/steps directory,
        # determine if the step has any executable steps; if not, it is saved in self.mock_steps
        #
        # steps that have executable code should use the @step decorator; if so, they are considered fake if the
        # test is run with the "fake" tag, because the @fake decorator will cause the step implementation function
        # to not be called if the "fake" tag is used (this results in a "dry run" of the test steps and substeps)
        #
        # when we encounter a step implementation that includeds calls to "context.run_substep(<substep name>)",
        # make a list of the substeps called within the step but don't treat it as an executable line;
        # after the complete list of fake substeps has been compiled, go back and see if any of them actually
        # called non-fake substeps and if so, remove them from the fake list
        substeps = {}
        is_fake = {}
        step_is_fake = False
        for filename in [name for name in os.listdir(step_directory) if name.endswith('.py')]:
            with open(os.path.join(step_directory, filename)) as f:
                current_key = None
                text = f.read()
                # remove triple-quoted text
                text = ''.join(triple_single_quoted_re.split(text))
                text = ''.join(triple_double_quoted_re.split(text))
                lines = text.split('\n')
                for lnum, line in enumerate(lines):
                    m = step_re.match(line)
                    if m:
                        step_key = m.group(1).lower()
                        # print step_key
                        if step_key in is_fake:
                            raise Ux("duplicate step name on line %s" % (lnum + 1) )
                        else:
                            is_fake[step_key] = True
                        step_is_fake = False
                        current_key = step_key
                    else:
                        # if this step is assumed to be adequately faked, skip lines until another step match occurs
                        if step_is_fake:
                            continue
                        # when "fake" is one of the tags passed to behave,
                        # and the word "fake" is mentioned in the executable code of a step,
                        # assume that the entire step is adequately faked (no real AUT interaction)
                        m = fake_re.match(line)
                        m2 = fake_wrapper_re.match(line)
                        if m or m2:
                            if fake_tag:
                                step_is_fake = True
                            continue
                        # for steps that don't mention "fake", see if there are any lines that should be
                        # counted as implementation, and if so, set is_fake[current_key] to False
                        m = nonspace_line_re.match(line)
                        if m:
                            if comment_re.match(line):
                                continue
                            if 'def ' in line or 'pass' in line:
                                continue
                            if substep_re.match(line):
                                if substep_re.match(line).group(2) is not None:
                                    substep = substep_re.match(line).group(2)
                                elif substep_re.match(line).group(3) is not None:
                                    substep = substep_re.match(line).group(3)
                                else:
                                    raise Ux("substep re error, line = %s" % line)
                                if current_key not in substeps:
                                    substeps[current_key] = [substep]
                                else:
                                    substeps[current_key].append(substep)
                            # if it gets to here, this should be an actual non-fake executable line
                            if current_key is not None:
                                is_fake[current_key] = False
        self.fake_steps = []
        for key in sorted(is_fake.keys()):
            if is_fake[key]:
                self.fake_steps.append(key)
        re_split_parse_matcher = re.compile('{[^}]*}')
        re_split_re_matcher = re.compile('\(\?p<[^>]+>[^)]+\)')
        # in cases where the step name includes a parameter (the same step can be called with different values
        # in one or more places embedded in the step name string), the step name in the features file probably
        # won't match the step name that prefixes the python implementation in features/steps/*.py.
        #
        # to handle this, we keep a list of "splits" (arrays of the text bits separated by variable parameter
        # definitions) for fake steps with parameters
        #
        # the "splits" list is used by the "match" function to determine if a parameterized step in a feature file
        # matches a fake python step implementation
        self.splits = []
        for text in self.fake_steps[:]:
            items = re_split_parse_matcher.split(text)
            if len(items) > 1:
                # only add to self.splits if the text contains a match for re_split_parse_matcher
                # but first escape '[' and ']' since we use it in a regex later
                new_split = []
                for item in items:
                    item = '\]'.join(item.split(']'))
                    item = '\['.join(item.split('['))
                    new_split.append(item)
                self.splits.append(new_split)
                self.fake_steps.remove(text)
                continue
            items = re_split_re_matcher.split(text)
            if len(items) > 1:
                self.splits.append(items)
                self.fake_steps.remove(text)
                continue
        # go through self.fake_steps and remove any that call non-fake substeps
        # this will need to be reiterated as long as the length of self.fake_steps changes
        # with each iteration
        last_fake_count = len(self.fake_steps)
        while True:
            for text in self.fake_steps:
                if text in substeps:
                    for substep in substeps:
                        if substep not in self.fake_steps:
                            del self.fake_steps[text]
                            break
            if len(self.fake_steps) != last_fake_count:
                last_fake_count = len(self.fake_steps)
            else:
                break

    def match(self, step_name):
        if step_name.lower() in self.fake_steps:
            return True
        for split in self.splits:
            if re.match('[^"]*'.join(split), step_name.lower()):
                return True
        else:
            # print step_name
            return False


