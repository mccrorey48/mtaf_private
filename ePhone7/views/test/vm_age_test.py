from lib.android import get_age_range_minutes

ages = [
    '0 minutes ago',
    '1 minute ago',
    '5 minutes ago',
    '59 minutes ago',
    '1 hour ago',
    '2 hours ago',
    '23 hours ago',
    'Yesterday',
    '2 days ago',
    'Oct 24, 2017'
]

for age in ages:
    min, max = get_age_range_minutes(age)
    print "age: %s, min:%02d:%02d, max:%02d:%02d" % (age, min/60, min%60, max/60, max%60)

