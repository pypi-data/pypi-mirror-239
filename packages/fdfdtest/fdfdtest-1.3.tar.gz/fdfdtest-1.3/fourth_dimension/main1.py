#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 
# @Author   : wgh
import json
import time

from fourth_dimension.config.config import config_setting, tokenizer, model
from fourth_dimension.es.es_client import ElasticsearchClient
from fourth_dimension.faiss_process.faiss_index import faiss_search_topk_IndexFlatL2
from fourth_dimension.faiss_process.faiss_storage import embeddings_storage
from fourth_dimension.model.chatGPT import answer_generate
from fourth_dimension.utils.file_parse import get_all_docx_contexts
from fourth_dimension.utils.mix_sort import rerank

"""
文件说明：
"""
word_storage = config_setting['word_storage']
embedding_storage = config_setting['embedding_storage']
search_method = config_setting['search_method']
index_name = config_setting['elasticsearch_setting']['index_name']

elasticsearch = 'elasticsearch'
faiss = 'faiss'
elasticsearch_faiss = 'elasticsearch+faiss'


def store_data(doc_path):
    """
    数据存储
    :param doc_path: 文档路径
    :return:
    """
    all_contexts = get_all_docx_contexts(doc_path)
    if search_method == elasticsearch:
        return all_contexts
    elif search_method == faiss or search_method == elasticsearch_faiss:
        all_doc_embeddings = embeddings_storage(all_contexts)
        return [all_contexts, all_doc_embeddings]


def query_entrance(question, data):
    """
    查询入口
    :param question: 问题
    :param data: 段落数据
    :return:
    """
    if search_method == elasticsearch:
        top_k_context = es_query(question, data)
        return top_k_context
    elif search_method == faiss:
        top_k_context = faiss_query(question, data[1])
        return top_k_context
    elif search_method == elasticsearch_faiss:
        es_client = ElasticsearchClient()
        es_client.insert_data(index_name, data[0])
        top_k_rerank_result = es_faiss_query(question, data[1])
        return top_k_rerank_result


def es_query(question, contexts):
    """
    es查询
    :param question: 问题
    :param contexts: 段落
    :return:
    """
    es_client = ElasticsearchClient()
    es_client.create_index(index_name)
    es_client.insert_data(index_name, contexts)
    top_k_context = es_client.es_search(question, index_name)
    return top_k_context


def faiss_query(question, embed_data):
    """
    faiss查询
    :param question: 问题
    :param embed_data: embedding结果
    :return:
    """
    top_k_context = faiss_search_topk_IndexFlatL2(question, embed_data)
    return top_k_context


def es_faiss_query(question, embed_data):
    """
    es+faiss重排查询
    :param question: 问题
    :param embed_data: embedding结果
    :return:
    """
    es_client = ElasticsearchClient()
    es_top_k_contexts = es_client.es_search(question, index_name)
    faiss_top_k_contexts = faiss_search_topk_IndexFlatL2(question, embed_data)
    merged_top_k = list(set(es_top_k_contexts + faiss_top_k_contexts))
    rerank_result = rerank(question, merged_top_k)
    return rerank_result


def generate_answers(question, data):
    """
    答案生成
    :param question: 问题
    :param data: 召回结果
    :return:
    """
    answer = answer_generate(question, data)
    return answer


def query(question, doc_path):
    """
    查询接口
    :param question: 问题
    :param doc_path: 文档路径
    :return:
    """
    all_contexts = store_data(doc_path)
    top_k_contexts = query_entrance(question, all_contexts)
    answer = generate_answers(question, top_k_contexts)
    return answer


if __name__ == '__main__':
    st_time = time.time()
    # print(query("工商银行活期存款有什么服务特色", '../data/231102_test'))
    store_data('C:\yantuProject\yantu_rag_tool1\data\doc_497')
    end_time = time.time()
    cost_time = end_time - st_time
    print('用时：' + str(cost_time))
    exit(0)
