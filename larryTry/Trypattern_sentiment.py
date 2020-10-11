from pattern.en import parse
from pattern.en import pprint
from pattern.en import sentiment, polarity, subjectivity, positive
from pattern.en import wordnet, ADJECTIVE

#s = "Poland says the combination of a second wave of COVID-19 with flu season could create ""a lot of confusion"" because of their overlap in symptoms and put a heavy strain on the health care system. "
'''
for word in ("amazing", "horrible", "public"):
    print(word, sentiment(word))

print(sentiment(
    "The movie attempts to be surreal by incorporating time travel and various time paradoxes,"
    "but it's presented in such a ridiculous way it's seriously boring."))
'''
#s="<p>In a matter of weeks, the coronavirus has spiralled from a handful of cases in China to what many experts fear will become the next global pandemic. "
s = "Poland says the combination of a second wave of COVID-19 with flu season could create ""a lot of confusion"" because of their overlap in symptoms and put a heavy strain on the health care system. "


print(sentiment(s))
for chunk, polarity, subjectivity, label in sentiment(s).assessments:
    print(chunk, polarity, subjectivity, label)

from pattern.metrics import avg
a = sentiment(s).assessments
score1 = avg([p for chunk, p, s, label in a if label is None])
print(score1)

print(sentiment("fear"))
#print(wordnet.sentiwordnet["horrible"])
#'''