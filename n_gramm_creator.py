import pandas as pd
from textblob import TextBlob
import Task
import matplotlib
from pylab import rcParams

rcParams['figure.figsize'] = 8, 5
matplotlib.use('Agg')


class Ngram:
    def __init__(self, task: Task, *args):
        self.task = task
        self.n_grams_size = args
        self.dataframes = [{} for _ in self.n_grams_size]

    def create_dataframe(self):
        for sentence in self.task.res_tokenize_text:
            ngram_object = TextBlob(sentence)
            for index, n_size in enumerate(self.n_grams_size):
                ngrams = ngram_object.ngrams(n=n_size)
                for ngram in ngrams:
                    ngram_text = (' '.join(ngram)).lower()
                    if ngram_text in self.dataframes[index].keys():
                        self.dataframes[index][ngram_text] += 1
                    else:
                        self.dataframes[index][ngram_text] = 1

        # res = []
        # for size in self.n_grams_size:
        #     data = {'ngram': self.dataframes[size-1].keys(), 'count': self.dataframes[size-1].values()}
        #     res.append(pd.DataFrame(data=data))
        # return res

    def save_fig(self, user_id):
        res = []
        for index, dataframes in enumerate(self.dataframes):
            data = {'ngram': dataframes.keys(), 'count': dataframes.values()}
            df = pd.DataFrame(data=data)
            df = df.sort_values('count', ascending=False)
            try:
                plot = df[df['count'] >= 150].plot(kind='bar', x="ngram", y="count", rot=20)
            except:
                plot = df[df['count'] >= 100].plot(kind='bar', x="ngram", y="count", rot=20)
            fig = plot.get_figure()
            res.append(f'{user_id}_{index}.png')
            fig.savefig(f'{user_id}_{index}.png')
        return res
