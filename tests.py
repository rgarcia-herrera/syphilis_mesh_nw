from timeline import Year
from timeline import Citation
from Bio import Medline

# test year class
y = Year(1817)
y.add_ref('pmid123', {'syphilis': 0.5,
                      'mercury': 0.25,
                      'morality': 0.25})
y.add_ref('pmid432', {'syphilis': 0.2,
                      'mercury': 0.1,
                      'methods': 0.7})
assert y.get_keywords() == {'mercury', 'methods', 'morality', 'syphilis'}


assert y.get_frequencies_for_kw('syphilis') == [0.5, 0.2]

assert y.get_normalized_kw_fq() == {'mercury': 0.0875, 'methods': 0.175,
                                    'morality': 0.0625, 'syphilis': 0.175}


# test citation class
records = Medline.parse(open('fixture.medline'))
for r in records:
    if r.get('PMID') == 27663926:
        c = Citation(r)
        assert c.get_keywords() == {u'tattoo': 0.5, u'tinea': 0.5}

    print c.get_meshterms()
