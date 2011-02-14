#!/usr/bin/python
# -*- encoding: utf-8 -*-

# TODOs:
# - defaults for non-supplied expansions:
#   template contains 

import ConfigParser
import logging
import optparse
import os
import re
import sys

# variable expansion:
# - %(dog)s --- normal python expansion
# - %(dog%)s --- no python expansion, leave as is (stripping the trailing %)
# - %(dog:cat) --- if there is an expansion for dog, dog will be used;
#                  otherwise if cat exists cat will be used
# - %(dog=cat) --- if there is an expansion for dog, dog will be used;
#                  otherwise "cat" will be used
# re_conf = re.compile(r'(?<!%)%\((?P<key>[^\(]+?)\)s')
re_conf = re.compile(r'(?P<verbatim>%?)%\((?P<key>[^+=:&\)]+?)' 
    + '(?:(?P<kind>[+=:&])(?P<default>[^\)]+))?\)(?P<type>s|d)')

def expand_variable(match, expansions, errors):
    key = match.group('key')
    kind = match.group('kind')
    default = match.group('default')
    typ = match.group('type')
    verbatim = match.group('verbatim')

    if verbatim:
        return match.group(0)[1:]

    # literal default
    if kind == '=':
        if key in expansions:
            return expansions[key]
        return default

    # variable default
    if kind == ':' and default in expansions:
        return expansions[default]

    if kind == '+' and default in expansions:
        if key in expansions:
            key = expansions[key]
        if typ == 's':
            return '%s%s' % (key, expansions[default])
        if typ == 'd':
            try:
                return str(int(key) + int(expansions[default]))
            except:
                pass

    if kind == '&' and default in expansions:
        if typ == 's':
            return '%s%s' % (key, expansions[default])
        if typ == 'd':
            try:
                return str(int(key) + int(expansions[default]))
            except:
                pass

    if key in expansions:
        return expansions[key]
        
    if not match.group(0) in errors:
        errors.append(match.group(0))

    return None

options = None

if __name__ == '__main__':

    # get config file
    parser = optparse.OptionParser()
    parser.add_option('-c', '--config', dest='config',
        help='config file', metavar='CONFIG')
    parser.add_option('-t', '--template', dest='template',
        help='template file', metavar='TEMPLATE')
    parser.add_option('-x', '--expandto', dest='expanded',
        help='expanded file', metavar='EXPANDED')
    parser.add_option('-e', '--echo', dest='echo',
        help='echo variable', metavar='ECHOVAR')

    (options, args) = parser.parse_args()

    if not options.config:
        parser.error('option --config|-c is required')
    if not os.path.exists(options.config):
        parser.error('config file "%s" does not exist' % options.config)
    if not options.echo:
        if not options.template:
            parser.error('option --template|-t is required')
        if not os.path.exists(options.template):
            parser.error('template file "%s" does not exist' \
                % options.template)
        if not options.expanded:
            parser.error('option --expandto|-e is required')

    logHandler = logging.StreamHandler()
    logHandler.setFormatter(logging.Formatter('%(asctime)s %(levelname)-8s '
        + ' %(message)s', '%a, %d %b %Y %H:%M:%S'))
    logging.getLogger().addHandler(logHandler)
    logging.getLogger().setLevel(logging.DEBUG)

    config = ConfigParser.RawConfigParser()
    config.readfp(open(options.config, 'r'))

    if not config.has_section('openlp'):
        logging.error('[expander] %s: config file "%s" lacks an [openlp] '
            + 'section', options.template, options.config)

    expansions = dict()
    for k in config.options('openlp'):
        expansions[k] = config.get('openlp', k)

    # commandline overrides?
    for override in args:
        if not '=' in override:
            continue
        
        (k, v) = override.split('=', 2)
        expansions[k] = v

    if options.echo:
        if options.echo in expansions:
            print expansions[options.echo]
            sys.exit(0)
        else:
            sys.exit(1)

    # closure to capture expansions and errors variable
    errors = []
    expanded = []
    
    try:
        # try to expand the template
        line = 0
        faulty = False

        template = open(options.template, 'r')
        raw = template.readlines()
        template.close()

        def _expand(m):
            return expand_variable(m, expansions = expansions, errors = errors)
    
        for l in raw:
            line += 1
            exp = re_conf.sub(_expand, l)
            if errors:
                for key in errors:
                    logging.error('[expander] %s: line %d: could not expand '
                        + 'key "%s"', options.template, line, key)
                faulty = True
                errors = []
            else:
                expanded.append(exp)

        if faulty:
            sys.exit(1)

        # successfully expanded template, now backup potentially existing
        # target file
        targetFile = options.expanded % expansions
        if os.path.exists(targetFile):
            if os.path.exists('%s~' % targetFile):
                os.unlink('%s~' % targetFile)
            os.rename(options.expanded, '%s~' % targetFile)
            logging.info('[expander] %s: backed up existing target file "%s" '
                 + 'to "%s"', options.template, targetFile,
                 '%s~' % options.expanded)

        # make sure that target directory exists
        targetDir = os.path.dirname(targetFile)
        if not os.path.exists(targetDir):
            os.makedirs(targetDir)

        # write target file
        try:
            target = open(targetFile, 'w')
            for exp in expanded:
                target.write(exp)
            target.close()
        except Exception, e:
            logging.error('[expander] %s: could not expand to "%s"',
                options.template, options.expaned, e)

        # copy over file access mode from template
        mode = os.stat(options.template)
        os.chmod(options.expanded, mode.st_mode)

        logging.info('[expander] expanded "%s" to "%s"',
                     options.template, options.expanded)
    
    except:
        pass

