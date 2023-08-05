# -*- coding: utf-8 -*-
"""
A decorator to register events into log. Created on Fev 11, 2014

"""

__author__ = "joaonrb"

from recommendation.simple_logging.models import LogEntry, LOGGER_MAX_LOGS
from recommendation.decorators import ILogger
from recommendation.models import Item, User
from recommendation.decorators import GoToThreadQueue
import functools
from collections import deque


class LogEvent(ILogger):
    """
    Log invents into database
    """

    CLICK = LogEntry.CLICK
    ACQUIRE = LogEntry.INSTALL
    REMOVE = LogEntry.REMOVE
    RECOMMEND = LogEntry.RECOMMEND

    def __init__(self, log_type, *args, **kwargs):
        super(LogEvent, self).__init__(*args, **kwargs)
        self.log_type = log_type
        if self.log_type == self.RECOMMEND:
            self.do_call = self.log_recommendation
        else:
            self.do_call = self.std

    @GoToThreadQueue()
    def bulk_load(self, user, recommendation):
        new_logs = [
            LogEntry(user=user, item_id=iid, type=self.log_type, value=i)
            for i, iid in enumerate(recommendation, start=1)
        ]
        LogEntry.objects.bulk_create(new_logs)
        LogEntry.add_logs(user, new_logs)

    def log_recommendation(self, function):
        """
        Record a recommendation to the database
        """
        @functools.wraps(function)
        def decorated(*args, **kwargs):
            user = kwargs["user"]
            result = function(*args, **kwargs)
            self.bulk_load(user, result)
            return result
        return decorated

    def std(self, function):
        @functools.wraps(function)
        def decorated(*args, **kwargs):
            user, item = args[0], args[1]
            result = function(*args, **kwargs)
            #GoToThreadQueue()(
            #    LogEntry.objects.create
            #)(user_id=uid, item=Item.get_item_by_external_id(iid], type=self.log_type)
            LogEntry.objects.create(user=user, item=item, type=self.log_type)
            return result
        return decorated

    def __call__(self, function):
        return self.do_call(function)