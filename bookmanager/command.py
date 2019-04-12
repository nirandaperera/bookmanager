"""bookmanager -- a helper to create books from mardown files in a yaml TOC.

Usage:
  bookmanager url check [YAML] [--format=FORMAT]
  bookmanager url list [YAML] [--format=FORMAT]
  bookmanager list [YAML] [--format=FORMAT]
  bookmanager info


Arguments:
  YAML   the yaml file

Options:
  -h --help
  -f, --format=FORMAT     [default: markdown]

Description:

    TBD

"""
from bookmanager.config import Config
from cloudmesh.DEBUG import VERBOSE
from cloudmesh.common.util import banner
from cloudmesh.shell.command import map_parameters
from cloudmesh.common.dotdict import dotdict
from docopt import docopt
from pprint import pprint
from bookmanager.util import download

import requests

debug = False

def main():
    arguments = dotdict(docopt(__doc__))
    arguments["FORMAT"] = arguments["--format"]

    pprint(arguments)

    config = Config(config=arguments.YAML)


    if arguments.info:

        pprint(config.book)
        pprint(config.variables)

    elif arguments.list and (arguments.FORMAT in ["md", "markdown"]):

        banner("MARDOWN")

        result = \
            config.flatten(
                book="My Book",
                title="- {book}",
                section="{indent}- [ ] [{topic}]({url}) {level}",
                header="{indent}- [ ] {topic} {level}",
                indent="  "
            )

        print(config.output(result, kind="text"))

    elif arguments.list and (arguments.FORMAT in ["list"]):

        banner("LITS LIST")

        result = \
            config.flatten(
                book="My Book",
                title="- {book}",
                section="{indent}- [ ] [{topic}]({url}) {level}",
                header="{indent}- [ ] {topic} {level}",
                indent="  "
            )

        print(config.output(result, kind="list"))

    elif arguments.url and arguments.check:

        result = \
            config.flatten(
                book="",
                title="",
                section="{url}",
                header="",
                indent=""
            )

        for entry in result:
            url = entry["url"]
            if url.startswith("http"):
                print(url, end="")
                response = requests.get(url)
                if response.status_code < 400:
                    print (" -> ok")
                else:
                    print("error", response.status_code)

    elif arguments.url and arguments.download:

        result = \
            config.flatten(
                book="",
                title="",
                section="{url}",
                header="",
                indent=""
            )

        for entry in result:
            url = entry["url"]
            path = "./dist/{path}".format(**entry)
            if url.startswith("http"):
                download(url, path)


    elif arguments.url and arguments.list:

        banner("URL")

        if arguments.FORMAT in ["md", "markdown"]:
            kind = "text"
        else:
            kind = "list"


        result = \
            config.flatten(
                book="",
                title="",
                section="{url}",
                header="",
                indent=""
            )

        print (result)

        print('\n'.join(config.output(result, kind="url")))




if __name__ == '__main__':
    main()
