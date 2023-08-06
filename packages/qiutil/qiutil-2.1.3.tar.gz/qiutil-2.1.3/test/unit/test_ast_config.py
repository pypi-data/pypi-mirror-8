import os
from nose.tools import (assert_equal, assert_is_not_none)
from ..helpers.logging import logger
from qiutil.ast_config import read_config
from test import ROOT

FIXTURE = os.path.join(ROOT, 'fixtures', 'ast_config', 'tuning.cfg')
"""The test fixture configuration file."""


class TestASTConfig(object):

    """The ASTConfig unit tests."""

    def test_config(self):
        logger(__name__).debug("Testing the JSON configuration loader on"
                               " %s..." % FIXTURE)
        cfg = read_config(FIXTURE)
        assert_is_not_none(cfg.has_section('Tuning'),
                           "The configuration is missing the Tuning section")
        opts = cfg['Tuning']
        expected = dict(method='FFT',
                        description="String with [ ( 3 , a\" ' 4.5 'b' ) ] characters",
                        iterations=[1, [2, [3, 4], 5]],
                        parameters=[(1,), (2, 3)],
                        sampling=[0.3, [None, [None] * 2, 1.0], -0.1],
                        two_tailed=[True, False],
                        threshold=1.2e-8,
                        plugin_args=dict(
                            qsub_args='-pe mpi 48-120 -l h_rt=4:00:00,mf=2G'' -b n',
                            overwrite=True))

        assert_equal(opts, expected, "The configuration Tuning options are"
                     " incorrect: %s" % opts)


if __name__ == "__main__":
    import nose

    nose.main(defaultTest=__name__)
