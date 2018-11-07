import click
import bs4
import requests

url = 'http://quotes.cat-v.org/programming/'


@click.command()
def cli():
    response = requests.get(url)
    doc = bs4.BeautifulSoup(response.text, features='html5lib')

    main, = doc.select('#main-copy')

    quotes = []
    quote = []

    bad_chars = [
        ('\x80', ' '),
        ('\x94', ' '),
        ('\xa0', ' '),
        ('\xe2', '-'),
    ]

    for item in main:
        if item.name == 'p':
            text = ''.join(item.stripped_strings)
            for bad, good in bad_chars:
                text = text.replace(bad, good)
            text = text.strip()
            quote.append(text)
            continue

        if item.name == 'hr':
            quotes.append('\n\n'.join(quote) + '\n')
            quote = []
            continue

    print('\0'.join(quotes))


if __name__ == '__main__':
    cli()
