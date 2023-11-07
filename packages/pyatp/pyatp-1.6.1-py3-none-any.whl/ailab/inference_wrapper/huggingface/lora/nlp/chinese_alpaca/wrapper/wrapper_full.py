#!/usr/bin/env python
# coding:utf-8
"""
@license: Apache License2
@file: wrapper.py
@time: 2022-08-19 02:05:07.467170
@project: mnist
@project: ./
"""
import os.path
from aiges.core.types import *
try:
    from aiges_embed import ResponseData, Response, DataListNode, DataListCls  # c++
except:
    from aiges.dto import Response, ResponseData, DataListNode, DataListCls

from aiges.sdk import WrapperBase, \
    ImageBodyField, \
    StringBodyField, StringParamField

try:
    from aiges_embed import callback_metric
except:
    callback_metric=None

from aiges.utils.log import log, getFileLogger
import threading
import torch
import copy
from peft import PeftModel


# 定义模型的超参数和输入参数
class UserRequest(object):
    input1 = StringBodyField(key="text", value='''这道试题类型属于 判断推理，类比推理，逻辑关系，逻辑关系-并列关系中的一种。 试题: QQ：微信：FaceBook
 请从下列选项选出一个最恰当的答案: A. 手提电脑：打印机：数字电视
B. 微博：论坛：互联网
C. 人民日报：工人日报：光明日报
D. 医生：护士：患者
'''.encode('utf-8'))
    input2 = StringParamField(key="atp_patch_id", value="179387562041344")


# 定义模型的输出参数
class UserResponse(object):
    accept1 = StringBodyField(key="result")


# 定义服务推理逻辑
class Wrapper(WrapperBase):
    serviceId = "chinese_alpaca"
    version = "v1"
    requestCls = UserRequest()
    responseCls = UserResponse()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filelogger = None
        self.lock = threading.Lock()

    def wrapperInit(self, config: {}) -> int:
        logger = log

        logger.info("Initializing ...")
        from transformers import LlamaTokenizer, LlamaForCausalLM,AutoModelForCausalLM
        base_model_path = os.environ.get("PRETRAINED_MODEL_NAME")
        base_tokenizer_path = os.environ.get("TOKENIZER_PATH")
        full_model_path = os.environ.get("FULL_MDOEL_PATH")
        if not base_model_path or not base_tokenizer_path or not full_model_path:
            log.error("should have environ(PRETRAINED_MODEL_NAME,MODEL_PATH(lora weight dir）,TOKENIZER_PATH)")
            return -1


        if not os.path.isdir(base_model_path):
            log.error(f"not find the base_model in {base_model_path}")
            return -1
        
        def load_model_tokenizer(model_path, tokenizer_path):
            load_type = torch.float16
            tokenizer = LlamaTokenizer.from_pretrained(tokenizer_path)

            if (len(tokenizer)) == 55296: #v2 49954:v1
                from ailab.utils.attn_and_long_ctx_patches import apply_attention_patch, apply_ntk_scaling_patch
                apply_attention_patch(use_memory_efficient_attention=True)
                apply_ntk_scaling_patch(1.0)

            model = LlamaForCausalLM.from_pretrained(
                model_path,
                load_in_8bit=False,
                torch_dtype=load_type,
                low_cpu_mem_usage=True,
                device_map='auto',
                )

            model_vocab_size = model.get_input_embeddings().weight.size(0)
            tokenzier_vocab_size = len(tokenizer)
            logger.info(f"Vocab of the base model: {model_vocab_size}")
            logger.info(f"Vocab of the tokenizer: {tokenzier_vocab_size}")
            if model_vocab_size!=tokenzier_vocab_size:
                assert tokenzier_vocab_size > model_vocab_size
                logger.info("Resize model embeddings to fit tokenizer")
                model.resize_token_embeddings(tokenzier_vocab_size)
            return model,tokenizer

        self.base_model, self.base_tokenizer = load_model_tokenizer(base_tokenizer_path,base_model_path)
        self.full_model, self.full_tokenizer = load_model_tokenizer(full_model_path,full_model_path)
        self.filelogger = getFileLogger()
        return 0


    def evaluate(self, instruction: str, model , tokenizer) -> str:
        generation_config = dict(
            temperature=0.2,
            top_k=40,
            top_p=0.9,
            do_sample=True,
            num_beams=1,
            repetition_penalty=1.3,
            max_new_tokens=400
            )

        # The prompt template below is taken from llama.cpp
        # and is slightly different from the one used in training.
        # But we find it gives better results
        if (len(tokenizer)) == 49954:
            prompt_input = (
                "Below is an instruction that describes a task. "
                "Write a response that appropriately completes the request.\n\n"
                "### Instruction:\n\n{instruction}\n\n### Response:\n\n"
            )
            def generate_prompt(instruction, input=None):
                if input:
                    instruction = instruction + '\n' + input
                return prompt_input.format_map({'instruction': instruction})
        elif (len(tokenizer)) == 55296:
            prompt_input = (
                "[INST] <<SYS>>\n"
                "{system_prompt}\n"
                "<</SYS>>\n\n"
                "{instruction} [/INST]"
            )
            DEFAULT_SYSTEM_PROMPT = """You are a helpful assistant. 你是一个乐于助人的助手。"""
            def generate_prompt(instruction, system_prompt=DEFAULT_SYSTEM_PROMPT):
                return prompt_input.format_map({'instruction': instruction,'system_prompt': system_prompt})

        with torch.no_grad():
            input_text = generate_prompt(instruction=instruction)
            inputs = tokenizer(input_text,return_tensors="pt")  #add_special_tokens=False ?
            input_ids = inputs["input_ids"].to(model.device)
            attention_mask = inputs['attention_mask'].to(model.device)
            generation_output = model.generate(
                input_ids = input_ids, 
                attention_mask = attention_mask,
                eos_token_id=tokenizer.eos_token_id,
                pad_token_id=tokenizer.pad_token_id,
                **generation_config
            )
            s = generation_output[0]
            output = tokenizer.decode(s,skip_special_tokens=True)
            if (len(tokenizer)) == 49954:
                response = output.split("### Response:")[1].strip()
            else:
                response = output.split("[/INST]")[-1].strip()
            return response

    def _base_model_inference(self, reqData: DataListCls) -> str:
        tokenizer = self.base_tokenizer
        model = self.base_model
            
        input_text = reqData.get("text").data.decode('utf-8')
        self.filelogger.info("got input_text , %s" % input_text)

        return self.evaluate(input_text,model,tokenizer)

    def _full_model_infence(self, reqData: DataListCls) -> str:
        tokenizer = self.full_tokenizer
        #model = self.patch_id_map[adapter_name][0]+
        model = self.full_model

        instruction = reqData.get("text").data.decode('utf-8')
        return self.evaluate(instruction,model,tokenizer)

    def wrapperOnceExec(self, params: {}, reqData: DataListCls, usrTag:str="",persId: int = 0) -> Response:
        patch_id = params.get("atp_patch_id", 0)
        self.filelogger.info("got reqdata , %s, patch_ID %s" %( reqData.list, patch_id))

        self.lock.acquire()
        if patch_id == 0 or patch_id == "0":
            result = self._base_model_inference(reqData)
        else:
            result = self._full_model_infence(reqData)
        self.lock.release()
        res = Response()
        if not result:
            self.filelogger.info("#####")
            return res.response_err(100)
        self.filelogger.info("got result , %s" % result)
        # 使用Response封装result
        resd = ResponseData()
        resd.key = "result"
        resd.setDataType(DataText)
        resd.status = Once
        resd.setData(result.encode("utf-8"))
        print("###")
        self.filelogger.info("###")

        self.filelogger.info(result)
        if callback_metric:
            ret = callback_metric(usrTag, "business.total", 1)
            self.filelogger.info("calc +1 ret: %d"%ret)
        res.list = [resd]
        return res

    def wrapperFini(cls) -> int:
        return 0

    def wrapperError(cls, ret: int) -> str:
        if ret == 100:
            return "not get result...."
        return ""

    '''
        此函数保留测试用，不可删除
    '''

    def wrapperTestFunc(cls, data: [], respData: []):
        pass

if __name__ == '__main__':
    m = Wrapper()
    m.run()
    #print(m.schema())


