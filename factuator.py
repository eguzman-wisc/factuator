import argparse
import logging
import coloredlogs

import mwclient
import mwparserfromhell

import auth_store

parser = argparse.ArgumentParser(description='Automate the wiki.')
parser.add_argument('-v', '--verbose', action='count')
parser.add_argument('-s', '--study', help='Update study pages', action='store_true')
parser.add_argument('--selfreport', help='Update self report pages', action='store_true')
parser.add_argument('--selfreportlibrary', help='Update self report library', action='store_true')
parser.add_argument('--medialinks', help='Update File: to Media: links in given category', action='append')
parser.add_argument('-a', '--all', help='Run all known automated updates', action='store_true')
args = parser.parse_args()

if args.verbose:
    if args.verbose > 1:
        coloredlogs.install(level='DEBUG')
    elif args.verbose > 0:
        coloredlogs.install(level='INFO')
else:
    coloredlogs.install(level='WARN')

auth = auth_store.get_auth()
user = auth[0]

ua = 'factuator/0.1 run by User:' + user
mother = mwclient.Site(('https', 'wiki.keck.waisman.wisc.edu'), path='/wikis/mother/', httpauth=auth)

if args.all or args.study:
    import study
    study.run(mother)
elif args.all or args.selfreport:
    import selfreport
    selfreport.run(mother)
elif args.all or args.selfreportlibrary:
    import selfreportlibrary
    selfreportlibrary.run(mother)
elif args.medialinks:
    import medialinks
    medialinks.run(mother, args.medialinks)
else:
    parser.print_help()
