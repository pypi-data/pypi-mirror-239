# Introduction
Multimatcher is an implementation of the Aho-Corasick (Aho & Corasick 1975) search algorithm.
It efficiently finds multiple keywords in an input string, without having to loop
over the input string multiple times.

The rationale behind the Multimatcher is that most often we want to do something with the found matches, and
the Multimatcher provides a flexible "replace" method that allows different use cases such as:

- find and delete
- find and replace
- tag with a global label (i.e. all matches get the same label)
- tag with custom label (i.e. each match gets its own label)
- count matches

When possible, it's recommended to set whole_words_only to True, which makes matching significantly faster.

# Examples
## Find and delete matches
```
from multimatcher import Multimatcher
mm = Multimatcher(separator=' ')
mm.set_replacement_text("") # matches will be deleted
mm.set_search_patterns(['a', 'b', 'c'])
mm.replace("x a y b z c") # produces "x y z"
```
## Find and transform matches
```
from multimatcher import Multimatcher
mm = Multimatcher(separator=' ')
mm.set_replacement_method(lambda x: x.capitalize()) # matches will be capitalized
mm.set_search_patterns(['a', 'b', 'c'])
mm.replace("x a y b z c") # produces "x A y B z C"
```
## Find and replace matches with the same label
```
from multimatcher import Multimatcher
mm = Multimatcher(separator=' ')
mm.set_replacement_text("0") # all matches will be replaced with 0
mm.set_search_patterns(['a', 'b', 'c'])
mm.replace("x a y b z c") # produces "x 0 y 0 z 0"
```
## Find and replace matches with custom labels
```
from multimatcher import Multimatcher
mm = Multimatcher(separator=' ')
mm.set_replacement_map({"a": "1", "b": "2", "c": "3"}) # replaces a > 1, b > 2, c > 3
mm.set_search_patterns(['a', 'b', 'c'])
mm.replace("x a y b z c") # produces "x 1 y 2 z 3"
```

## Find and replace matches with custom labels
```
from multimatcher import Multimatcher
mm = Multimatcher(separator='')
mm.set_search_patterns(['a', 'b', 'c'])
mm.count("aa xx bb yy cc zz") # produces {'a': 2, 'b': 2, 'c': 2}
```
# References
Aho, A. V., & Corasick, M. J. (1975). Efficient string matching: an aid to bibliographic search.
Communications of the ACM, 18(6), 333-340.
