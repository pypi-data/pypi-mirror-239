## 什么是第四维度？
Fourth-Dimension是言图科技提供的以Python语言编写的应用程序库，以实现对Yantu API便捷访问。它包括一个用于初始化的API资源的预定义类集，可以方便地访问Yantu API，以高效地使用言图私域知识库、言图文档问答等功能。此外，Fourth-Dimension还提供了一套本地部署方法。

## 产品特点
可在线使用Yantu API或本地部署专属知识库，自定义embedding和答案生成模型，根据自己的需求进行定制和优化。

## 主要功能
* 简单高效，用户只需配置专属密钥即可使用yantu API
* 高度定制化和数据安全的私域知识库
* 言图智能业务机器人
* 基于私域知识库的文档问答
* 简单易用的本地化部署流程

## 存储/检索方式
* elasticsearch
* faiss
* elasticsearch+Faiss

## 答案生成模型
* gpt-3.5-turbo-16k

## 版本说明
* Python 3.8
* Elasticsearch 7.17.7
* Faiss 1.7.4


## 如何安装
### 创建虚拟环境
确保存在可用的虚拟环境，若没有可根据以下命令进行创建
```
conda create --name 您的虚拟环境名 python=3.8
```

### 安装第四维度  
通过pip安装：
```
pip install Fourth-Dimension
```
或通过源码安装：
```
pip setup.py install
```


### 本地部署
#### Elasticsearch


#### BGE


## 配置文件说明
```json
{
  //文档文本存储方式
  "word_storage": "elasticsearch",
  //文档向量存储方式
  "embedding_storage": "faiss_process",
  //检索方式选择
  "search_select": "elasticsearch",
  //embedding模型
  "embedding_model": "bge-large-zh-v1.5",
  //答案生成模型
  "answer_generation_model": "gpt-3.5-turbo-16k",
  //文档划分设置
  "para_config": {
    //文档划分段落长度
    "chunk_size": 500,
    //文档划分重叠度
    "overlap": 20
  },
  //召回设置
  "recall_config": {
    //指定使用多少召回结果进行答案生成
    "top_k": 10
  },
  //Elasticsearch设置
  "elasticsearch_setting": {
    "host": "localhost",
    "port": 9200,
    //若存在安全认证，则填写用户名和密码
    "username": "",
    "password": "",
    //Elasticsearch分词器
    "analyzer": "standard"
  },
  //Faiss设置
  "faiss_setting": {
    //索引方式
    "retrieval_way": "IndexFlatL2"
  }
}
```

## 示例代码
```python
import fourth_dimension

answer = fourth_dimension.query("您的问题", '文档路径')
```