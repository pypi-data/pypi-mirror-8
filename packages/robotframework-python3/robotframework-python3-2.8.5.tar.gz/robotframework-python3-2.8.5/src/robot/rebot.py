#!/usr/bin/env python

#  Copyright 2008-2014 Nokia Solutions and Networks
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""Module implementing the command line entry point for post-processing outputs.

This module can be executed from the command line using the following
approaches::

    python -m robot.rebot
    python path/to/robot/rebot.py

Instead of ``python`` it is possible to use also other Python interpreters.
This module is also used by the installed ``rebot``, ``jyrebot`` and
``ipyrebot`` start-up scripts.

This module also provides :func:`rebot` and :func:`rebot_cli` functions
that can be used programmatically. Other code is for internal usage.
"""

USAGE = """Rebot -- Robot Framework report and log generator

Version:  <VERSION>

Usage:  rebot|jyrebot|ipyrebot [options] robot_outputs
   or:  python|jython|ipy -m robot.rebot [options] robot_outputs
   or:  python|jython|ipy path/to/robot/rebot.py [options] robot_outputs
   or:  java -jar robotframework.jar rebot [options] robot_outputs

Rebot can be used to generate logs and reports in HTML format. It can also
produce new XML output files which can be further processed with Rebot or
other tools.

Inputs to Rebot are XML output files generated by Robot Framework test runs or
earlier Rebot executions. When more than one input file is given, a new top
level test suite containing suites in the given files is created by default.
This allows combining multiple outputs together to create higher level reports.
An exception is that if --rerunmerge is used, results are combined by replacing
original tests with tests in the latter test runs.

Depending is Robot Framework installed using Python, Jython, or IronPython
interpreter, Rebot can be run using `rebot`, `jyrebot` or `ipyrebot` command,
respectively. Alternatively, it is possible to directly execute `robot.rebot`
module (e.g. `python -m robot.rebot`) or `robot/rebot.py` script using a
selected interpreter. Finally, there is also a standalone JAR distribution.

For more information about Robot Framework run, for example, `pybot --help` or
go to http://robotframework.org.

Options
=======

 -N --name name           Set the name of the top level test suite. Underscores
                          in the name are converted to spaces. Default name is
                          created from the name of the executed data source.
 -D --doc documentation   Set the documentation of the top level test suite.
                          Underscores in the documentation are converted to
                          spaces and it may also contain simple HTML formatting
                          (e.g. *bold* and http://url/).
 -M --metadata name:value *  Set metadata of the top level test suite.
                          Underscores in the name and value are converted to
                          spaces. Value can contain same HTML formatting as
                          --doc. Example: `--metadata version:1.2`
 -G --settag tag *        Sets given tag(s) to all executed test cases.
 -t --test name *         Select test cases by name or long name. Name is case
                          and space insensitive and it can also be a simple
                          pattern where `*` matches anything and `?` matches
                          any char. If using `*` and `?` in the console is
                          problematic, see --escape and --argumentfile.
 -s --suite name *        Select test suites by name. When this option is used
                          with --test, --include or --exclude, only test cases
                          in matching suites and also matching other filtering
                          criteria are selected. Given name can be a simple
                          pattern similarly as with --test.
 -i --include tag *       Select test cases to by tag. Similarly as name with
                          --test, tag is case and space insensitive and it is
                          possible to use patterns with `*` and `?` as
                          wildcards. Tags and patterns can also be combined
                          together with `AND`, `OR`, and `NOT` operators.
                          Examples: --include foo --include bar*
                                    --include fooANDbar*
 -e --exclude tag *       Select test cases not to be included by tag. These
                          tests are not selected even if included with
                          --include. Tags are matched using the rules explained
                          with --include.
 -R --rerunmerge          Combine results of re-running tests so that tests in
                          the latter runs replace the original. Typically used
                          after using --rerunfailed option when running tests.
                          Example: rebot --rerunmerge orig.xml rerun.xml
    --processemptysuite   Processes output also if the top level test suite is
                          empty. Useful e.g. with --include/--exclude when it
                          is not an error that no test matches the condition.
 -c --critical tag *      Tests having given tag are considered critical. If no
                          critical tags are set, all tags are critical. Tags
                          can be given as a pattern like  with --include.
 -n --noncritical tag *   Tests with given tag are not critical even if they
                          have a tag set with --critical. Tag can be a pattern.
 -d --outputdir dir       Where to create output files. The default is the
                          directory where Rebot is run from and the given path
                          is considered relative to that unless it is absolute.
 -o --output file         XML output file. Not created unless this option is
                          specified. Given path, similarly as paths given to
                          --log, --report and --xunit, is relative to
                          --outputdir unless given as an absolute path.
 -l --log file            HTML log file. Can be disabled by giving a special
                          name `NONE`. Default: log.html
                          Examples: `--log mylog.html`, `-l none`
 -r --report file         HTML report file. Can be disabled with `NONE`
                          similarly as --log. Default: report.html
 -x --xunit file          xUnit compatible result file. Not created unless this
                          option is specified.
    --xunitfile file      Deprecated. Use --xunit instead.
    --xunitskipnoncritical  Mark non-critical tests on xUnit output as skipped.
 -T --timestampoutputs    When this option is used, timestamp in a format
                          `YYYYMMDD-hhmmss` is added to all generated output
                          files between their basename and extension. For
                          example `-T -o output.xml -r report.html -l none`
                          creates files like `output-20070503-154410.xml` and
                          `report-20070503-154410.html`.
    --splitlog            Split log file into smaller pieces that open in
                          browser transparently.
    --logtitle title      Title for the generated test log. The default title
                          is `<Name Of The Suite> Test Log`. Underscores in
                          the title are converted into spaces in all titles.
    --reporttitle title   Title for the generated test report. The default
                          title is `<Name Of The Suite> Test Report`.
    --reportbackground colors  Background colors to use in the report file.
                          Either `all_passed:critical_passed:failed` or
                          `passed:failed`. Both color names and codes work.
                          Examples: --reportbackground green:yellow:red
                                    --reportbackground #00E:#E00
 -L --loglevel level      Threshold for selecting messages. Available levels:
                          TRACE (default), DEBUG, INFO, WARN, NONE (no msgs).
                          Use syntax `LOGLEVEL:DEFAULT` to define the default
                          visible log level in log files.
                          Examples: --loglevel DEBUG
                                    --loglevel DEBUG:INFO
    --suitestatlevel level  How many levels to show in `Statistics by Suite`
                          in log and report. By default all suite levels are
                          shown. Example:  --suitestatlevel 3
    --tagstatinclude tag *  Include only matching tags in `Statistics by Tag`
                          and `Test Details` in log and report. By default all
                          tags set in test cases are shown. Given `tag` can
                          also be a simple pattern (see e.g. --test).
    --tagstatexclude tag *  Exclude matching tags from `Statistics by Tag` and
                          `Test Details`. This option can be used with
                          --tagstatinclude similarly as --exclude is used with
                          --include.
    --tagstatcombine tags:name *  Create combined statistics based on tags.
                          These statistics are added into `Statistics by Tag`
                          and matching tests into `Test Details`. If optional
                          `name` is not given, name of the combined tag is got
                          from the specified tags. Tags are combined using the
                          rules explained in --include.
                          Examples: --tagstatcombine requirement-*
                                    --tagstatcombine tag1ANDtag2:My_name
    --tagdoc pattern:doc *  Add documentation to tags matching given pattern.
                          Documentation is shown in `Test Details` and also as
                          a tooltip in `Statistics by Tag`. Pattern can contain
                          characters `*` (matches anything) and `?` (matches
                          any char). Documentation can contain formatting
                          similarly as with --doc option.
                          Examples: --tagdoc mytag:My_documentation
                                    --tagdoc regression:*See*_http://info.html
                                    --tagdoc owner-*:Original_author
    --tagstatlink pattern:link:title *  Add external links into `Statistics by
                          Tag`. Pattern can contain characters `*` (matches
                          anything) and `?` (matches any char). Characters
                          matching to wildcard expressions can be used in link
                          and title with syntax %N, where N is index of the
                          match (starting from 1). In title underscores are
                          automatically converted to spaces.
                          Examples: --tagstatlink mytag:http://my.domain:Link
                          --tagstatlink bug-*:http://tracker/id=%1:Bug_Tracker
    --removekeywords all|passed|for|wuks|name:<pattern> *  Remove keyword data
                          from all generated outputs. Keywords containing
                          warnings are not removed except in `all` mode.
                          all:     remove data from all keywords
                          passed:  remove data only from keywords in passed
                                   test cases and suites
                          for:     remove passed iterations from for loops
                          wuks:    remove all but the last failing keyword
                                   inside `BuiltIn.Wait Until Keyword Succeeds`
                          name:<pattern>:  remove data from keywords that match
                                   the given pattern. The pattern is matched
                                   against the full name of the keyword (e.g.
                                   'MyLib.Keyword', 'resource.Second Keyword'),
                                   is case, space, and underscore insensitive,
                                   and may contain `*` and `?` as wildcards.
                                   Examples: --removekeywords name:Lib.HugeKw
                                             --removekeywords name:myresource.*
    --flattenkeywords for|foritem|name:<pattern> *  Flattens matching keywords
                          in all generated outputs. Matching keywords get all
                          log messages from their child keywords and children
                          are discarded otherwise.
                          for:     flatten for loops fully
                          foritem: flatten individual for loop iterations
                          name:<pattern>:  flatten matched keywords using same
                                   matching rules as with
                                   `--removekeywords name:<pattern>`
    --starttime timestamp  Set starting time of test execution when creating
                          reports. Timestamp must be given in format
                          `2007-10-01 15:12:42.268` where all separators are
                          optional (e.g. `20071001151242268` is ok too) and
                          parts from milliseconds to hours can be omitted if
                          they are zero (e.g. `2007-10-01`). This can be used
                          to override starttime of the suite when reports are
                          created from a single suite or to set starttime for
                          combined suite, which is otherwise set to `N/A`.
    --endtime timestamp   Same as --starttime but for ending time. If both
                          options are used, elapsed time of the suite is
                          calculated based on them. For combined suites,
                          it is otherwise calculated by adding elapsed times
                          of combined test suites together.
    --nostatusrc          Sets the return code to zero regardless of failures
                          in test cases. Error codes are returned normally.
 -C --monitorcolors auto|on|ansi|off  Use colors on console output or not.
                          auto: use colors when output not redirected (default)
                          on:   always use colors
                          ansi: like `on` but use ANSI colors also on Windows
                          off:  disable colors altogether
                          Note that colors do not work with Jython on Windows.
 -E --escape what:with *  Escape characters which are problematic in console.
                          `what` is the name of the character to escape and
                          `with` is the string to escape it with. Note that
                          all given arguments, incl. data sources, are escaped
                          so escape characters ought to be selected carefully.
                          <---------------------ESCAPES----------------------->
                          Examples:
                          --escape space:_ --metadata X:Value_with_spaces
                          -E space:SP -E quot:Q -v var:QhelloSPworldQ
 -A --argumentfile path *  Text file to read more arguments from. File can have
                          both options and data sources one per line. Contents
                          do not need to be escaped but spaces in the beginning
                          and end of lines are removed. Empty lines and lines
                          starting with a hash character (#) are ignored.
                          Example file:
                          |  --include regression
                          |  --name Regression Tests
                          |  # This is a comment line
                          |  my_tests.html
                          |  path/to/test/directory/
 -h -? --help             Print usage instructions.
 --version                Print version information.

Options that are marked with an asterisk (*) can be specified multiple times.
For example, `--test first --test third` selects test cases with name `first`
and `third`. If other options are given multiple times, the last value is used.

Long option format is case-insensitive. For example, --SuiteStatLevel is
equivalent to but easier to read than --suitestatlevel. Long options can
also be shortened as long as they are unique. For example, `--logti Title`
works while `--lo log.html` does not because the former matches only --logtitle
but the latter matches both --log and --logtitle.

Environment Variables
=====================

REBOT_OPTIONS             Space separated list of default options to be placed
                          in front of any explicit options on the command line.
ROBOT_SYSLOG_FILE         Path to a file where Robot Framework writes internal
                          information about processed files. Can be useful when
                          debugging problems. If not set, or set to special
                          value `NONE`, writing to the syslog file is disabled.
ROBOT_SYSLOG_LEVEL        Log level to use when writing to the syslog file.
                          Available levels are the same as for --loglevel
                          command line option and the default is INFO.

Examples
========

# Simple Rebot run that creates log and report with default names.
$ rebot output.xml

# Using options. Note that this is one long command split into multiple lines.
$ rebot --log smoke_log.html --report smoke_report.html --include smoke
        --ReportTitle Smoke_Tests --ReportBackground green:yellow:red
        --TagStatCombine tag1ANDtag2 path/to/myoutput.xml

# Executing `robot.rebot` module using Python and creating combined outputs.
$ python -m robot.rebot outputs/*.xml

# Running `robot/rebot.py` script with Jython.
$ jython path/robot/rebot.py -N Project_X -l none -r x.html output.xml
"""

import sys

# Allows running as a script. __name__ check needed with multiprocessing:
# http://code.google.com/p/robotframework/issues/detail?id=1137
if 'robot' not in sys.modules and __name__ == '__main__':
    ## import pythonpathsetter
    #HACK: Prevent 2to3 from converting to relative import
    pythonpathsetter = __import__('pythonpathsetter')

from robot.conf import RebotSettings
from robot.errors import DataError
from robot.reporting import ResultWriter
from robot.output import LOGGER
from robot.utils import Application
from robot.run import RobotFramework


class Rebot(RobotFramework):

    def __init__(self):
        Application.__init__(self, USAGE, arg_limits=(1,),
                             env_options='REBOT_OPTIONS', logger=LOGGER)

    def main(self, datasources, **options):
        settings = RebotSettings(options)
        LOGGER.register_console_logger(**settings.console_logger_config)
        LOGGER.disable_message_cache()
        rc = ResultWriter(*datasources).write_results(settings)
        if rc < 0:
            raise DataError('No outputs created.')
        return rc


def rebot_cli(arguments):
    """Command line execution entry point for running rebot.

    :param arguments: Command line arguments as a list of strings.

    For programmatic usage the :func:`rebot` method is typically better. It has
    a better API for that usage and does not call :func:`sys.exit` like this
    method.

    Example::

        from robot import rebot_cli

        rebot_cli(['--report', 'r.html', '--log', 'NONE', 'o1.xml', 'o2.xml'])
    """
    Rebot().execute_cli(arguments)


def rebot(*datasources, **options):
    """Creates reports/logs from given Robot output files with given options.

    Given input files are paths to Robot output files similarly as when running
    rebot from the command line. Options are given as keywords arguments and
    their names are same as long command line options without hyphens.

    Options that can be given on the command line multiple times can be
    passed as lists like `include=['tag1', 'tag2']`. If such option is used
    only once, it can be given also as a single string like `include='tag'`.

    To capture stdout and/or stderr streams, pass open file objects in as
    special keyword arguments `stdout` and `stderr`, respectively.

    A return code is returned similarly as when running on the command line.

    Examples::

        from robot import rebot

        rebot('path/to/output.xml')
        with open('stdout.txt', 'w') as stdout:
            rebot('o1.xml', 'o2.xml', report='r.html', log='NONE', stdout=stdout)

    Equivalent command line usage::

        rebot path/to/output.xml
        rebot --report r.html --log NONE o1.xml o2.xml > stdout.txt
    """
    return Rebot().execute(*datasources, **options)


if __name__ == '__main__':
    rebot_cli(sys.argv[1:])

