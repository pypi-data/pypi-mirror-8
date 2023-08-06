
import unittest
import Yaco
from moa.sysConf import sysConf
import moa.job
import moa.logger as l


class templateTest(unittest.TestCase):
    """
    Test a ruff template
    """
    def __init__(self, job, *args, **kwargs):
        self.job = job
        super(templateTest, self).__init__(*args, **kwargs)

    def runTest(self):
        if not hasattr(self, 'job'):
            # only test if a job is set
            # hence, only if it is called by RuffSuite()
            return

        l.critical("testing %s" % self.job.template.name)
        templateName = self.job.template.name
        sysConf.job = self.job

        #has the job properly instantiated?
        self.assertTrue(isinstance(self.job, moa.job.Job))

        #currently we're only testing ruff type jobs
        if not self.job.template.backend == 'ruff':
            self.skipTest("Only testing ruff jobs - not %s" %
                          templateName)

        #if
        if not self.job.hasCommand('unittest'):
            self.skipTest("no unittest defined for %s" %
                          templateName)

        #self.job.prepare()
        sysConf.pluginHandler.run('prepare_3')
        dummyargs = Yaco.Yaco()
        dummyargs.command = 'unittest'
        rc = self.job.execute(self.job, dummyargs)
        print rc
        self.assertEqual(rc, 0, 'test failed for %s' %
                         templateName)

        #self.assertEqual(widget.size(), (50, 50), 'incorrect default size')
