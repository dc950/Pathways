import re


def contains_bad_word(term):
    """
    Returns true if there is a naught word in the term
    :param term: The term to be checked
    :return: True if there is a naughty word, false if it's clean
    """

    naughty_words = []
    with open('app/main/naughty_words.txt', 'r') as f:
        naughty_words = f.read().splitlines()
    # Setup regex
    #regex = r'[^!@#$%^&*]*'  # (foobar|foobaz|foofii)[^!@#$%^&*]*'
    regex = ''
    naughties = ''
    for i, w in enumerate(naughty_words):
        if i != 0:
            naughties += r'| '  # space is insterted as some words end with or contain words - surpass etc.
        naughties += w

    #  print(str(naughties))
    regex += naughties
    #regex += r'[^!@#$%^&*]*'
    print(regex)
    # ' ' is added so first word will be recognised
    if re.search(regex, ' '+term) is not None:
        return True
    return False
