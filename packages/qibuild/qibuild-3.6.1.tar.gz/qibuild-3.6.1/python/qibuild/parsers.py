## Copyright (c) 2012-2014 Aldebaran Robotics. All rights reserved.
## Use of this source code is governed by a BSD-style license that can be
## found in the COPYING file.

""" Collection of parser fonctions for qibuild actions
"""

import os

from qisys import ui
import qisys.parsers
import qibuild.worktree
import qibuild.cmake_builder


def cmake_build_parser(parser, group=None):
    qisys.parsers.build_parser(parser, group=None)
    if not group:
        group = parser.add_argument_group("Build options")
    parser.add_argument("-j", dest="num_jobs", type=int)
    parser.add_argument("--build-type", action="store")
    group.add_argument("--verbose-make", action="store_true", default=False,
                    help="Print the executed commands while building")

def project_parser(parser, positional=True):
    """Parser settings for every action using several build projects."""
    group = qisys.parsers.project_parser(parser, positional=positional)
    # --use-deps is only useful when it would make more sense to
    # NOT solve the deps by default (for instance for `qibuild test`)
    group.add_argument("--use-deps", action="store_true", dest="use_deps",
                       help="Force deps resolution")
    group.add_argument("--build-deps-only", action="store_const",
                       const=["build"], dest="dep_types",
                       help="Work on specified projects by ignoring "
                             "the runtime deps.")
    parser.set_defaults(dep_types="default")

def get_build_worktree(args, verbose=True):
    """ Get a build worktree to use from a argparse.Namespace
    object

    """
    worktree = qisys.parsers.get_worktree(args)
    build_worktree = qibuild.worktree.BuildWorkTree(worktree)
    if verbose:
        ui.info(ui.green, "Current build worktree:", ui.reset, ui.bold, build_worktree.root)
    if not hasattr(args, "build_type"):
        # cmake_build_parser() has not been called, so do leave the default build_config
        return build_worktree
    build_config = get_build_config(build_worktree, args)
    build_worktree.build_config = build_config

    if verbose:
        if build_config.toolchain:
            ui.info(ui.green, "Using toolchain:", ui.blue, build_config.toolchain.name)

        for profile in build_config.profiles:
            ui.info(ui.green, "Using profile:", ui.blue, profile)

        ui.info(ui.green, "Build type:", ui.blue, build_config.build_type)

    return build_worktree

def get_build_projects(build_worktree, args, solve_deps=True, default_all=False):
    """ Get a list of build projects to use from an argparse.Namespace
    object. Useful when you do not need a CMakeBuilder.
    You can choose wether or not to solve the dependencies

    """
    parser = BuildProjectParser(build_worktree)
    projects = parser.parse_args(args, default_all=default_all)
    if not solve_deps or args.single:
        return projects
    dep_types = get_dep_types(args)
    deps_solver = qibuild.deps_solver.DepsSolver(build_worktree)
    return deps_solver.get_dep_projects(projects, dep_types)

def get_one_build_project(build_worktree, args):
    """ Get one build project from the command line.
    (zero or one project name may be specified)

    """
    parser = BuildProjectParser(build_worktree)
    projects = parser.parse_args(args)
    if not len(projects) == 1:
        raise Exception("This action can only work on one project")
    return projects[0]

def get_dep_types(args, default=None):
    """ Get a list of dep types from the command line """
    if not default:
        default = ["build", "runtime", "test"]
    if args.single:
        return list()
    if not hasattr(args, "dep_types") or args.dep_types == "default":
        return default
    return args.dep_types

def get_cmake_builder(args, default_dep_types=None):
    """ Get a :py:class:`.CMakeBuilder` object from the command line

    """
    build_worktree = get_build_worktree(args)
    # dep solving will be made later by the CMakeBuilder
    build_projects = get_build_projects(build_worktree, args, solve_deps=False)
    cmake_builder = qibuild.cmake_builder.CMakeBuilder(build_worktree, build_projects)
    cmake_builder.dep_types = get_dep_types(args, default=default_dep_types)
    return cmake_builder

def get_build_config(build_worktree, args):
    """ Get a CMakeBuildConfig object from an argparse.Namespace object

    """
    build_config = build_worktree.build_config
    if args.config:
        build_config.set_active_config(args.config)
    build_config.build_type = args.build_type
    if args.profiles:
        build_config.profiles = args.profiles
    if hasattr(args, "cmake_generator"):
        build_config.cmake_generator = args.cmake_generator
    if hasattr(args, "verbose_make"):
        build_config.verbose_make= args.verbose_make
    if hasattr(args, "cmake_flags") and args.cmake_flags:
        # should be a list a strings looking like key=value
        user_flags = list()
        for flag_string in args.cmake_flags:
            if "=" not in flag_string:
                raise Exception("Expecting a flag looking like -Dkey=value")
            (key, value) = flag_string.split("=")
            user_flags.append((key, value))
        build_config.user_flags = user_flags
    if hasattr(args, "num_jobs"):
        build_config.num_jobs = args.num_jobs
    return build_config

##
# Implementation details


class BuildProjectParser(qisys.parsers.AbstractProjectParser):
    """ Implements AbstractProjectParser for a BuildWorkTree """

    def __init__(self, build_worktree):
        self.build_worktree = build_worktree

    def all_projects(self, args):
        return self.build_worktree.build_projects

    def parse_no_project(self, args):
        """ Try to find the closest worktree project that
        mathes the current directory

        """
        # step 1: find the closest buildable project
        parser = qisys.parsers.WorkTreeProjectParser(self.build_worktree.worktree)
        worktree_projects = parser.parse_no_project(args)
        if not worktree_projects:
            raise CouldNotGuessProjectName()

        # WorkTreeProjectParser returns None or a list of one element
        worktree_proj = worktree_projects[0]
        build_proj = qisys.parsers.find_parent_project(self.build_worktree.build_projects,
                                                       worktree_proj.path)
        if not build_proj:
            # step 2: if we can't find, still look for a qiproject.xml not
            # registered yet and add it to the worktree:
            build_proj = qibuild.worktree.new_build_project(self.build_worktree,
                                                            worktree_proj)
        if not build_proj:
            # give up:
            raise CouldNotGuessProjectName()

        return self.parse_one_project(args, build_proj.name)

    def parse_one_project(self, args, project_arg):
        """ Accept both an absolute path matching a worktree project,
        or a project src

        """
        project = self.build_worktree.get_build_project(project_arg, raises=True)
        return [project]

class CouldNotGuessProjectName(Exception):
    def __str__(self):
        return """
Could not guess qibuild project name from current working directory
Please go inside a project, or specify the project name
on the command line
"""
