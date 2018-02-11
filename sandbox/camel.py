import re
def camel_case(text):
    words = re.split('[\s_]+', text)
    for i, word in enumerate(words[:]):
        word = word.lower()
        words[i] = word[0].upper() + word[1:]
    return ''.join(words)

print camel_case('now is the_time_for all')
