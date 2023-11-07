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
import threading
from aiges.core.types import *
try:
    from aiges_embed import ResponseData, Response, DataListNode, DataListCls  # c++
except:
    from aiges.dto import Response, ResponseData, DataListNode, DataListCls

from aiges.sdk import WrapperBase, \
    ImageBodyField, \
    StringBodyField, StringParamField
from aiges.utils.log import log, getFileLogger

try:
    from aiges_embed import callback_metric
except:
    callback_metric=None

# 定义模型的超参数和输入参数
class UserRequest(object):
    input1 = StringBodyField(key="text", value=b"I have a problem with my iphone that needs to be resolved asap!!")


# 定义模型的输出参数
class UserResponse(object):
    accept1 = StringBodyField(key="result")


# 定义服务推理逻辑
class Wrapper(WrapperBase):
    serviceId = "effcient"
    version = "v1"
    requestCls = UserRequest()
    responseCls = UserResponse()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filelogger = None
        self.model = None
        self.tokenizer = None
        self.patch_id = {}
        self.first_load_lora = True
        self.lock = threading.Lock()

    def wrapperInit(self, config: {}) -> int:
        #log.info("Initializing ...")
        from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer
        tokenizer_path = os.environ.get("TOKENIZER_PATH")
        base_model = os.environ.get("MODEL_PATH")
        self.pretrained_name = os.environ.get("PRETRAINED_MODEL_NAME")

        if not self.pretrained_name: 
            log.error("should have environ(PRETRAINED_MODEL_NAME,MODEL_PATH(lora weight dir）,TOKENIZER_PATH)")
            return -1

        # 加载基础模型
        #base_model = f"/home/.atp/models/{self.pretrained_name}"
        #tokenizer_path = f"/home/.atp/models/{self.pretrained_name}"
        if not os.path.isdir(base_model):
            log.error(f"not find the base_model in {base_model}")
            return -1
        if not base_model or not tokenizer_path:
            log.error("should have environ(FULL_MODEL_PATH,(base or full ）,TOKENIZER_PATH)")
            return -1


        tokenizer = AutoTokenizer.from_pretrained(tokenizer_path, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(base_model, device_map="auto", trust_remote_code=True)

        self.model = model
        self.tokenizer = tokenizer
        self.filelogger = getFileLogger()
        self.filelogger.info("wrapperInit end")
        return 0

    def checkValidLora(self, pretrained_name, lora_path):
        import json
        confjson = "adapter_config.json"
        if not os.path.isdir(lora_path):
            msg = "not find  %s"%lora_path
            log.error(msg)
            return False, msg
        files = os.listdir(lora_path)
        if not confjson in files:
            msg = "%s doesnt have file adapter_config.json" % lora_path
            log.error(msg)
            return False, msg
        fp = open(os.path.join(lora_path, confjson),'rb')
        conf = json.load(fp)
        base_model_path = conf.get("base_model_name_or_path","")
        if not base_model_path:
            msg = "config json not contains base_model_name_or_path...c=" % lora_path
            log.error(msg)
            return False, msg
        user_pretrained_name = os.path.basename(base_model_path)
        if pretrained_name != user_pretrained_name.strip():
            msg = f"current runntime model is {pretrained_name}, but you pass the {user_pretrained_name}, Error"
            log.error(msg)
            return False, msg
        else:
            return True, "Check Success..."


    def wrapperLoadRes(self, reqData: DataListCls, patch_id: int) -> int:
        from peft import PeftModel
        if patch_id in self.patch_id:
            log.warn("patch_id has exist.Please first to UnloadRes")
            return 0
        lora_weight_path = "/home/.atp/lora_weight/"
        lora_weight_path = os.path.join(lora_weight_path, str(patch_id))
        if os.path.exists(lora_weight_path):
            log.warn("zip file has exist.Please first to UnloadRes")

        import io
        import zipfile
        byte_stream = io.BytesIO(reqData.list[0].data)
        # 解压缩 zip 文件到指定目录
        with zipfile.ZipFile(byte_stream, 'r') as zip_ref:
            zip_ref.extractall(lora_weight_path)

        #valid, msg = self.checkValidLora(self.pretrained_name, lora_weight_path)
        #if not valid:
        #    return -1
        #log.info(msg)
        self.lock.acquire()
        adapter_name = str(patch_id)
        if self.first_load_lora == True:
            self.model = PeftModel.from_pretrained(self.model, lora_weight_path, adapter_name=adapter_name)
            self.first_load_lora = False
        else:
            self.model.load_adapter(lora_weight_path, adapter_name)

        self.patch_id[patch_id] = lora_weight_path
        self.lock.release()
        log.info("Load Resource Successfully...")
        return 0




    def wrapperUnloadRes(self, presid: int) -> int:
        if presid not in self.patch_id:
            log.error("patch_id not exist")
            return 0 
        lora_weight_path = self.patch_id[presid]
        if not os.path.exists(lora_weight_path):
            log.error("lora weigth path not exist")
            return 0
        
        self.lock.acquire()
        import shutil
        shutil.rmtree(lora_weight_path)
        del self.patch_id[presid]
        self.lock.release()
        return 0

    def _base_model_inference(self, reqData: DataListCls) -> str:
        tokenizer = self.tokenizer
        model = self.model

        input_text = reqData.get("text").data.decode('utf-8')
        self.filelogger.info("got input_text , %s" % input_text)
        model_name = self.pretrained_name
        from ailab.atp_finetuner.constant import Model
        prompt_model = [Model.atom_7b]
        if model_name in prompt_model:
            from ailab.utils.template import Template
            template_dict = {
                Model.atom_7b: "atom_7b",
            }
            prompt_template = Template(template_dict.get(model_name))
            history = []
            input_text = prompt_template.get_prompt(input_text, history, "")
        inputs = tokenizer(input_text, return_tensors='pt')
        input_text_skip_st = tokenizer.decode(inputs.input_ids[0], skip_special_tokens=True)
        gen_kwargs = {
                "max_new_tokens": 512,
                "repetition_penalty": 1.1,
            }

        input_ids_model = [Model.xverse_13b,Model.falcon_7b,Model.llama2_7b]

        if hasattr(model, 'disable_adapter'):
            with model.disable_adapter():
                inputs = inputs.to(model.device)
                output = model.generate(**inputs, **gen_kwargs)
                output = tokenizer.decode(output[0], skip_special_tokens=True)
                if output.startswith(input_text_skip_st):
                    output = output[len(input_text_skip_st):]
                output = output.strip()
                return output
        else:
            if model_name in input_ids_model:
                inputs = inputs.input_ids
                inputs = inputs.to(model.device)
                output = model.generate(inputs, **gen_kwargs)
            else:
                inputs = inputs.to(model.device)
                output = model.generate(**inputs, **gen_kwargs)
            output = tokenizer.decode(output[0], skip_special_tokens=True)
            if output.startswith(input_text_skip_st):
                output = output[len(input_text_skip_st):]
            output = output.strip()
            return output

    def _lora_model_infence(self, reqData: DataListCls, patch_id:int) -> str:
        if patch_id not in self.patch_id:
            log.error("patch_id not exist")
            return None
        model_name = self.pretrained_name
        tokenizer = self.tokenizer
        model = self.model
        lora_weight = self.patch_id[patch_id]
        model.load_adapter(lora_weight,patch_id)
        model.set_adapter(str(patch_id))

        input_text = reqData.get("text").data.decode('utf-8')
        self.filelogger.info("got input_text , %s" % input_text)

        from transformers import TextIteratorStreamer
        from ailab.utils.template import get_template_and_fix_tokenizer
        from ailab.atp_finetuner.constant import Model
        from threading import Thread
        import torch

        template_dict = {
            Model.baichuan_7b : "default",
            Model.baichuan_13b : "default",
            Model.bloomz_7b1_mt : "default",
            Model.falcon_7b : "default",
            Model.moss_moon_003_base : "moss",
            Model.llama2_7b : "llama2",
            Model.internlm_7b : "default",
            Model.belle_7b_2m : "belle",
            Model.xverse_13b : "vanilla",
            Model.lawgpt_llama : "alpaca",
            Model.atom_7b: "atom",
            Model.chatglm3_6b: "chatglm3",
        }

        prompt_template = get_template_and_fix_tokenizer(template_dict.get(model_name),tokenizer)
        def predict_and_print(query) -> list:
            history = []
            prompt, _ = prompt_template.encode_oneturn(tokenizer=tokenizer, query=query, 
                                                       resp="", history=history, system=None)
            input_ids = torch.tensor([prompt], device=model.device)

            streamer = TextIteratorStreamer(tokenizer, timeout=60.0, skip_prompt=True, skip_special_tokens=True)
            gen_kwargs = {
                "input_ids": input_ids,
                "streamer": streamer,
                "do_sample": True,
                "temperature": 0.95,
                "top_p": 0.7,
                "top_k": 50,
                "num_beams": 1,
                "max_new_tokens": 512,
                "repetition_penalty": 1.0,
                "length_penalty": 1.0,
            }

            thread = Thread(target=model.generate, kwargs=gen_kwargs)
            thread.start()

            response = ""
            for new_text in streamer:
#                print(new_text, end="", flush=True)
                response += new_text
#            print()

            return response

        result = predict_and_print(input_text)
        return result

    def wrapperOnceExec(self, params: {}, reqData: DataListCls, usrTag:str="",persId: int = 0) -> Response:
        patch_id = params.get("atp_patch_id", 0)
        self.filelogger.info("got reqdata , %s" % reqData.list)
        self.lock.acquire()
        if patch_id == 0 or patch_id == "0":
            result = self._base_model_inference(reqData)
        else:
            result = self._lora_model_infence(reqData, patch_id)
        self.lock.release()
        res= Response()
        if not result:
            self.filelogger.info("no result")
            return res.response_err(100)

        self.filelogger.info("got result , %s" % result)
        # 使用Response封装result
        resd = ResponseData()
        resd.key = "result"
        resd.setDataType(DataText)
        resd.status = Once
        resd.setData(result.encode("utf-8"))
        self.filelogger.info("###")

        self.filelogger.info(result)
        if callback_metric:
            ret = callback_metric(usrTag, "business.total", 1)
            self.filelogger.info("calc business.total, count: %d " %ret)
        res.list = [resd]
        return res

    def wrapperFini(cls) -> int:
        return 0

    def wrapperError(cls, ret: int) -> str:
        if ret == 100:
            return "no result.."
        return ""

    '''
        此函数保留测试用，不可删除
    '''

    def wrapperTestFunc(cls, data: [], respData: []):
        pass


    def testLoad(self,patch_id):
        from peft import PeftModel
        lora_weight_path = "/home/.atp/lora_weight/"
        lora_weight_path = os.path.join(lora_weight_path, str(patch_id))
        if self.first_load_lora == True:
            self.model = PeftModel.from_pretrained(self.model, lora_weight_path, adapter_name=patch_id)
            self.first_load_lora = False
        else:
            self.model.load_adapter(lora_weight_path, patch_id)
        self.patch_id[patch_id] = lora_weight_path
        self.model.eval()


    def run_once_test(self):
        # 1. 模拟调用初始化引擎
        #  传入配置当前模拟为空
        self.wrapperInit(self.config)
        self.testLoad("1111")
        #import pdb
        #pdb.set_trace()

        try:
            # 2. 准备wrapperOnceExec需要的数据
            inputs_fields, inputs_body = self._parse_inputs()

            params_fields, required_params = self._parse_params()
            params = self.params_test_values
            reqData = []
            reqData.append(self.inputs_test_values)
            req = DataListCls()
            tmp = []
            for key, value in self.inputs_test_values.items():
                node = DataListNode()
                node.key = key
                node.data = value
                node.len = len(value)
                typeStr = inputs_fields[key]["dataType"]
                node.type = 0
                tmp.append(node)

            req.list = tmp
            # 3. 模拟调用 exec，并返回数据
#            response = self.wrapperOnceExec(params, req)
            params['atp_patch_id'] = '0'
            response = self.wrapperOnceExec(params, req)
            params['atp_patch_id'] = '1111'
            response = self.wrapperOnceExec(params, req)
            params['atp_patch_id'] = '0'
            response = self.wrapperOnceExec(params, req)
            if self.check_resp(response):
                log.info("wrapper.py has been verified... Congratulations ...!")
            else:
                log.error("Sorry, Please Check The Log Output Above ...")
        except Exception as e:
            # 4. 模拟检查 wrapperOnceExec返回
            log.error(e)
            self.wrapperError(-1)


if __name__ == '__main__':
    m = Wrapper()
    m.run()


