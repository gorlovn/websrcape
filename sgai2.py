#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 10:35 2024

Load graph config from file
and scrape web site

@author: gnv
"""

import os
import logging

from helpers import setup_logger

if __name__ == "__main__":
    log = setup_logger('', '_sgai2.out', console_out=True)
else:
    log = logging.getLogger(__name__)

CWD = os.getcwd()
DATA_PATH = os.path.join(CWD, 'data')
GRAPH_CONFIG_FILE_NAME = 'graph_config_1.json'
RESULTS_FILE = 'scrape_results.json'


def main(_url, _prompt,
         _config_file=GRAPH_CONFIG_FILE_NAME,
         _results_file=RESULTS_FILE):
    import time
    import json
    from scrapegraphai.graphs import SmartScraperGraph
    import nest_asyncio  # Import nest_asyncio module for asynchronous operations

    nest_asyncio.apply()  # Apply nest_asyncio to resolve any issues with asyncio event loop

    _config_path = os.path.join(DATA_PATH, _config_file)
    if not os.path.isfile(_config_path):
        log.error(f"Config file {_config_path} was not found")
        return None

    with open(_config_path, 'r') as json_file:
        _graph_config = json.load(json_file)

    _start = time.time()

    log.info(f"Scrape site: {_url}")
    log.info(f"Prompt: {_prompt}")
    _llm = _graph_config.get('llm', {})
    _model = _llm.get('model')
    log.info(f"Model: {_model}")

    smart_scraper_graph = SmartScraperGraph(prompt=_prompt, source=_url, config=_graph_config)

    result = smart_scraper_graph.run()
    if type(result) is dict:
        _j_text = json.dumps(result, indent=4, sort_keys=True, default=str, ensure_ascii=False)
        _result_path = os.path.join(DATA_PATH, _results_file)
        with open(_result_path, 'w+') as _f:
            _f.write(_j_text)
        log.info(f"File {_result_path} has been written")
    else:
        log.info(f"Result: {result}")

    _dur = (time.time() - _start) * 1000
    log.info(f"Duration: {_dur:.2f} ms")
    return result


if __name__ == "__main__":
    """
    1. URL
    2. PROMPT
    """
    import sys

    url = "https://perinim.github.io/projects"
    prompt = "List me all the news with their description."

    n_args = len(sys.argv)
    if n_args > 1:
        url = sys.argv[1]
        if n_args > 2:
            prompt = sys.argv[2]

    rr = main(url, prompt)

    sys.exit(0)
