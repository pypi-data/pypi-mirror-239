#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 
# @Author   : wgh


"""
文件说明：
"""
import os

import faiss
import numpy as np

from fourth_dimension.config.config import config_setting, tokenizer, model
from fourth_dimension.utils.embddings import get_question_embeddings

top_k = config_setting['recall_config']['top_k']


def faiss_search_topk_IndexFlatL2(question, embed_data):
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
    index = faiss.read_index('../data/faiss_cache/index.index')
    index.nprobe = 10
    results = []  # 存储结果的列表

    # 批量检索与问题最相关的上下文
    question_embedding = get_question_embeddings(question, tokenizer, model)
    query_embeddings = np.array([question_embedding])
    distances, indices = index.search(query_embeddings, top_k)  # 使用Faiss索引进行检索

    # 按照相关性从大到小排序上下文：
    sorted_indices = indices[0][np.argsort(distances[0])]
    top_k_context = [embed_data[i]["context"] for i in sorted_indices]
    return top_k_context
