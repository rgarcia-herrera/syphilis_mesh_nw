from timeline import Year

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
