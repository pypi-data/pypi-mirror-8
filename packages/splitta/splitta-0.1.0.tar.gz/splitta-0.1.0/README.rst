Improved Sentence Boundary Detection
====================================

Overview
--------

Consider the following text:

"On Jan. 20, former Sen. Barack Obama became the 44th President of the
U.S. Millions attended the Inauguration."

The periods are potentially ambiguous, signifying either the end of a
sentence, an abbreviation, or both. The sentence boundary detection
(SBD) task involves disambiguating the periods, and in particular,
classifying each period as end-of-sentence () or not. In the example,
only the period at the end of U.S. should be classified as :

"On Jan. 20, former Sen. Barack Obama became the 44th President of the
U.S. Millions attended the Inauguration."

Chances are, if you are using some SBD system, it has an error rate of
1%-3% on English newswire text. The system described here achieves the
best known error rate on the Wall Street Journal corpus: 0.25% and
comparable error rates on the Brown corpus (mixed genre) and other test
corpora.

Background
----------

SBD is fundamental to many natural language processing problems, but
only a few papers describe solutions. A variety of rule-based systems
are floating around, and a few semi-statistical systems are available if
you know where to look. The most widely cited are:

-  Alembic (Aberdeen, et al. 1995): Abbreviation list and ~100
   hand-crafted regular expressions.
-  Satz (Palmer & Hearst at Berkeley, 1997): Part of speech features and
   abbreviation lists as input to a classifier (neural nets and decision
   trees have similar performance).
-  mxTerminator (Reynar & Ratnaparkhi, 1997): Maximum entropy
   classification with simple lexical features.
-  Mikheev (Mikheev, 2002): Observes that perfect labels for
   abbreviations and names gives almost perfect SBD results. Creates
   heuristics for marking these, unsupervised, from held-out data.
-  Punkt (Strunk and Kiss, 2006): Unsupervised method uses heuristics to
   identify abbreviations and sentence starters.

I have not been able to find publicly available copies of any of these
systems, with the exception of Punkt, which ships with NLTK.
Nonetheless, here are some error rates reported on what I believe to be
the same subset of the WSJ corpus (sections 03-16).

-  Alembic: 0.9%
-  Satz: 1.5%; 1.0% with extra hand-written lists of abbreviations and
   non-names.
-  mxTerminator: 2.0%; 1.2% with extra abbreviation list.
-  Mikheev: 1.4%; 0.45% with abbreviation list (assembled automatically
   but carefully tuned; test-set-dependent parameters are a concern)
-  Punkt: 1.65% (Though if you use the model that ships with NLTK,
   you'll get over 3%)

All of these systems use lists of abbreviations in some capacity, which
I think is a mistake. Some abbreviations almost never end a sentence
(Mr.), which makes list-building appealing. But many abbreviations are
more ambiguous (U.S., U.N.), which complicates the decision.

--------------

While 1%-3% is a low error rate, this is often not good enough. In
automatic document summarization, for example, including a sentence
fragment usually renders the resulting summary unintelligible. With
10-sentence summaries, 1 in 10 is ruined by an SBD system with 99%
accuracy. Improving the accuracy to 99.75%, only 1 in 40 is ruined.
Improved sentence boundary detection is also likely to help with
language modeling and text alignment.

--------------

I built a supervised system that classifies sentence boundaries without
any heuristics or hand-generated lists. It uses the same training data
as mxTerminator, and allows for Naive Bayes or SVM models (SVM Light).

+-------------------------------------+---------+---------------+
| Corpus                              | SVM     | Naive Bayes   |
+=====================================+=========+===============+
| WSJ                                 | 0.25%   | 0.35%         |
+-------------------------------------+---------+---------------+
| Brown                               | 0.36%   | 0.45%         |
+-------------------------------------+---------+---------------+
| Complete Works of Edgar Allen Poe   | 0.52%   | 0.44          |
+-------------------------------------+---------+---------------+

I've packaged this code, written in Python, for general use. Word-level
tokenization, which is particularly important for good sentence boundary
detection, is included.

Note that the included models use all of the labeled data listed here,
meaning that the expected results are somewhat better than the numbers
reported above. Including the Brown data as training improves the WSJ
result to 0.22% and the Poe result to 0.37 (using the SVM).

Performance
-----------

A few other notes on performance. The standard WSJ test corpus includes
26977 possible sentence boundaries. About 70% are in fact sentence
boundaries. Classification with the included SVM model will give 59
errors. Of these, 24 (41%) involve the word "U.S.", a particularly
interesting case. In training, "U.S." appears 2029 times, and 90 of
these are sentence boundaries. Further complicating the situation,
"U.S." often appears in a context like "U.S. Security Council" or "U.S.
Government", and either "Security" or "Government" are viable sentence
starters.

Other confusing cases include "U.N.", "U.K.", and state abbreviations
like "N.Y." which have similar characteristics as "U.S." but appear
somewhat less frequently.

Setup
-----

See SETUP.md for setup instructions and notes.
