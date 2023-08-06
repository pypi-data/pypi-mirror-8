##########################################################################
#
#   MRC FGU Computational Genomics Group
#
#   $Id$
#
#   Copyright (C) 2009 Andreas Heger
#
#   This program is free software; you can redistribute it and/or
#   modify it under the terms of the GNU General Public License
#   as published by the Free Software Foundation; either version 2
#   of the License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
##########################################################################
'''
CGAT.py - CGAT project specific functions
=========================================

:Author: Andreas Heger
:Release: $Id$
:Date: |today|
:Tags: Python

The :mod:`CGAT` module contains various utility functions
for working on CGAT projects.

API
----
'''
import os
import re
import shutil
import inspect

from CGAT import Experiment as E

PROJECT_ROOT = '/ifs/projects'


def getProjectDirectories():
    '''return a dict directories relevant to this project.'''

    project_name = getProjectName()

    result = {
        'webdir': os.path.join(PROJECT_ROOT,
                               PARAMS["web_dir"]),
        'exportdir': os.path.join(PARAMS["exportdir"]),
        'notebookdir': os.path.join(PROJECT_ROOT,
                                    project_name, "notebooks")
    }

    for x, y in result.items():
        if not os.path.exists(y):
            raise ValueError(
                "directory %s for %s does not exist" % (y, x))

    return result


#######################################################
# Duplicated functions from Pipeline.py - refactor
# once Local.py is fully parameterized
#######################################################
def getPipelineName():
    '''return the name of the pipeline.

    The name does not include the ``.py``
    suffix.
    '''
    # use the file attribute of the caller
    for x in inspect.stack():
        if x[0].f_globals["__name__"] == "__main__":
            return os.path.basename(x[0].f_globals['__file__'])[:-3]


def getMakefiles(makefiles, source_directory="", ignore_missing=False):
    """get all makefiles that are included in a set of makefiles.

    Keep the order of inclusion.
    """

    read_makefiles = set()
    output_makefiles = []

    def __getMakefiles(makefiles):

        new_makefiles = []
        for makefile in makefiles:
            if makefile in read_makefiles:
                continue
            if os.path.exists(makefile):
                fn = makefile
            elif os.path.exists(os.path.join(source_directory, makefile)):
                fn = os.path.join(source_directory, makefile)
            else:
                if ignore_missing:
                    continue
                else:
                    raise IOError("could not find %s in %s" %
                                  (makefile, source_directory))

            output_makefiles.append(fn)
            infile = open(fn, "r")

            for line in infile:
                if re.match("include\s+(\S+)", line):
                    fn = re.search("include\s+(\S+)", line).groups()[0]
                    # add explicitely given files
                    if os.path.exists(fn):
                        new_makefile = fn
                    else:
                        new_makefile = os.path.basename(fn)
                        # remove any path name variables
                        new_makefile = new_makefile[
                            new_makefile.find(")") + 1:]
                    if new_makefile not in read_makefiles:
                        new_makefiles.append(new_makefile)
            infile.close()

            read_makefiles.add(makefile)

        if new_makefiles:
            __getMakefiles(new_makefiles)

    __getMakefiles(makefiles)

    return output_makefiles


def getScripts(makefiles, source_directory):
    """extract all python and perl scripts from a set of makefiles."""

    scripts = set()

    for makefile in makefiles:
        for line in open(makefile, "r"):
            if re.search("python", line):
                try:
                    python_scripts = re.search(
                        "python\s+(\S+.py)", line).groups()
                except AttributeError:
                    continue

                for s in python_scripts:
                    scripts.add(("python", s))

            if re.search("perl", line):
                try:
                    perl_scripts = re.search("perl\s+(\S+.pl)", line).groups()
                except AttributeError:
                    continue

                for s in perl_scripts:
                    scripts.add(("perl", s))

    return scripts


def getModules(modules, scriptdirs, libdirs):
    """extract all imported libraries (modules) from a set of (python) scripts.

    Libraries that are not found are ignored and assumed to be
    installed systemwide.
    """

    read_modules = set()
    system_modules = set()

    def __getModules(modules):

        new_modules = set()

        for lib in modules:
            if lib in read_modules or lib in system_modules:
                continue
            for x in scriptdirs + libdirs:
                if os.path.exists(x + lib):
                    for line in open(x + lib, "r"):
                        if re.match("import\s+(\S+)", line):
                            ll = re.search("import\s+(\S+)", line).groups()[0]
                            ll = filter(
                                lambda x: x != "", map(lambda x: x.strip(),
                                                       ll.split(",")))
                            for l in ll:
                                new_modules.add(l + ".py")

                    read_modules.add(lib)
                    break
            else:
                system_modules.add(lib)

        if new_modules:
            __getModules(new_modules)

    __getModules(modules)

    read_modules = read_modules.difference(modules)

    return read_modules, system_modules


##########################################################################
##########################################################################
##########################################################################
# Methods related to publishing - should be moved into the CGATPipelines
# directory.
##########################################################################
def getProjectId():
    '''cgat specific method: get the (obfuscated) project id
    based on the current working directory.

    web_dir should be link to the web directory in the project
    directory which then links to the web directory in the sftp
    directory which then links to the obfuscated directory.

    pipeline:web_dir
    -> /ifs/projects/.../web
    -> /ifs/sftp/.../web
    -> /ifs/sftp/.../aoeuCATAa (obfuscated directory)

    '''
    curdir = os.path.abspath(os.getcwd())
    if not curdir.startswith(PROJECT_ROOT):
        raise ValueError(
            "method getProjectId no called within %s" % PROJECT_ROOT)

    webdir = PARAMS['web_dir']
    assert os.path.islink(webdir)
    target = os.readlink(webdir)
    assert os.path.islink(target)
    return os.path.basename(os.readlink(target))


def getProjectName():
    '''cgat specific method: get the name of the project
    based on the current working directory.'''

    curdir = os.path.abspath(os.getcwd())
    if not curdir.startswith(PROJECT_ROOT):
        raise ValueError(
            "method getProjectName no called within %s" % PROJECT_ROOT)
    prefixes = len(PROJECT_ROOT.split("/"))
    return curdir.split("/")[prefixes]


def getPublishDestinations(prefix="", suffix=None):

    if not prefix:
        prefix = PARAMS.get("report_prefix", "default")

    if prefix == "default":
        prefix = getPipelineName() + "_"

    if not suffix:
        suffix = PARAMS.get("report_suffix", "")

    dest_report = prefix + "report"
    dest_export = prefix + "export"

    if suffix is not None:
        dest_report += suffix
        dest_export += suffix

    return dest_report, dest_export


def publish_report(prefix="",
                   patterns=[],
                   project_id=None,
                   prefix_project="/ifs/projects",
                   export_files=None,
                   suffix=None,
                   subdirs=False,
                   ):
    '''publish report into web directory.

    Links export directory into web directory.

    Copies html pages and fudges links to the pages in the
    export directory.

    If *prefix* is given, the directories will start with prefix,
    otherwise, it is looked up from the option ``report_prefix``.
    If report_prefix is "default", the prefix will be derived
    from the pipeline name. For example, pipeline_intervals will
    we copied to ``pipeline_intervals_report``.

    *patterns* is an optional list of two-element tuples (<pattern>,
    replacement_string).  Each substitutions will be applied on each
    file ending in .html.

    If *project_id* is not given, it will be looked up. This requires
    that this method is called within a subdirectory of PROJECT_ROOT.

    *export_files* is a dictionary of files to be exported. The key
    of the dictionary denotes the targetdirectory within the web
    directory. The values in the dictionary are the files to be
    linked to in the direcotry. For example::

        exportfiles = {
            "bamfiles" : glob.glob( "*/*.bam" ) + glob.glob( "*/*.bam.bai" ),
            "bigwigfiles" : glob.glob( "*/*.bw" ),
            }

    .. note::
       This function is CGAT specific.

    '''

    dest_report, dest_export = getPublishDestinations(prefix, suffix)

    web_dir = PARAMS["web_dir"]

    if project_id is None:
        project_id = getProjectId()

    src_export = os.path.abspath("export")
    curdir = os.path.abspath(os.getcwd())

    # substitute links to export and report
    base_url = "http://www.cgat.org/downloads/%s" % project_id
    _patterns = [
        # redirect export directory
        (re.compile(src_export),
         "%(base_url)s/%(dest_export)s" % locals()),
        # redirect report directory
        (re.compile(curdir),
         "%(base_url)s/%(dest_report)s" % locals()),
        (re.compile('(%s)/_static' %
                    curdir),
         "%(base_url)s/%(dest_report)s/_static" % locals())]

    _patterns.extend(patterns)

    def _link(src, dest):
        '''create links.

        Only link to existing targets.
        '''
        if os.path.exists(dest):
            os.remove(dest)

        if not os.path.exists(src):
            E.warn("%s does not exist - skipped" % src)
            return

        # IMS: check if base path of dest exists. This allows for
        # prefix to be a nested path structure e.g. project_id/
        if not os.path.exists(os.path.dirname(os.path.abspath(dest))):
            E.info('creating directory %s' %
                   os.path.dirname(os.path.abspath(dest)))
            os.mkdir(os.path.dirname(os.path.abspath(dest)))

        os.symlink(os.path.abspath(src), dest)

    def _copy(src, dest):
        if os.path.exists(dest):
            shutil.rmtree(dest)
        if not os.path.exists(src):
            E.warn("%s does not exist - skipped" % src)
            return
        shutil.copytree(os.path.abspath(src), dest)

    # publish export dir via symlinking
    E.info("linking export directory in %s" % dest_export)
    _link(src_export,
          os.path.abspath(os.path.join(web_dir, dest_export)))

    # publish web pages by copying
    E.info("publishing web pages in %s" %
           os.path.abspath(os.path.join(web_dir, dest_report)))
    _copy(os.path.abspath("report/html"),
          os.path.abspath(os.path.join(web_dir, dest_report)))

    for root, dirs, files in os.walk(os.path.join(web_dir, dest_report)):
        for f in files:
            fn = os.path.join(root, f)
            if fn.endswith(".html"):
                with open(fn) as inf:
                    data = inf.read()
                for rx, repl in _patterns:
                    data = rx.sub(repl, data)
                outf = open(fn, "w")
                outf.write(data)
                outf.close()

    if export_files:
        bigwigs, bams, beds = [], [], []

        for targetdir, filenames in export_files.items():

            targetdir = os.path.join(web_dir, targetdir)
            if not os.path.exists(targetdir):
                os.makedirs(targetdir)

            for src in filenames:
                dest = os.path.join(targetdir, os.path.basename(src))
                if dest.endswith(".bam"):
                    bams.append((targetdir, dest))
                elif dest.endswith(".bw"):
                    bigwigs.append((targetdir, dest))
                elif dest.endswith(".bed.gz"):
                    beds.append((targetdir, dest))
                dest = os.path.abspath(dest)
                if not os.path.exists(dest):
                    try:
                        os.symlink(os.path.abspath(src), dest)
                    except OSError, msg:
                        E.warn("could not create symlink from %s to %s: %s" %
                               (os.path.abspath(src), dest, msg))

        # output ucsc links
        with open("urls.txt", "w") as outfile:
            for targetdir, fn in bams:
                filename = os.path.basename(fn)
                track = filename[:-len(".bam")]
                outfile.write(
                    """track type=bam name="%(track)s" bigDataUrl=http://www.cgat.org/downloads/%(project_id)s/%(targetdir)s/%(filename)s\n""" % locals())

            for targetdir, fn in bigwigs:
                filename = os.path.basename(fn)
                track = filename[:-len(".bw")]
                outfile.write(
                    """track type=bigWig name="%(track)s" bigDataUrl=http://www.cgat.org/downloads/%(project_id)s/%(targetdir)s/%(filename)s\n""" % locals())

            for targetdir, fn in beds:
                filename = os.path.basename(fn)
                track = filename[:-len(".bed.gz")]
                outfile.write(
                    """http://www.cgat.org/downloads/%(project_id)s/%(targetdir)s/%(filename)s\n""" % locals())

        E.info("UCSC urls are in urls.txt")

    E.info(
        "report has been published at http://www.cgat.org/downloads/%(project_id)s/%(dest_report)s" % locals())


