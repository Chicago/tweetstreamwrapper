from whoosh.analysis import RegexTokenizer
from whoosh.analysis import LowercaseFilter
from whoosh.analysis import StopFilter

my_f = RegexTokenizer() | LowercaseFilter() | StopFilter()

print [token.text for token in my_f(u"This is a TEST of something I like to do for fun!")]
