# -*- coding: utf-8 -*-

__author__ = 'luckydonald'

import logging
logger = logging.getLogger(__name__)

from eyed3.id3.tag import AccessorBase

def overwrite_if_not(tag, field, default):
	"""
	Set or get values.
	:param tag:
	:param field:
	:param default: The value to write. NOTE: on .set() values this is interpreted as *args.
	:param needs_setter:
	:return:
	"""
	logger.debug("Checking tag.{attribute}".format(attribute=field))
	if hasattr(tag, field):
		if not getattr(tag, field):
			logger.debug("Appears to be empty...")
			if isinstance(getattr(tag, field), AccessorBase):
				logger.debug("Setting value with accessor.set()..")
				getattr(tag, field).set(*default)
			else:
				logger.debug("Setting value..")
				setattr(tag, field, default)
		else:
			if isinstance(getattr(tag, field), AccessorBase):
				logger.debug("(Accessor) Was already set to {value}.".format(value=list(getattr(tag, field))))
			else:
				logger.debug("Was already set to {value}.".format(value=getattr(tag, field)))
	else:
		raise AttributeError("No attribute {attribute}".format(attribute=field))