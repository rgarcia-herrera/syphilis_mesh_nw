# Syphilis Keyword Genesis and Development

So I read this fragment on Fleck's [Genesis and Development of a
Scientific Fact](http://www.evolocus.com/Textbooks/Fleck1979.pdf):

    It's as if we wanted to record in writing the natural course of an
    excited conversation among several persons all speaking
    simultaneously among themselves and each clamoring to make himself
    heard, yet which nevertheless permitted a consensus to
    crystallize. The continuity in time of the line of thought already
    mapped out must continually be interrupted to introduce other
    lines. The main line of development often must be held in abeyance
    to explicate connections. Moreover, a great deal has to be
    ommitted to preserve the idealized main line. Instead of a
    description of dynamic interactions, one is left with a more or
    less artificial scheme.

I immediately thought of this timeline:

<img src="http://imgs.xkcd.com/comics/congress.png" height="500px">

[source](https://xkcd.com/1127/)

## PubMed Mining

A [search for syphilis in
PubMed](https://www.ncbi.nlm.nih.gov/pubmed/?term=syphilis) yields 33,659
citations, spanning years 1817 to 2016.

[MeSH terms](https://www.nlm.nih.gov/mesh/meshhome.html) are extracted
from each citation, when they were available, or keywords are chosen
from the title or abstract using
[Pattern](http://www.clips.ua.ac.be/pages/pattern-vector), a natural
language processor.

Grouping these keywords per year creates a data structure that can be
plotted in a timeline like the one shown above.

This is pseudocode for the data structure:

1817

pmid123:
syph:0.5,
mercury:0.25
morals:0.25

pmid432:
syph:0.2
mercury:0.1
methods:07

...

1817
syph: [0.5, 0.2]
mercury: [0.25, 0.1]
morals: [0.25]
methos: [0.7]

(+ 0.5 0.2 0.25 0.1 0.25 0.7)
2.0



Scale, sum:

(/ 0.5 2)
0.25
(/ 0.2 2)
0.1
(/ 0.25 2)
0.125
(/ 0.1 2)
0.05
(/ 0.25 2)
0.125
(/ 0.7 2)
0.35


syph: [0.25, 0.1]
mercury: [0.125, 0.05]
morals: [0.125]
methods: [0.35]

sum
syph: (+ 0.25 0.1) 0.35
mercury: (+ 0.125 0.05) 0.175
morals: (+ 0.125) 0.125
methods: (+ 0.35) 0.35



## RiverPlot library

Checkout the API in [try_sql_river.py](try_sql_river.py). It's mostly
done, but there's room for improvement: labels, styles.

<img src="river.png">

