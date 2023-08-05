# -*- coding: utf-8 -*-
"""
Commande en ligne pour lister la carte de toute les urls
"""
import datetime
from optparse import OptionValueError, make_option

from Sveetchies.utils import startswith_in_list
from Sveetchies.cli.termcolors import colorize

from django.conf import settings
from django.core.management.base import CommandError, BaseCommand
from django.core.urlresolvers import RegexURLResolver

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("--exclude", dest="excluded_paths", action="append", help="Excludes paths, append each excluded path with this option"),
    )
    help = "Command to list url map"

    def handle(self, *args, **options):
        if len(args) != 0:
            raise CommandError("Command doesn't accept any arguments")
        
        self.excluded_paths = options.get('excluded_paths')
        if not self.excluded_paths:
            self.excluded_paths = []
        self.verbosity = int(options.get('verbosity'))

        # Parcours des urls depuis la racine
        urlconf = settings.ROOT_URLCONF
        rootresolver = RegexURLResolver(r'^/', urlconf)
        self._walk_urlresolver("/", rootresolver)
    
    def _walk_urlresolver(self, parent, urlresolver, lv=0):
        for item in urlresolver.url_patterns:
            current_path = parent + self._clear_regexpath(item.regex.pattern)
            if startswith_in_list(current_path, self.excluded_paths):
                continue
            if not isinstance(item, RegexURLResolver):
                print "{indent}* {path} {name}".format(indent=("  "*lv), path=colorize(current_path, fg='green'), name=colorize(item.name, fg='magenta'))
            else:
                print "{indent}* {path}".format(indent=("  "*lv), path=colorize(current_path, fg='blue'))
                self._walk_urlresolver(current_path, item, lv=lv+1)
    
    def _clear_regexpath(self, regex):
        path = regex
        if path.startswith('^'):
            path = path[1:]
        if path.endswith('$'):
            path = path[:-1]
        return path
