# -*- coding: utf-8 -*-
'''Determine whether a client matches a specification (beta)

Usage:
    exo [options] spec <cik> <spec-yaml> [--ids=<id1,id2,idN>] [--portal|--domain] [-f]
    exo [options] spec <cik> --generate=<filename> [--scripts=<dir>] [--asrid]
    exo [options] spec --example

The --generate form creates spec YAML and scripts from a CIK.

Command options:
    --update-scripts  Update any scripts that do not match what's
                      on the filesystem
    --create          Create any resources that do not exist
    --asrid           When generating a spec, do not convert RIDs into aliases.
    --ids substitutes values for <% id %> when matching alias
    --example         Show an annotated example spec YAML file
    --portal          Will apply the spec command to all devices in a portal
                      that match the vendor/model in the given spec file
    --domain          Will apply the spec command to all devices, in all of the
                      portals under the given domain, that match the vendor/model
                      in the given spec file
    -f                Used with the `--portal` or `--domain flag to override the
                      prompt when updating multiple devices.
    --no-diff         Do not show diff output on scripts.
'''

from __future__ import unicode_literals
import re
import os
import json
from pprint import pprint
import sys
import pyonep
import ast

import yaml
import jsonschema
import six
from six import iteritems


class Spec401Exception(BaseException):
    # Used when a 401 is caught during a spec
    pass


class Plugin():
    def command(self):
        return 'spec'
    def run(self, cmd, args, options):
        if args['--example']:
            s = '''
# Example client specification file
# Specification files are in YAML format (a superset of JSON
# with more readable syntax and support for comments) and
# look like this. They may contain comments that begin
# with a # sign.

# Device client model information
device:
    model: "myModel"
    vendor: "myVendor"

# list of dataports that must exist
dataports:
      # this the absolute minimum needed to specify a
      # dataport.
    - alias: mystring
      # names are created, but not compared
    - name: Temperature
      # aliases, type, and format are created
      # and compared
      alias: temp
      format: float
      unit: °F
    - name: LED Control
      alias: led6
      format: integer
    - alias: config
      # format should be string, and parseable JSON
      format: string/json
      # initial value (if no other value is read back)
      initial: '{"text": "555-555-1234", "email": "jeff@555.com"}'
    - alias: person
      format: string/json
      # JSON schema specified inline (http://json-schema.org/)
      # format must be string/json to do validate
      # you may also specify a string to reference schema in an
      # external file. E.g. jsonschema: personschema.json
      jsonschema: {"title": "Person Schema",
                   "type": "object",
                   "properties": {"name": {"type": "string"}},
                   "required": ["name"]}
      initial: '{"name":"John Doe"}'
    - alias: place
      # An description of the dataport.
      description: 'This is a place I have been'
      # Dataport are private by default,
      # but if you want to share one with the world
      public: true

    # any dataports not listed but found in the client
    # are ignored. The spec command does not delete things.

# list of script datarules that must exist
scripts:
    # by default, scripts are datarules with
    # names and aliases set to the file name
    - file: test/files/helloworld.lua
    # you can also set them explicitly
    - file: test/files/convert.lua
      # if <% id %> is embedded in aliases
      # or script content, the --ids parameter must
      # be passed in. The spec command then expects
      # a script or dataport resource per id passed, substituting
      # each ID for <% id %>. In this example, if the command was:
      #
      # $ exo spec mysensor sensorspec.yaml --ids=A,B
      #
      # ...then the spec command looks for *two* script datarules
      # in mysensor, with aliases convertA.lua and convertB.lua.
      # Additionally, any instances of <% id %> in the content of
      # convert.lua are substituted with A and B before being
      # written to each script datarule.
      #
      alias: convert<% id %>.lua
'''
            if not six.PY3:
                s = s.encode('utf-8')
            print(s)
            return


        input_cik = options['cik']
        rpc = options['rpc']
        ExoException = options['exception']
        asrid = args['--asrid']

        if cmd == 'spec':

            if args['--generate'] is not None:
                spec_file = args['--generate']
                if args['--scripts'] is not None:
                    script_dir = args['--scripts']
                else:
                    script_dir = 'scripts'
                print('Generating spec for {0}.'.format(input_cik))
                print('spec file: {0}, scripts directory: {1}'.format(spec_file, script_dir))

                # generate spec file, download scripts
                spec = {}
                info, listing = rpc._exomult(input_cik,
                    [['info', {'alias': ''}, {'basic': True,
                                              'description': True,
                                              'aliases': True}],
                     ['listing', ['dataport', 'datarule', 'dispatch'], {}]])
                rids = listing['dataport'] + listing['datarule']

                if len(rids) > 0:
                    child_info = rpc._exomult(input_cik, [['info', rid, {'basic': True, 'description': True}] for rid in rids])
                    for idx, rid in enumerate(rids):
                        myinfo = child_info[idx]
                        name = myinfo['description']['name']
                        def skip_msg(msg):
                            print('Skipping {0} (name: {1}). {2}'.format(rid, name, msg))
                        if rid not in info['aliases']:
                            skip_msg('It needs an alias.')
                            continue
                        typ = myinfo['basic']['type']
                        if typ == 'dataport':
                            dp = {'name': myinfo['description']['name'],
                                  'alias': info['aliases'][rid][0],
                                  'format': myinfo['description']['format']
                                  }

                            preprocess = myinfo['description']['preprocess']
                            if preprocess is not None and len(preprocess) > 0:
                                def toAlias(pair):
                                    if not asrid and pair[1] in info['aliases']:
                                        return [pair[0], info['aliases'][pair[1]][0]]
                                    else:
                                        return pair
                                dp['preprocess'] = [toAlias(x) for x in preprocess]


                            subscribe = myinfo['description']['subscribe']
                            if subscribe is not None and subscribe is not "":
                                if not asrid and subscribe in info['aliases']:
                                    dp['subscribe'] = info['aliases'][subscribe][0]
                                else:
                                    dp['subscribe'] = subscribe

                            retention = myinfo['description']['retention']
                            if retention is not None:
                                count = retention['count']
                                duration = retention['duration']
                                if count is not None and duration is not None:
                                    if count == 'infinity':
                                        del retention['count']
                                    if duration == 'infinity':
                                        del retention['duration']
                                    if len(retention) > 0:
                                        dp['retention'] = retention

                            meta_string = myinfo['description']['meta']
                            try:
                                meta = json.loads(meta_string)
                                unit = meta['datasource']['unit']
                                if len(unit) > 0:
                                    dp['unit'] = unit
                                desc = meta['datasource']['description']
                                if len(desc) > 0:
                                    dp['description'] = desc
                            except:
                                # assume unit is not present in metadata
                                pass
                            spec.setdefault('dataports', []).append(dp)
                            
                            public = myinfo['description']['public']
                            if public is not None and public:
                                dp['public'] = public


                        elif typ == 'datarule':
                            desc = myinfo['description']
                            is_script = desc['format'] == 'string' and 'rule' in desc and 'script' in desc['rule']
                            if not is_script:
                                skip_msg('Datarules that are not scripts are not supported.')
                                continue
                            filename = os.path.join(script_dir, info['aliases'][rid][0])
                            spec.setdefault('scripts', []).append({'file': filename})
                            with open(filename, 'w') as f:
                                print('Writing {0}...'.format(filename))
                                f.write(desc['rule']['script'])
                        elif typ == 'dispatch':
                            skip_msg('dispatch type is not yet supported by spec command.')
                            continue

                with open(spec_file, 'w') as f:
                    print('Writing {0}...'.format(spec_file))
                    yaml.safe_dump(spec, f, encoding='utf-8', indent=4, default_flow_style=False, allow_unicode=True)
                return

            updatescripts = args['--update-scripts']
            create = args['--create']

            def query_yes_no(question, default="yes"):
                """Ask a yes/no question via raw_input() and return their answer.

                "question" is a string that is presented to the user.
                "default" is the presumed answer if the user just hits <Enter>.
                    It must be "yes" (the default), "no" or None (meaning
                    an answer is required of the user).

                The "answer" return value is one of "yes" or "no".
                """
                valid = {"yes":True,   "y":True,  "ye":True,
                         "no":False,     "n":False}
                if default == None:
                    prompt = " [y/n] "
                elif default == "yes":
                    prompt = " [Y/n] "
                elif default == "no":
                    prompt = " [y/N] "
                else:
                    raise ValueError("invalid default answer: '%s'" % default)

                while True:
                    sys.stdout.write(question + prompt)
                    choice = raw_input().lower()
                    if default is not None and choice == '':
                        return valid[default]
                    elif choice in valid:
                        return valid[choice]
                    else:
                        sys.stdout.write("Please respond with 'yes' or 'no' "\
                                         "(or 'y' or 'n').\n")

            def generate_aliases_and_data(res, args):
                ids = args['--ids']
                if 'alias' in res:
                    alias = res['alias']
                else:
                    if 'file' in res:
                        alias = os.path.basename(res['file'])
                    else:
                        raise ExoException('Resources in spec must have an alias.')

                if reid.search(alias) is None:
                    yield alias, None
                else:
                    alias_template = alias
                    if ids is None:
                        raise ExoException('This spec requires --ids')
                    ids = ids.split(',')
                    for id, alias in [(id, reid.sub(id, alias_template)) for id in ids]:
                        yield alias, {'id': id}

            reid = re.compile('<% *id *%>')

            def infoval(input_cik, alias):
                '''Get info and latest value for a resource'''
                return rpc._exomult(
                    input_cik,
                    [['info', {'alias': alias}, {'description': True, 'basic': True}],
                    ['read', {'alias': alias}, {'limit': 1}]])


            with open(args['<spec-yaml>']) as f:
                spec = yaml.safe_load(f)

            ciks = []
            portal_ciks = []

            iterate_portals = False

            if args['--portal'] == True:
                portal_ciks.append((input_cik,''))
                iterate_portals = True

            if args['--domain'] == True:
                #set iterate_portals flag to true so we can interate over each portal
                iterate_portals = True
                # Get list of users under a domain
                user_keys = []
                clients = rpc._listing_with_info(input_cik,['client'])

                email_regex = re.compile(r'[^@]+@[^@]+\.[^@]+')

                for k,v in clients['client'].items():
                    name = v['description']['name']
                    # if name is an email address
                    if email_regex.match(name):
                        user_keys.append(v['key'])


                # Get list of each portal
                for key in user_keys:
                    userlisting = rpc._listing_with_info(key,['client'])
                    for k,v in userlisting['client'].items():
                        portal_ciks.append((v['key'],v['description']['name']))
                    #print(x)


            if iterate_portals == True:
                for portal_cik, portal_name in portal_ciks:
                    # If user passed in the portal flag, but the spec doesn't have
                    # a vendor/model, exit
                    if (not 'device' in spec) or (not 'model' in spec['device']) or (not 'vendor' in spec['device']):
                        print("With --portal (or --domain) option, spec file requires a\r\n"
                              "device model and vendor field:\r\n"
                              "e.g.\r\n"
                              "device:\r\n"
                              "    model: modelName\r\n"
                              "    vendor: vendorName\r\n")
                        raise ExoException('--portal flag requires a device model/vendor in spec file')
                    else:

                        # get device vendor and model
                        modelName = spec['device']['model']
                        vendorName = spec['device']['vendor']

                        # If the portal has no name, use the cik as the name
                        if portal_name == '':
                            portal_name = portal_cik
                        print('Looking in ' + portal_name + " for " + modelName + "/" + vendorName)
                        # Get all clients in the portal
                        clients = rpc._listing_with_info(portal_cik, ['client'])
                        #print(modelName)
                        # for each client
                        for k,v in iteritems(list(iteritems(clients))[0][1]):
                            # Get meta field
                            validJson = False
                            meta = None
                            try:
                                meta = json.loads(v['description']['meta'])
                                validJson = True
                            except ValueError as e:
                                # no json in this meat field
                                validJson = False
                            if validJson == True:
                                # get device type (only vendor types have a model and vendor
                                type = meta['device']['type']

                                # if the device type is 'vendor'
                                if type == 'vendor':
                                    # and it matches our vendor/model in the spec file
                                    if meta['device']['vendor'] == vendorName:
                                        if meta['device']['model'] == modelName:
                                            # Append the cik to our list
                                            ciks.append(v['key'])
                                            print("  found: " + v['description']['name'] + " " + v['key'] )
            else:
                # only for single client
                ciks.append(input_cik)

            # Make sure user knows they are about to update multiple devices
            # unless the `-f` flag is passed
            if ((args['--portal'] or args['--domain']) and args['--create']) and not args['-f']:
                res = query_yes_no("You are about to update " + str(len(ciks)) + " devices, are you sure?")
                if res == False:
                    print('exiting')
                    return

            # for each device in our list of ciks
            for cik in ciks:
                try:
                    aliases = {}
                    print("Running spec on: " + cik)
                    #   apply spec [--create]

                    # Get map of aliases
                    info = rpc.info(cik, {'alias': ''}, {'aliases': True})
                    try:
                        for rid, alist in info['aliases'].items():
                            for alias in alist:
                                aliases[alias] = rid
                    except:
                        pass

                    for typ in ['dataport', 'client', 'script']:
                        if typ + 's' in spec:
                            for res in spec[typ + 's']:
                                for alias, resource_data in generate_aliases_and_data(res, args):
                                    # TODO: handle nonexistence
                                    exists = True
                                    try:
                                        info, val = infoval(cik, alias)
                                    except rpc.RPCException as e:
                                        exists = False
                                        print('{0} not found.'.format(alias))
                                        if not create:
                                            print('Pass --create to create it')
                                            continue
                                    except pyonep.exceptions.OnePlatformException as ex:
                                        exc = ast.literal_eval(ex.message)

                                        if exc['code'] == 401:
                                            raise Spec401Exception()
                                        else:
                                            raise ex

                                    # TODO: use templating library
                                    def template(script):
                                        if resource_data is None:
                                            return script
                                        else:
                                            return reid.sub(resource_data['id'], script)

                                    if typ == 'client':
                                        if not exists:
                                            if create:
                                                print('Client creation is not yet supported')
                                            continue
                                    elif typ == 'dataport':
                                        format = res['format'] if 'format' in res else 'string'
                                        pieces = format.split('/')
                                        if len(pieces) > 1:
                                            format = pieces[0]
                                            format_content = pieces[1]
                                        else:
                                            format_content = None
                                        name = res['name'] if 'name' in res else alias
                                        if not exists and create:
                                            print('Creating dataport with name: {0}, alias: {1}, format: {2}'.format(
                                                name, alias, format))
                                            rid = rpc.create_dataport(cik, format, name=name)
                                            rpc.map(cik, rid, alias)
                                            info, val = infoval(cik, alias)
                                            aliases[alias] = rid

                                        # check type
                                        if info['basic']['type'] != typ:
                                            raise ExoException('{0} is a {1} but should be a {2}.'.format(alias, info['basic']['type'], typ))

                                        # check format
                                        if format != info['description']['format']:
                                            raise ExoException(
                                                '{0} is a {1} but should be a {2}.'.format(
                                                alias, info['description']['format'], format))

                                        # check initial value
                                        if 'initial' in res and len(val) == 0:
                                            if create:
                                                initialValue = template(res['initial'])
                                                print('Writing initial value {0}'.format(initialValue))
                                                rpc.write(cik, {'alias': alias}, initialValue)
                                                # update values being validated
                                                info, val = infoval(cik, alias)
                                            else:
                                                print('Required initial value not found in {0}. Pass --create to write initial value.'.format(alias))

                                        # check format content (e.g. json)
                                        if format_content == 'json':
                                            if format != 'string':
                                                raise ExoException(
                                                    'Invalid spec for {0}. json content type only applies to string, not {1}.'.format(alias, format));
                                            if len(val) == 0:
                                                print('Spec requires {0} be in JSON format, but it is empty.'.format(alias))
                                            else:
                                                obj = None
                                                try:
                                                    obj = json.loads(val[0][1])
                                                except:
                                                    print('Spec requires {0} be in JSON format, but it does not parse as JSON. Value: {1}'.format(
                                                        alias,
                                                        val[0][1]))

                                                if obj is not None and 'jsonschema' in res:
                                                    schema = res['jsonschema']
                                                    if isinstance(schema, six.string_types):
                                                        schema = json.loads(open(schema).read())
                                                    try:
                                                        jsonschema.validate(obj, schema)
                                                    except Exception as ex:
                                                        print("{0} failed jsonschema validation.".format(alias))
                                                        print(ex)

                                        elif format_content is not None:
                                            raise ExoException(
                                                'Invalid spec for {0}. Unrecognized format content {1}'.format(alias, format_content))

                                        # check unit
                                        if 'unit' in res or 'description' in res:
                                            meta_string = info['description']['meta']
                                            try:
                                                meta = json.loads(meta_string)
                                            except:
                                                meta = None

                                            def bad_desc_msg(s):
                                                sys.stdout.write('spec expects description for {0} to be {1}, but they are not.'.format(alias, res['description']))
                                            def bad_unit_msg(s):
                                                sys.stdout.write('spec expects unit for {0} to be {1}, but they are not.'.format(alias, res['unit']))

                                            if create:
                                                if meta is None:
                                                    meta = {'datasource':{'description':'','unit':''}}
                                                if 'datasource' not in meta:
                                                    meta['datasource'] = {'description':'','unit':''}
                                                if 'unit' in res:
                                                    meta['datasource']['unit'] = res['unit']
                                                if 'description:' in res:
                                                    meta['datasource']['description'] = res['description']

                                                new_desc = info['description'].copy()
                                                new_desc['meta'] = json.dumps(meta)
                                                rpc.update(cik, {'alias': alias}, new_desc)

                                            else:
                                                if meta is None:
                                                    sys.stdout.write('spec expects metadata but found has no metadata at all. Pass --create to write metadata.')
                                                elif 'datasource' not in meta:
                                                    sys.stdout.write('spec expects datasource in metadata but found its not there. Pass --create to write metadata.')
                                                elif 'unit' not in meta['datasource']:
                                                    bad_unit_msg(', but no unit is specified in metadata. Pass --create to set unit.')
                                                elif 'description' not in meta['datasource']:
                                                    bad_desc_msg(', but no description is specified in metadata. Pass --create to set description.')
                                                elif 'unit' in res and meta['datasource']['unit'] != res['unit']:
                                                    bad_unit_msg(', but metadata specifies unit of {0}. Pass --create to update unit.'.format(meta['datasource']['unit']))
                                                elif 'description' in res and meta['datasource']['description'] != res['description']:
                                                    bad_desc_msg(', but metadata specifies description of {0}. Pass --create to update description.'.format(meta['datasource']['description']))


                                        if 'public' in res:
                                            resPub = res['public']
                                            public = info['description']['public']
                                            if public is None:
                                                if create:
                                                    new_desc = info['description'].copy()
                                                    new_desc['public'] = respub
                                                    rpc.update(cik, {'alias': alias}, new_desc)
                                                else:
                                                    sys.stdout.write('spec expects public for {0} to be {1}, but they are not.'.format(alias, resPub))
                                            elif public != resPub:
                                                sys.stdout.write('spec expects public for {0} to be {1}, but they are not.'.format(alias, resPub))


                                        if 'subscribe' in res:
                                            # Alias *must* be local to this CIK
                                            resSub = res['subscribe']
                                            # Lookup alias/name if need be
                                            if resSub in aliases:
                                                resSub = aliases[resSub]
                                            subscribe = info['description']['subscribe']
                                            if subscribe is None:
                                                if create:
                                                    new_desc = info['description'].copy()
                                                    new_desc['subscribe'] = resSub
                                                    rpc.update(cik, {'alias': alias}, new_desc)
                                                else:
                                                    sys.stdout.write('spec expects subscribe for {0} to be {1}, but they are not.'.format(alias, resSub))
                                            elif subscribe != resSub:
                                                sys.stdout.write('spec expects subscribe for {0} to be {1}, but they are not.'.format(alias, resSub))

                                        if 'preprocess' in res:
                                            def fromAliases(pair):
                                                if pair[1] in aliases:
                                                    return [pair[0], aliases[pair[1]]]
                                                else:
                                                    return pair
                                            resPrep = [fromAliases(x) for x in res['preprocess']]
                                            preprocess = info['description']['preprocess']
                                            if preprocess is None or len(preprocess) == 0:
                                                if create:
                                                    new_desc = info['description'].copy()
                                                    new_desc['preprocess'] = resPrep
                                                    rpc.update(cik, {'alias': alias}, new_desc)
                                                else:
                                                    sys.stdout.write('spec expects preprocess for {0} to be {1}, but they are not.'.format(alias, resPrep))
                                            elif preprocess != resPrep:
                                                sys.stdout.write('spec expects preprocess for {0} to be {1}, but they are {2}.'.format(alias, resPrep, preprocess))

                                        if 'retention' in res:
                                            resRet = {}
                                            if 'count' in res['retention']:
                                                resRet['count'] = res['retention']['count']
                                            if 'duration' in res['retention']:
                                                resRet['duration'] = res['retention']['duration']

                                            retention = info['description']['retention']
                                            if create:
                                                new_desc = info['description'].copy()
                                                new_desc['retention'] = resRet
                                                rpc.update(cik, {'alias': alias}, new_desc)
                                            elif retention != resRet:
                                                sys.stdout.write('spec expects retention for {0} to be {1}, but they are {2}.'.format(alias, resRet, retention))


                                    elif typ == 'script':
                                        if 'file' not in res:
                                            raise ExoException('{0} is a script, so it needs a "file" key'.format(alias))
                                        name = res['name'] if 'name' in res else alias

                                        if not exists and create:
                                            rpc.upload_script([cik], res['file'], name=alias, create=True, filterfn=template)
                                            continue

                                        with open(res['file'], 'rb') as scriptfile:
                                            script_spec = template(scriptfile.read().decode('utf8'))
                                            script_svr = info['description']['rule']['script']
                                            if script_svr != script_spec:
                                                print('Script for {0} does not match file {1}.'.format(alias, res['file']))
                                                if updatescripts:
                                                    print('Uploading script to {0}...'.format(alias))
                                                    rpc.upload_script([cik], res['file'], name=name, create=False, filterfn=template)
                                                elif not args['--no-diff']:
                                                    # show diff
                                                    import difflib
                                                    differ = difflib.Differ()

                                                    differences = '\n'.join(
                                                        difflib.unified_diff(
                                                            script_spec.splitlines(),
                                                            script_svr.splitlines(),
                                                            fromfile=res['file'],
                                                            tofile='info["description"]["rule"]["script"]'))

                                                    print(differences)
                                    else:
                                        raise ExoException('Found unsupported type {0} in spec.'.format(typ))
                except Spec401Exception as ex:
                    print("******WARNING******* 401 received in spec, is the device expired?")
                    pass

