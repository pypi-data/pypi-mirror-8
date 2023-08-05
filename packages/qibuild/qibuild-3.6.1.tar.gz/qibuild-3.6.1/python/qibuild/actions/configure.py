## Copyright (c) 2012-2014 Aldebaran Robotics. All rights reserved.
## Use of this source code is governed by a BSD-style license that can be
## found in the COPYING file.

"""Configure a project

"""

from qisys import ui

import qibuild.cmake
import qibuild.parsers

def configure_parser(parser):
    """Configure parser for this action"""
    qibuild.parsers.cmake_build_parser(parser)
    qibuild.parsers.project_parser(parser)
    group = parser.add_argument_group("configure options")
    group.add_argument("-G", "--cmake-generator", action="store",
        help="Specify the CMake generator")
    group.add_argument("-D", dest="cmake_flags",
        action="append",
        help="additional cmake flags")
    group.add_argument("--no-clean-first", dest="clean_first",
        action="store_false",
        help="do not clean CMake cache")
    group.add_argument("--debug-trycompile", dest="debug_trycompile",
        action="store_true",
        help="pass --debug-trycompile to CMake call")
    group.add_argument("--eff-c++", dest="effective_cplusplus",
        action="store_true",
        help="activate warnings from the 'Effective C++' book (gcc only)")
    group.add_argument("--werror", dest="werror",
        action="store_true",
        help="treat warnings as error")
    group.add_argument("--profiling", dest="profiling", action="store_true",
        help="profile cmake execution")
    group.add_argument("--summarize-options", dest="summarize_options",
                        action="store_true",
                        help="summarize build options at the end")
    group.add_argument("--trace-cmake", dest="trace_cmake",
                      action="store_true",
                      help="run cmake in trace mode")
    group.add_argument("--coverage", dest="coverage",
                       action="store_true",
                       help="activate coverage support (gcc only)")
    group.add_argument("--32-bits", dest="force_32_bits",
                       action="store_true", help="force 32 bits build")
    group.add_argument("--with-debug-info", action="store_true", dest="debug_info",
                        help="include debug information in binaries. Overrides --debug")
    group.add_argument("--without-debug-info", action="store_false", dest="debug_info",
                        help="remove debug information from binaries. Overrides --release")

    parser.set_defaults(clean_first=True, effective_cplusplus=False,
                        werror=False, profiling=False,
                        trace_cmake=False, debug_info=None)
    if not parser.epilog:
        parser.epilog = ""
    parser.epilog += """
Note:
    if CMAKE_INSTALL_PREFIX is set during configure, it will be necessary to
    repeat it at install (for further details, see: qibuild install --help).
"""

@ui.timer("qibuild configure")
def do(args):
    """Main entry point"""

    # Convert 'helper' options into cmake flags
    if not args.cmake_flags:
        args.cmake_flags = list()
    if args.effective_cplusplus:
        args.cmake_flags.append("QI_EFFECTIVE_CPP=ON")
    if args.werror:
        args.cmake_flags.append("QI_WERROR=ON")
    if args.coverage:
        args.cmake_flags.append("QI_WITH_COVERAGE=ON")
    # args.debug_info has 3 values: None (not set at all), True, False
    if args.debug_info is True:
        args.cmake_flags.append("QI_WITH_DEBUG_INFO=ON")
    if args.debug_info is False:
        args.cmake_flags.append("QI_WITH_DEBUG_INFO=OFF")
    if args.force_32_bits:
        args.cmake_flags.append("QI_FORCE_32_BITS=ON")

    cmake_builder = qibuild.parsers.get_cmake_builder(args)

    if args.debug_trycompile:
        ui.info(ui.green, "Using cmake --debug-trycompile")
    if args.trace_cmake:
        ui.info(ui.green, "Tracing CMake execution")

    cmake_builder.configure(clean_first=args.clean_first,
                            debug_trycompile=args.debug_trycompile,
                            trace_cmake=args.trace_cmake,
                            profiling=args.profiling,
                            summarize_options=args.summarize_options)
