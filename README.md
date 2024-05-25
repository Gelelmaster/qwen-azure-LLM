# qwen-azure-LLM
本代码基于阿里通义千问大模型和微软Azure LLS运行，Windows环境  
按照阿里官方流程  
https://help.aliyun.com/zh/dashscope/developer-reference/activate-dashscope-and-create-an-api-key
1. 开通DashScope灵积模型服务并创建API-KEY
2. 安装DashScope SDK并更新  
   pip install dashscope  
   pip install dashscope --upgrade  
3. 设置API-KEY，设置地址官方文档网址  
   https://help.aliyun.com/zh/dashscope/developer-reference/api-key-settings  
   不推荐将API-KEY直接写在代码中，会有一定的API-KEY暴露风险，实际应用中，配置的环境变量有时会出现读取不到的情况，此时将API-KEY写在代码中可以使程序正常运行。  
   这里以Windows为例，对当前用户添加永久性环境变量设置通义千问API-KEY：  
   setx DASHSCOPE_API_KEY "YOUR_DASHSCOPE_API_KEY"
   
创建并获取微软Azure语音模型  
https://portal.azure.com/#home  
1. 在Azure AI services | 语音服务 | ID | 资源管理 | 密钥和终结点 里获取你的Azure语音服务的API密钥和服务区域。
2. 安装Azure认知服务SDK：pip install azure-cognitiveservices-speech

之后安装一下需要用到的库：  
pip install numpy  
pip install sounddevice # sounddevice库提供了简单的接口来处理音频的输入输出  
pip install soundfile # 安装soundfile库，用于音频文件的读写操作  
pip install SpeechRecognition # speech_recognition是专为语音识别设计的库。它封装了多种语音识别引擎，能够方便地将音频转换为文本  
