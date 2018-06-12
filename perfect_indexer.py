import json

with open('dataset/nfL6.json') as fp:
    questions = json.load(fp)

def perfect_answer(question):
    ret = [{'answer': answer, 'score': '0.5'} for answer in question['nbestanswers']]
    answers = [val['answer'] for val in ret]
    best_score = '0.1'
    try:
        ret[answers.index(question['answer'])]['score'] = best_score
    except ValueError:
        ret.append({'answer': question['answer'], 'score':best_score})
    return ret



perfect_dict = [{'id': question['id'], 'answers':perfect_answer(question)} for question in questions]

with open('perfect_results.json','w') as fp:
    json.dump(perfect_dict,fp,indent=4)
