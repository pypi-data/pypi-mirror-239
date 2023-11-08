#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 
# @Author   : wgh


"""
文件说明：
"""
import os

from docx import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter


def get_docx_files(folder_path):
    docx_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".docx"):
                docx_files.append(os.path.join(root, file))
    return docx_files


def get_docx_contents(docx_files):
    contents = []
    for file_path in docx_files:
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        contents.append(text)
    return contents


def compute_documents_local(documents):
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )

    documents = text_splitter.split_documents(documents)
    print(documents)

