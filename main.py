from app.kryptarytm import Algebraf, Kryptarytm

# required variables for algebraf:
url = "https://szarada.net/krzyzowki/pokaz/o-r-r-h-o-b/"

# required variables for kryptarym
# known_letters = (('a', 0),) # as a pairs of tuples
words = ['łopatka', 'do', 'wiadra']
equation = "/"
hint = [
#     ['e', 'e', 'ze', '*'],
#     ['e', 'e', 'od', '+']
]

# resolve algebraf or kryptarytm (uncomment appropriate)

# Algebraf(url).resolve_algebraf()
Kryptarytm(equation, words, hints=hint).resolve_kryptarytm()
