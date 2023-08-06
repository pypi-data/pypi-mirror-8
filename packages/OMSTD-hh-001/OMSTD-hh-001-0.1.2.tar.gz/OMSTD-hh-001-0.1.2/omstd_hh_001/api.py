# -*- coding: utf-8 -*-

"""
Project name: Open Methodology for Security Tool Developers
Project URL: https://github.com/cr0hn/OMSTD

Copyright (c) 2014, cr0hn<-AT->cr0hn.com
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""


"""
API file
"""

__author__ = 'cr0hn - cr0hn<-at->cr0hn.com (@ggdaniel)'

__all__ = ["run_scan", "run_in_console"]

import time

# Import data
from .lib.data import *
from .lib.scan_tools import scan_tcp_ports


# ----------------------------------------------------------------------
def run_scan(input_parameters):
    """
    Checks MD5 hash and return an Results object.

    :param input_parameters: Parameters object with config
    :type input_parameters: Parameters

    :return: dict with IPs and their results object: {TARGET: Results()}
    :rtype: dict(str: Results)

    :raises: TypeError
    """
    if not isinstance(input_parameters, Parameters):
        raise TypeError("Expected Parameters, got '%s' instead" % type(input_parameters))

    results = {}

    #
    # Scan each target
    #
    for target in input_parameters.targets:

        start = time.time()

        # Run!
        r = scan_tcp_ports(target, input_parameters)

        end = time.time()
        taken_time = end - start

        results[target] = Results(ports=r,
                                  scan_time=taken_time)

    return results


# ----------------------------------------------------------------------
def run_in_console(input_parameters):
    """
    Run for command line interface. It's make all steps of tool:

    :param input_parameters: Parameters object with config
    :type input_parameters: Parameters

    :raises: TypeError
    """
    print("\nStarting OMSTD-HH-001 port scan.")
    results = run_scan(input_parameters)

    start = time.time()

    # Run!
    for target, res in results.items():

        print("\nCompleted Connect Scan, %ss elapsed (%s total ports)" % (len(res.scan_time), len(res.ports)))
        print("Scan report for %s" % target)
        print("Not shown: %s closed ports" % abs(len(res.open_ports) - len(res.ports)))
        print("PORT     STATE SERVICE")

        # Show open ports
        for port, status in res.ports.items():
            if input_parameters.only_open is True and status == "closed":
                continue
            print("%s/tcp %s" % (port, status))

    end = time.time()
    taken_time = '{number:.8f}'.format(number=(end - start))
    print("Done: %s target%s scanned in %s seconds\n" % (
        len(results),
        "s" if len(results) > 1 else "",
        taken_time))
