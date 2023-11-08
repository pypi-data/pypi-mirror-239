#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 
# @Author   : wgh
import time

from fourth_dimension.config.config import config_setting, tokenizer, model
from fourth_dimension.es.es_client import ElasticsearchClient
from fourth_dimension.faiss_process.faiss_index import faiss_search_topk_IndexFlatL2
from fourth_dimension.faiss_process.faiss_storage import embeddings_storage
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
    all_contexts = get_all_docx_contexts(doc_path)
    if search_method == elasticsearch:
        return all_contexts
    elif search_method == faiss or search_method == elasticsearch_faiss:
        all_doc_embeddings = embeddings_storage(all_contexts)
        return [all_contexts, all_doc_embeddings]


def query(question, data):
    if search_method == elasticsearch:
        top_k_context = es_query(question, data[0])
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
    es_client = ElasticsearchClient()
    es_client.create_index(index_name)
    es_client.insert_data(index_name, contexts)
    top_k_context = es_client.es_search(question, index_name)
    return top_k_context


def faiss_query(question, embed_data):
    top_k_context = faiss_search_topk_IndexFlatL2(question, embed_data)
    return top_k_context


def es_faiss_query(question, embed_data):
    es_client = ElasticsearchClient()
    es_top_k_contexts = es_client.es_search(question, index_name)
    faiss_top_k_contexts = faiss_search_topk_IndexFlatL2(question, embed_data)
    merged_top_k = list(set(es_top_k_contexts + faiss_top_k_contexts))
    rerank_result = rerank(question, merged_top_k)
    return rerank_result


def generate_answers():
    pass


def main(question, doc_path):
    all_contexts = store_data(doc_path)
    top_k_contexts = query(question, all_contexts)
    return top_k_contexts


if __name__ == '__main__':
    st_time = time.time()
    main("工商银行活期存款有什么服务特色", '../data/231102_test')
    end_time = time.time()
    cost_time = end_time - st_time
    print('用时：' + str(cost_time))
    exit(0)
