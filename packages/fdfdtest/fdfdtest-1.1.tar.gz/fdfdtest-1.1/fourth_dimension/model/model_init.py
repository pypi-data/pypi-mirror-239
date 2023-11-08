#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 
# @Author   : wgh


"""
文件说明：模型初始化
"""
from transformers import AutoTokenizer, AutoModel


def init_model(model_path):
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModel.from_pretrained(model_path)
    print("模型初始化成功，参数量为：", sum([param.nelement() for param in model.parameters()]))
    model.eval()
    model.cuda(0)
    return tokenizer, model
