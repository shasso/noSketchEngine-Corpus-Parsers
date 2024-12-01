# utils.py

# Define additional punctuation marks
additional_punctuation = {
    '\u002d',  # HYPHEN-MINUS
    '\u060c',  # ARABIC COMMA
    '\u061b',  # ARABIC SEMICOLON
    '\u061f',  # ARABIC QUESTION MARK
    '\u2018',  # LEFT SINGLE QUOTATION MARK
    '\u2019',  # RIGHT SINGLE QUOTATION MARK
    '\u201c',  # LEFT DOUBLE QUOTATION MARK
    '\u201d',  # RIGHT DOUBLE QUOTATION MARK
    '\u002c',  # COMMA
    '\u0703',  # SYRIAC SUPRALINEAR COLON
    '\u0702',   # SYRIAC SUBLINEAR FULL STOP
    '\u0028',  # LEFT PARENTHESIS
    '\u0029',  # RIGHT PARENTHESIS
}

def tokenize_sentence(sentence):
    tokens = []
    word = ""
    for char in sentence:
        if char in ".,;:!?" or char in additional_punctuation:
            if word:
                tokens.append(word)
                word = ""
            tokens.append("<g/>")
            tokens.append(char)
        elif char.isspace():
            if word:
                tokens.append(word)
                word = ""
        else:
            word += char
    if word:
        tokens.append(word)
    return tokens