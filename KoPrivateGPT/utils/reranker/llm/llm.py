"""
The original code is from [RankGPT](https://github.com/sunnweiwei/RankGPT).
I modified the code to fit the KoPrivateGPT framework.
"""
import os
from typing import List

from KoPrivateGPT.llm.basic import BasicLLM
from KoPrivateGPT.utils.reranker.base import BaseReranker
from KoPrivateGPT.utils.reranker.llm.rank_gpt import permutation_pipeline, sliding_windows
from KoPrivateGPT.schema import Passage


class LLMReranker(BaseReranker):
    def __init__(self, model_name: str = "gpt-3.5-turbo", api_base: str = None, *args, **kwargs):
        self.model_name = model_name
        self.api_base = api_base
        BasicLLM.set_model(api_base)

    def rerank(self, query: str, passages: List[Passage]) -> List[Passage]:
        items = self.make_item(query, passages)
        new_items = permutation_pipeline(item=items, model_name=self.model_name, api_base=self.api_base,
                                         api_key=os.getenv("OPENAI_API_KEY"))
        return self.make_passages(new_items, passages)

    def rerank_sliding_window(self, query: str, passages: List[Passage], window_size: int) -> List[Passage]:
        items = self.make_item(query, passages)
        new_items = sliding_windows(item=items, model_name=self.model_name, api_base=self.api_base,
                                    api_key=os.getenv("OPENAI_API_KEY"), window_size=window_size)
        return self.make_passages(new_items, passages)

    def make_item(self, query: str, passages: List[Passage]) -> dict:
        hits_list = [{'content': passage.content} for passage in passages]
        return {
            "query": query,
            "hits": hits_list
        }

    def make_passages(self, items: dict, original_passages: List[Passage]) -> List[Passage]:
        content_list = [item['content'] for item in items['hits']]
        return [self.find_passages(original_passages, content) for content in content_list]

    def find_passages(self, target_passages: List[Passage], content: str):
        for target_passage in target_passages:
            if target_passage.content == content:
                return target_passage
        raise ValueError(f"Cannot find the passage with content {content}")
