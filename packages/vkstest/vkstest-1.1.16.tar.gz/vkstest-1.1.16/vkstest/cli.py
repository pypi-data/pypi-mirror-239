import argparse

def get_word():
    parser = argparse.ArgumentParser(
        description='MW_CLI is a command line tool to get word definition using Merrian-webster API.\n Next Line', 
        add_help='This command line tool will help to get the description of passed words'
        )
    parser.add_argument(
        'word', 
        help='The word to get the definition from Merrian-Webster',
        )
    return parser.parse_args()


def main():
    import sys, json
    from vkstest import api
    args=get_word()
    if args.word:
        word=args.word
        api.getData(word)
    else:
        print(f'Enter a word to get its definition from Merrian-Websters')

if __name__ == '__main__':
    main()