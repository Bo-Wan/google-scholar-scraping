import html
import urllib.parse

o = 'Reliability and predictive validity of the Motivated Strategies for Learning Questionnaire (MSLQ)'

print(o)
p = urllib.parse.quote(o)
r = p.replace("%20", "+")


print(p)
print(r)
