# -*- coding: utf-8 -*-
from docutils.parsers.rst import Directive
import docutils
import hashlib
import os
import pickle
import robot
import tempfile

from sphinx.directives import CodeBlock

ROBOT_PICKLE_FILENAME = 'robotframework.pickle'


class RobotAwareCodeBlock(CodeBlock):

    option_spec = dict(
        docutils.parsers.rst.directives.body.CodeBlock.option_spec.items()
        + CodeBlock.option_spec.items()
    )

    def run(self):
        app = self.state_machine.document.settings.env.app
        document = self.state_machine.document

        if 'robotframework' in self.arguments:
            robot_source = u'\n'.join(self.content)
            if not hasattr(document, '_robot_source'):
                document._robot_source = robot_source
            else:
                document._robot_source += u'\n' + robot_source

            if 'hidden' in (self.options.get('class', []) or []):
                return []  # suppress nodes with :class: hidden
            if app.config.sphinxcontrib_robotframework_quiet:
                return []  # suppress nodes when required in settings

        return super(RobotAwareCodeBlock, self).run()


def creates_option(argument):
    """Splitslist of filenames into a list (and defaults to an empty list).
    """
    return filter(bool, argument.split() if argument else [])


class RobotSettingsDirective(Directive):
    """Per-document directive for controlling Robot Framework tests
    """
    has_content = False
    option_spec = {
        'creates': creates_option,
    }

    def run(self):
        # This directive was made obsolete in >= 0.5.0 and is now waiting for a
        # new purpose...
        return []


def get_robot_variables():
    """Return list of Robot Framework -compatible cli-variables parsed
    from ROBOT_-prefixed environment variable

    """
    prefix = 'ROBOT_'
    variables = []
    for key in os.environ:
        if key.startswith(prefix) and len(key) > len(prefix):
            variables.append('%s:%s' % (key[len(prefix):], os.environ[key]))
    return variables


def run_robot(app, doctree, docname):

    # Tests can be switched off with a global setting:
    if not app.config.sphinxcontrib_robotframework_enabled:
        return

    # Set up a variable for 'the current working directory':
    robot_dir = os.path.dirname(os.path.join(app.srcdir, docname))

    # Tests are only run when they are found:
    if not hasattr(doctree, '_robot_source'):
        return

    # Skip already run robotframework suites
    checksums_filename = os.path.join(app.doctreedir, ROBOT_PICKLE_FILENAME)
    try:
        with open(checksums_filename) as fp:
            checksums = pickle.loads(fp.read())
    except (IOError, EOFError, TypeError, IndexError):
        checksums = []
    checksum = hashlib.md5(doctree._robot_source).hexdigest()
    if checksum in checksums:
        return

    # Build a test suite:
    robot_file = tempfile.NamedTemporaryFile(dir=robot_dir, suffix='.robot')
    robot_file.write(doctree._robot_source.encode('utf-8'))
    robot_file.flush()  # flush buffer into file

    # Skip running when the source has no test cases (e.g. has settings)
    try:
        robot.running.TestSuiteBuilder().build(robot_file.name)
    except robot.errors.DataError, e:
        if e.message.endswith('File has no test case table.'):
            return
        raise
    except AttributeError, e:
        # Fix to make this package still work with robotframework < 2.8.x
        pass

    # Get robot variables from environment
    env_robot_variables = get_robot_variables()
    env_robot_keys = [var.split(':')[0] for var in env_robot_variables]

    # Run the test suite:
    options = {
        'outputdir': robot_dir,
        'output': 'NONE',
        'log': 'NONE',
        'report': 'NONE',
        'variable': env_robot_variables + [
            '%s:%s' % (key, value) for key, value
            in app.config.sphinxcontrib_robotframework_variables.items()
            if not key in env_robot_keys
        ]
    }
        # Update persisted checksums
    if robot.run(robot_file.name, **options) == 0:
        with open(checksums_filename, 'w') as fp:
            fp.write(pickle.dumps(checksums + [checksum]))

    # Close the test suite (and delete it, because it's a tempfile):
    robot_file.close()

    # Re-process images to include robot generated images:
    if os.path.sep in docname:
        # Because process_images is not designed to be called more than once,
        # calling it with docnames with sub-directories needs a bit cleanup:
        removable = os.path.dirname(docname) + os.path.sep
        for node in doctree.traverse(docutils.nodes.image):
            if node['uri'].startswith(removable):
                node['uri'] = node['uri'][len(removable):]
    app.env.process_images(docname, doctree)


def setup(app):
    app.add_config_value('sphinxcontrib_robotframework_enabled', True, True)
    app.add_config_value('sphinxcontrib_robotframework_variables', {}, True)
    app.add_config_value('sphinxcontrib_robotframework_quiet', False, True)
    app.add_directive('code', RobotAwareCodeBlock)
    app.add_directive('robotframework', RobotSettingsDirective)
    app.connect('doctree-resolved', run_robot)
