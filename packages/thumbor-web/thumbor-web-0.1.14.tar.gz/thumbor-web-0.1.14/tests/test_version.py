#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file is part of thumbor-web.
# https://github.com/thumbor/thumbor-web

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2014 Bernardo Heynemann heynemann@gmail.com

from preggy import expect

from thumbor_web import __version__
from tests.base import TestCase


class VersionTestCase(TestCase):
    def test_has_proper_version(self):
        expect(__version__).to_equal("0.1.0")
