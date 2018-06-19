import json

import click

from product_team import load_index,train


@click.group()
def cli():
    pass

@cli.command("train")
@click.option('--restore/--dont_restore', default=True)
def train_cmd(restore):
    train(restore)



@cli.command
@click.argument("queries_path")
def search(queries_path: str):
    index = load_index()

    def gen_results():
        with open(queries_path) as opened_file:
            query = opened_file.readline()
        question_id = query.split()[0]
        question = query.split()[1:]
        yield {'id': question_id, 'answers': index.search(question)}

    answers = list(gen_results())
    with open('results.json', 'w') as opened_file:
        json.dump(answers, opened_file)


if __name__ == '__main__':
    cli()
