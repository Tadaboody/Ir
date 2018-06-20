import json

import click

from product_team import load_index, train, Searcher,first_pass


@click.group()
def cli():
    pass

@cli.command("train")
@click.option('--restore/--dont_restore', default=True)
def train_cmd(restore):
    train(restore)


@cli.command("search")
@click.argument("queries_path")
def search(queries_path: str):
    index = load_index()
    searcher = Searcher(index)

    def gen_results():
        with open(queries_path) as opened_file:
            query = opened_file.readline()
        question_id = query.split()[0]
        question = query.split()[1:]
        yield {'id': question_id, 'answers': searcher.search(question, n=5)}

    answers = list(gen_results())
    with open('results.json', 'w') as opened_file:
        json.dump(answers, opened_file)

@cli.command('first_pass')
def first_pass_cmd():
    first_pass()

if __name__ == '__main__':
    cli()
