from lib.mock_detector import MockDetector

mock_detector = MockDetector('lib/lib_test/features/steps', fake_tag=False)
steps = [
        'A fake step',
        'A real step',
        'A step with fake substep',
        'A step with real substep'
        ]
for step in steps:
    print step, mock_detector.match(step)
