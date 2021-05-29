from nltk.collocations import *
import nltk
import Task


class ColocationFinder:
    def __init__(self, task: Task, n_best: int):
        self.N_best = n_best
        self.colocationFinder = {'1': '',
                                 '2': nltk.collocations.BigramCollocationFinder,
                                 '3': nltk.collocations.TrigramCollocationFinder}
        self.colocationMeasures = {'1': '',
                                   '2': nltk.collocations.BigramAssocMeasures(),
                                   '3': nltk.collocations.TrigramAssocMeasures()}
        self.all_text = ' '.join(task.res_tokenize_text).split()

    # TODO: Реалиовать эту штуку
    def unigramm(self):
        pass

    def get_colocation(self, typeC: int, freq_filter: int):
        f = self.colocationFinder[str(typeC)].from_words(self.all_text)
        f.apply_freq_filter(freq_filter)
        bm = self.colocationMeasures[str(typeC)]
        raw_freq_ranking = [' '.join(i) for i in f.nbest(bm.raw_freq, self.N_best)]

        tscore_ranking = [' '.join(i) for i in f.nbest(bm.student_t, self.N_best)]

        pmi_ranking = [' '.join(i) for i in f.nbest(bm.pmi, self.N_best)]

        llr_ranking = [' '.join(i) for i in f.nbest(bm.likelihood_ratio, self.N_best)]

        chi2_ranking = [' '.join(i) for i in f.nbest(bm.chi_sq, self.N_best)]

        return raw_freq_ranking, tscore_ranking, pmi_ranking, llr_ranking, chi2_ranking
