#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
from typing import Iterable, Mapping, Collection, Tuple


def read_data(path: str) -> Iterable[str]:
    with open(path) as f:
        lines = f.readlines()
    return lines


def handle_line(line: str) -> (str, str, float):
    user_id, item_id, score = line.strip().split(",")
    return user_id.strip(), item_id.strip(), float(score.strip())


def pre_process(data: Iterable[str], handle_func=handle_line) -> Iterable[str]:
    return map(handle_func, data)


def print_cost_time(task_content, start_time):
    print(f"{task_content}: {round(time.time()-start_time, 2)} seconds.")