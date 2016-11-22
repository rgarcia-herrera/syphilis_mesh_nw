from pattern.vector import Document
import time
import datetime
from term_groups import groupterm
from term_groups import uninteresting_terms


class Year:

    def __init__(self, year):
        self.year = year
        self.refs = dict()

    def add_ref(self, pmid, kw_fq):
        self.refs[pmid] = kw_fq

    def get_keywords(self):
        kw = set()
        for pmid in self.refs:
            for w in self.refs[pmid].keys():
                kw.add(w)
        return kw

    def get_frequencies_for_kw(self, kw):
        freqs = list()
        for pmid in self.refs:
            freqs.append(self.refs[pmid].get(kw, 0))
        return freqs

    def get_normalized_kw_fq(self):
        kw_fq = dict()
        for kw in self.get_keywords():
            kw_fq[kw] = sum(self.get_frequencies_for_kw(kw)) \
                        / float(len(self.get_keywords()))
        return kw_fq


class Citation:
    def __init__(self, medline_record):

        self.record = medline_record

        # get citation date
        if 'EDAT' not in medline_record.keys():
            print medline_record.keys(), medline_record

        assert 'EDAT' in medline_record.keys()
        try:
            conv = time.strptime(medline_record['EDAT'], "%Y/%m/%d %H:%M")
            self.date = datetime.datetime(*conv[:6])  # entrez date
        except ValueError:
            conv = time.strptime(medline_record['EDAT'], "%Y/%m/%d")
            self.date = datetime.datetime(*conv[:6])  # entrez date

    def get_meshterms_fq(self):
        if 'MH' in self.record:
            # grab mesh terms
            mh = Document(self.record['MH'])
        elif 'OT' in self.record:
            mh = Document(self.record['OT'])
        else:
            return {}

        main_terms = list()
        other_terms = list()
        for term in mh:
            words = term.split('/')
            for w in words:
                if w not in uninteresting_terms:
                    if '*' in w:
                        term = w.replace('*', '')
                        main_terms.append(groupterm.get(term, term))
                    else:
                        other_terms.append(groupterm.get(w, w))
        total_terms = float(len(main_terms) + len(other_terms))
        main_terms_fq = dict()
        for term in main_terms:
            main_terms_fq[term] = (1 / total_terms) * 2
        other_terms_fq = dict()
        for term in other_terms:
            other_terms_fq[term] = 1 / total_terms

        # importance adjusted frequency total
        f = sum(main_terms_fq.values()) + sum(other_terms_fq.values())

        terms = {term: 0 for term in main_terms + other_terms}
        for term in main_terms:
            terms[term] += main_terms_fq[term] / f
        for term in other_terms:
            terms[term] += other_terms_fq[term] / f

        return terms


    def get_meshterms(self, flatten=True, group=True):
        if 'MH' not in self.record and 'OT' not in self.record:
            return list()

        mh = self.record.get('MH', list()) + self.record.get('OT', list())
        
        mesh_terms = list()
        for term in mh:
            term = term.replace('*', '')
            
            if flatten:
                words = term.split('/')
                for w in words:
                    if group:
                        w = groupterm.get(w, w)
                    mesh_terms.append(w)
            else:
                if group:
                    term = groupterm.get(term, term)
                mesh_terms.append(term)
                
        return mesh_terms

    
    def get_keywords(self):
        """ use pattern.Document to grab keywords from title or abstract """
        # if 'OT' not in self.record and 'MH' not in r:
        d = Document(self.record.get('TI',
                                     self.record.get('AB')))
        kw = dict()
        for w in d.keywords():
            try:
                # numbers are uninteresting
                # try to convert word to integer
                int(w[1])
            except ValueError:
                # only keep them if they fail
                kw[w[1]] = w[0]

        return kw



class Term:

    def __init__(self, term):
        self.term = term
        self.mentions_in_year = dict()

    def get_weight(self):
        return sum(self.mentions_in_year.values())

    def __repr__(self):
        return "<w=%s %s>" % (self.get_weight(), self.term)
