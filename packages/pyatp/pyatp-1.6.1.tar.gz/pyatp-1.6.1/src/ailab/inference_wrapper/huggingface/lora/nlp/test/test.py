from aiges.dto import Response, ResponseData, DataListNode, DataListCls

"""personal param"""
model_name = 'vicuna'
pretrain_model_name = '/home/sdk_models/llama-7b-hf/'
token_path = '/home/sdk_models/llama-7b-hf/'
zip_path = '/home/finetuned_models/my_chinese_llama_vicuna_model/adapter.zip'
module_name = 'alpaca'
""""""

import sys
print(sys.path)

import importlib
module_path = f'ailab.inference_wrapper.huggingface.lora.nlp.{module_name}.wrapper.wrapper'
wrapper_module = importlib.import_module(module_path)
Wrapper = getattr(wrapper_module, 'Wrapper')
wrapper = Wrapper()

def Init():
    import os
    os.environ['PRETRAINED_MODEL_NAME'] = model_name
    os.environ['MODEL_PATH'] = pretrain_model_name
    os.environ['TOKENIZER_PATH'] = token_path
    wrapper.wrapperInit({})

def LoadRes(key):
    zip_file_path = zip_path
    with open(zip_file_path, 'rb') as zip_file:
        # 读取压缩包的二进制数据
        zip_data = zip_file.read()
        # 计算数据长度
        zip_data_length = len(zip_data)

    list_node = DataListNode()
    list_node.key = str(key)
    list_node.data = zip_data
    list_node.len = zip_data_length

    req_data = DataListCls()
    req_data.list.append(list_node)
    wrapper.wrapperLoadRes(req_data, key)

def Once(key, text):
    http_node = DataListNode()
    http_node.key = 'text'
    text_data = text
    text_data = text_data.encode('utf-8')
    http_node.data = text_data 
    http_data = DataListCls()
    http_data.list.append(http_node)

    import os
    os.environ['PetrainedModel'] = model_name
    wrapper.wrapperOnceExec({"atp_patch_id":key}, http_data, key)

def UnloadRes(key):
    wrapper.wrapperUnloadRes(key)


if __name__ == '__main__' :
    Init()
    LoadRes('1')
    Once('0', 'what is NLP')
    Once('1', 'what is NLP')
    UnloadRes('1')


