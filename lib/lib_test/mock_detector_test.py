from lib.mock_detector import MockDetector
from glob import glob

mock_detector = MockDetector('ePhone7/features/steps', fake_tag=False)
for fname in glob('ePhone7/features/*.feature'):
    print fname
    with open(fname) as f:
        lines = [line.strip() for line in f.readlines()]
        for line in lines:
            if not (line.startswith('Feature') or line.startswith('Scenario') or line == ''):
                print "%80s: %s" % (line[6:], mock_detector.match(line[6:]))


pass
# mock_detector = MockDetector('lib/lib_test/features/steps', fake_tag=False)
# steps = [
#         'A fake step',
#         'A real step',
#         'A step with fake substep',
#         'A step with real substep'
#         ]
# for step in steps:
#     print step, mock_detector.match(step)
