class SpecialChar:
    SPACE = " "
    OPEN_SQUARE_BRACKET = "["
    CLOSING_SQUARE_BRACKET = "]"
    DOLLAR = "$"

    ADDITIONAL_END_MARKERS = ["?", "!", "^", "°", "@", "€", "*", "+", "~", "#", "'", "-", ".", ",", ";", ":", "<", ">", "|", "\"",
                              "§", "%", "&", "/", "{", "(", ")", "[", "]", "}", "=", "\\", "´", "`"]

    START_MARKERS = [OPEN_SQUARE_BRACKET, DOLLAR]
    END_MARKERS = [OPEN_SQUARE_BRACKET, CLOSING_SQUARE_BRACKET, SPACE, DOLLAR]
    END_MARKERS.extend(ADDITIONAL_END_MARKERS)
