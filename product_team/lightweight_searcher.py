import json
from product_team import EnglishAnalyzer, load_index
from product_team.utils import memorize,s_dump,s_load,stream_memorize
from tqdm import tqdm
from itertools import islice
import numpy as np


def first_pass(dataset_path="dataset/nfL6.json"):
    analyzer = EnglishAnalyzer()
    with open(dataset_path) as fp:
        dataset = json.load(fp)

    def all_answers():
        for question in dataset:
            yield from question['nbestanswers']
    
    index = load_index()
    def filtered_tokenized_pairs():
        for i,answer in enumerate(tqdm(list(all_answers()))):
            tokenized_answer = index.process_for_train(answer)
            if tokenized_answer is not None:
                yield i, tokenized_answer
    
    gen = filtered_tokenized_pairs()
    batch_size = len(list(all_answers()))//200
    batches = np.array(list((gen)))
    print(batches.shape)
    exit()
    for batch in islice(gen, batch_size):
        print(np.array(batch).shape)
