# -*- coding: utf-8 -*-
#
# This file is part of Workflow.
# Copyright (C) 2014 CERN.
#
# Workflow is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for
# more details.

import unittest
import os
import logging
from six import StringIO

from workflow.config import config_reader


class TestConfig(unittest.TestCase):

    """Tests of the WE interface"""

    def setUp(self):
        config_reader.setBasedir(os.path.dirname(__file__))
        self._old_handlers = logging.root.handlers[:]

    def tearDown(self):
        logging.root.handlers = self._old_handlers[:]

    def test_basics(self):
        config_reader.init(os.path.join(os.path.dirname(__file__),
                                        'local.ini'))
        self.assertEqual(config_reader.STRING, 'string')
        self.assertEqual(config_reader.ARRAY, ['one', 'two', 'three'])
        self.assertEqual(config_reader.OVERRIDEN, 'local')
        self.assertEqual(config_reader.string, 'global/local')

        config_reader.init(os.path.join(os.path.dirname(__file__),
                                        'local2.ini'))
        self.assertEqual(config_reader.STRING, 'string')
        self.assertEqual(config_reader.ARRAY, ['one', 'two', 'three'])
        self.assertEqual(config_reader.OVERRIDEN, 'global')
        self.assertEqual(config_reader.string, 'second')

    def test_logger(self):
        """The WF logger should not affect other loggers."""
        from workflow import engine

        logging.root.handlers = []
        engine.LOG.handlers = []

        other_logger = logging.getLogger('other')
        wf_logger = engine.get_logger('workflow.test')

        test_io = StringIO()
        root_io = StringIO()
        other_io = StringIO()

        logging.root.addHandler(logging.StreamHandler(root_io))
        other_logger.addHandler(logging.StreamHandler(other_io))
        wf_logger.addHandler(logging.StreamHandler(test_io))

        # set the root level to WARNING; wf should honour parent level
        logging.root.setLevel(logging.WARNING)

        logging.warn('root warn')
        other_logger.warn('other warn')
        wf_logger.warn('wf warn')

        logging.info('root info')
        other_logger.info('other info')
        wf_logger.info('wf info')

        self.assertEqual(root_io.getvalue(), "root warn\nother warn\n",
                         "Root logger should have two msgs")
        self.assertEqual(other_io.getvalue(), "other warn\n",
                         "Other logger should have one msg")
        self.assertEqual(test_io.getvalue(), "wf warn\n",
                         "Wf logger should have one msg")

        root_io.seek(0)
        other_io.seek(0)
        test_io.seek(0)

        # now set too to DEBUG and wf to INFO
        logging.root.setLevel(logging.DEBUG)
        engine.reset_all_loggers(logging.WARNING)

        logging.warn('root warn')
        other_logger.warn('other warn')
        wf_logger.warn('wf warn')

        logging.info('root info')
        other_logger.info('other info')
        wf_logger.info('wf info')

        self.assertEqual(root_io.getvalue(), "root warn\nother warn\n"
                         "root info\nother info\n",
                         "Root logger should have four msgs")
        self.assertEqual(other_io.getvalue(), "other warn\nother info\n",
                         "Other logger should have two msg")
        self.assertEqual(test_io.getvalue(), "wf warn\n",
                         "Wf logger should have one msg")


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestConfig))
    return suite

if __name__ == '__main__':
    unittest.main()
    # unittest.TextTestRunner(verbosity=2).run(suite())
