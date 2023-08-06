# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
#
# This file is part of Moa - http://github.com/mfiers/Moa
#
# Licensed under the GPL license (see 'COPYING')
#
"""
**parameterCheck** - check parameters
-------------------------------------
"""

import os

import moa.args
import moa.ui
from moa.sysConf import sysConf


def errorMessage(message, details):
    moa.ui.fprint(
        "%%(bold)s%%(red)sError%%(reset)s: %%(bold)s%s%%(reset)s: %s" % (
        message, details))


def _isInteger(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def _isFloat(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def hook_preRun():
    test_ui()


def hook_promptSnippet():
    """
    Function used by the prompt plugin to generate snippets for inlusion
    in the prompt
    """
    m = test(sysConf.job, {})
    if m:
        return "{{red}}X{{reset}}"
    else:
        return "{{green}}o{{reset}}"


def test_ui():

    options = sysConf['options']
    messages = test(sysConf.job, {})

    for message, detail in messages:
        errorMessage(message, detail)

    if messages and not options.force:
        moa.ui.exitError()


@moa.args.needsJob
@moa.args.command
def test(job, args):
    """
    Test the job parameters
    """
    messages = []
    rconf = job.conf.render()
    for p in rconf.keys():
        if p in job.conf.doNotCheck:
            continue

        if ' ' in p:
            messages.append(
                ("Invalid parameter name - cannot contain spaces", p))

        if not p in job.template.parameters:
            continue

        pt = job.template.parameters[p]
        if not pt.optional and not rconf[p]:
            messages.append(("Undefined variable", p))
        elif (pt.type == 'file'
              and job.conf[p]
              and not os.path.isfile(rconf[p])):
            if pt.get('optional', True):
                #ignore this
                pass
            else:
                print
                messages.append(("Not a file",
                                 "%s=%s " % (p, rconf[p])))
        elif (pt.type == 'directory'
              and job.conf[p]
              and not os.path.isdir(rconf[p])):
            messages.append((
                "Not a directory",
                "%s=%s " % (p, rconf[p])))

        elif (pt.type == 'integer'
              and job.conf[p]
              and not _isInteger(rconf[p])):
            messages.append(("Not an integer",
                             "%s=%s " % (p, rconf.conf[p])))
        elif (pt.type == 'float'
              and job.conf[p]
              and not _isFloat(rconf[p])):
            messages.append(("Not a float",
                             "%s=%s " % (p, rconf[p])))

    return messages
