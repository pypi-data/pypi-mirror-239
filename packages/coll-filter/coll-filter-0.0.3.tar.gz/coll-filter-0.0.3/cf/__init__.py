#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""coll filter"""

import os
import math
from typing import Iterable, Tuple, List


def default_similar_func(items: List[str], other: List[str]) -> float:
    """两个item并集数"""
    return 1.0 / float(len(set(items + other)))


def sqrt_similar_func(items: List[str], other: List[str]) -> float:
    """两个item数相乘开根"""
    return 1.0 / math.sqrt(len(items) * len(other))


class CollFilter:

    def __init__(self, data: Iterable[Tuple[str, str, float]], process_num=os.cpu_count(),
                 similar_func=default_similar_func):
        if process_num > 0:
            from cf.pool_coll_filter import PollCollFilter
            self.coll_filter = PollCollFilter(data, process_num, similar_func)
        else:
            from cf.base import BaseCollFilter
            self.coll_filter = BaseCollFilter(data, similar_func)

    def user_cf(self, size_per_user=5):
        """
        用户协同过滤

        @param size_per_user  每个用户推荐结果数目
        @return {user_id: [(item, score),],}
        """
        return self.coll_filter.user_cf(size_per_user)

    def item_cf(self, size_per_user=5):
        """
        物品协同过滤

        @param size_per_user  每个用户推荐结果数目
        @return {user_id: [(item, score),],}
        """
        return self.coll_filter.item_cf(size_per_user)
