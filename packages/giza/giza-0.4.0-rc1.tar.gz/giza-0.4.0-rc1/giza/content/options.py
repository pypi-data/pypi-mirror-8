# Copyright 2014 MongoDB, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import logging
from copy import deepcopy

logger = logging.getLogger('giza.content.options')

from jinja2 import Template
from rstcloth.rstcloth import RstCloth

from giza.tools.files import expand_tree, rm_rf
from giza.tools.serialization import ingest_yaml_list

#################### Rendering ####################

class Options(object):
    def __init__(self, fn=None):
        self.data = list()
        self.cache = dict()
        self.source_files = list()
        self.unresolved = list()

        if fn is not None:
            self.source_dirname = os.path.dirname(os.path.abspath(fn))
            logger.debug("reading options from {0}".format(fn))
            self.ingest(fn)
        else:
            self.source_dirname = fn

    def __len__(self):
        return len(self.cache)

    def ingest(self, fn):
        if self.source_dirname is None:
            self.source_dirname = os.path.dirname(os.path.abspath(fn))

        input_fn = os.path.join(self.source_dirname, os.path.basename(fn))
        input_sources = ingest_yaml_list(input_fn)
        self.cache[fn] = dict()

        self.source_files.append(input_sources)

        for option in input_sources:
            opt = Option(option)
            opt.source_filenames = [input_fn]

            self.cache_option(opt, fn)

        self.resolve(fn)

    def cache_option(self, opt, fn):
        if opt.program not in self.cache[fn]:
            self.cache[fn][opt.program] = dict()

        self.cache[fn][opt.program][opt.name] = opt

        if opt.inherited is True:
            self.unresolved.append(opt)
        else:
            self.data.append(opt)

    def resolve(self, fn):
        for opt in self.unresolved:
            if opt.inherited is True:
                deps = [os.path.join(self.source_dirname, fn)]

                if opt.source['file'] == fn:
                    continue
                else:
                    deps.append(os.path.join(self.source_dirname, opt.source['file']))

                if opt.source['file'] in self.cache:
                    base_opt = self.resolve_inherited(opt.source)
                else:
                    self.ingest(opt.source['file'])
                    base_opt = self.resolve_inherited(opt.source)

                base_opt.doc.update(opt.doc)
                if 'inherit' in base_opt.doc:
                    del base_opt.doc['inherit']

                opt = Option(base_opt.doc)
                opt.source_filenames = deps
                logmsg = 'cached option while rendering {0}, program "{1}" name "{2}"'
                logger.debug(logmsg.format(self.source_dirname, opt.program, opt.name))

                self.cache_option(opt, fn)

        self.unresolved = list()

    def resolve_inherited(self, spec):
        return deepcopy(self.cache[spec['file']][spec['program']][spec['name']])

    def iterator(self):
        for item in self.data:
            if not item.program.startswith('_'):
                yield item

optional_source_fields = ['default', 'type', 'pre', 'description', 'post', 'directive']

class Option(object):
    def __init__(self, doc):
        self.doc = doc
        self._directive = None

        self.name = doc['name']
        self.program = doc['program']

        for k in optional_source_fields:
            if k in doc:
                setattr(self, k, doc[k])
            else:
                setattr(self, k, None)

        if 'inherit' in doc:
            self.inherited = True
            self.source = doc['inherit']
        else:
            self.inherited = False
            self.source = {}

        if 'args' in doc:
            if doc['args'] is None or doc['args'] == '':
                pass
            else:
                self.arguments = doc['args']

        if 'aliases' in doc:
            if doc['aliases'] is None or doc['aliases'] == '':
                pass
            else:
                if isinstance(doc['aliases'], list):
                    self.aliases = doc['aliases']
                else:
                    self.aliases = [ doc['aliases'] ]

        self.replacement = dict()
        if 'replacement' in doc:
            if isinstance(doc['replacement'], dict):
                self.replacement = doc['replacement']

        # add auto-populated replacements here
        self.add_replacements()
        logmsg = 'created option representation for the {0} option for {1}'
        logger.debug(logmsg.format(self.name, self.program))

    @property
    def directive(self):
        if self._directive is None:
            return 'describe'
        else:
            return self._directive

    @directive.setter
    def directive(self, value):
        self._directive = value

    def add_replacements(self):
        if not self.program.startswith('_'):
            if 'program' not in self.replacement:
                self.replacement['program'] = ':program:`{0}`'.format(self.program)
            if 'role' not in self.replacement:
                if self.directive == 'describe':
                    self.replacement['role'] = "``{0}``".format(self.name)
                elif self.directive == 'option':
                    self.replacement['role'] = ":{0}:`--{1}`".format(self.directive, self.name)
                else:
                    self.replacement['role'] = ":{0}:`{1}`".format(self.directive, self.name)

    def replace(self):
        attempts = range(10)

        if self.description is not None:
            for i in attempts:
                template = Template(self.description)
                self.description = template.render(**self.replacement)

                if "{{" not in self.description:
                    break

        if self.pre is not None:
            for i in attempts:
                template = Template(self.pre)
                self.pre = template.render(**self.replacement)

                if "{{" not in self.pre:
                    break

        if self.post is not None:
            for i in attempts:
                template = Template(self.post)
                self.post = template.render(**self.replacement)

                if "{{" not in self.post:
                    break

        if self.default is not None and not (isinstance(self.default, bool) or
                                             isinstance(self.default, int)):
            for i in attempts:
                template = Template(self.default)
                self.efault = template.render(**self.replacement)

                if "{{" not in self.default:
                    break

    def resolve_output_path(self, path):
        name_parts = self.name.split(',')

        if len(name_parts) > 1:
            clensed_name = name_parts[0]
        else:
            clensed_name = self.name

        fn = '-'.join([ self.directive, self.program, clensed_name ]) + '.rst'
        return os.path.join(path, fn)

class OptionRendered(object):
    def __init__(self, option):
        if not isinstance(option, Option):
            raise TypeError
        else:
            self.option = option

        self.rst = RstCloth()

    def resolve_option_name(self):
        if self.option.directive == 'option':
            if self.option.name.startswith('<'):
                prefix = ''
            else:
                prefix = '--'

            if hasattr(self.option, 'aliases'):
                if hasattr(self.option, 'arguments'):
                    return '{0}{1} {2}, {3} {4}'.format(prefix, self.option.name,
                                                    self.option.arguments,
                                                    '{0}, '.format(self.option.arguments).join(self.option.aliases),
                                                    self.option.arguments)
                else:
                    return '{0}{1}, {2}'.format(prefix, self.option.name,
                                                ', '.join(self.option.aliases))

            else:
                if hasattr(self.option, 'arguments'):
                    return '{0}{1} {2}'.format(prefix, self.option.name,
                                               self.option.arguments)
                else:
                    return '{0}{1}'.format(prefix, self.option.name)
        else:
            return self.option.name

    def render(self, path):
        self.option.replace()

        self.rst.directive(self.option.directive, self.resolve_option_name())
        self.rst.newline()

        if self.option.type is not None:
            self.rst.content('*Type*: {0}'.format(self.option.type), indent=3)
            self.rst.newline()

        if self.option.default is not None:
            self.rst.content('*Default*: {0}'.format(self.option.default), indent=3)
            self.rst.newline()

        if self.option.pre is not None:
            self.rst.content(self.option.pre.split('\n'), indent=3, wrap=False)
            self.rst.newline()

        if self.option.description is not None:
            self.rst.content(self.option.description.split('\n'), indent=3, wrap=False)
            self.rst.newline()

        if self.option.post is not None:
            self.rst.content(self.option.post.split('\n'), indent=3, wrap=False)
            self.rst.newline()

        output_file = self.option.resolve_output_path(path)

        self.rst.write(output_file)

        logger.debug('wrote option to file {0}'.format(output_file))


#################### Source Iterators ####################1

def get_option_path(conf):
    return os.path.join(get_base_path(conf), 'option')

def get_base_path(conf):
    return os.path.join(conf.paths.projectroot,
                        conf.paths.branch_includes)

def option_sources(conf):
    output_path = get_option_path(conf)

    for fn in expand_tree(get_base_path(conf), 'yaml'):
        if fn.startswith(output_path):
            yield fn

#################### Worker and Integration ####################1

def render_option_page(opt, path):
    renderer = OptionRendered(opt)
    renderer.render(path)

def option_tasks(conf, app):
    base_path = get_base_path(conf)

    options = Options()
    options.source_dirname = base_path
    output_path = get_option_path(conf)

    for fn in option_sources(conf):
        options.ingest(fn)

    if len(options) > 0 and not os.path.exists(output_path):
        os.makedirs(output_path)

    for opt in options.iterator():
        t = app.add('task')
        t.job = render_option_page
        t.args = [ opt, output_path ]
        t.dependency = opt.source_filenames
        t.target = opt.resolve_output_path(output_path)
        t.description = 'generating option "{0}" for "{1}"'.format(opt.name, opt.program)

def option_clean(conf):
    rm_rf(get_option_path(conf))
    logger.info('removed all option output')
