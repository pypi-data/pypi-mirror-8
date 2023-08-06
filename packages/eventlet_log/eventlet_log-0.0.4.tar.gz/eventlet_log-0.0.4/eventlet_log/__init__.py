# -*- coding: utf-8 -*-

from __future__ import absolute_import

from .simple import create_logger, create_file_logger, \
                    switch_keeping_filehandlers, \
                    stop_file_logger


__all__ = ('create_logger',
           'create_file_logger',
           'stop_file_logger',
           'switch_keeping_filehandlers')
