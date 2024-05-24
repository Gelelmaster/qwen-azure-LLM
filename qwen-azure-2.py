from dashscope import Generation
from dashscope.api_entities.dashscope_response import Role
from typing import List, Dict
import azure.cognitiveservices.speech as speechsdk
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr

# Azure语音服务的API密钥和服务区域
speech_key = "144b2266024a4df29a7bf25d3b65e9f0"
service_region = "eastus"

# 初始化Azure语音服务客户端
def text_to_speech(text):
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = speechsdk.audio.AudioOutputConfig(filename="output.wav")
    # 创建语音合成器
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    # 合成语音并保存到文件
    result = synthesizer.speak_text_async(text).get()
    # 检查结果
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("语音输出中...")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"语音合成被取消: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"错误详情: {cancellation_details.error_details}")

def play_audio(file_path):
    # 使用soundfile加载音频文件
    data, fs = sf.read(file_path, dtype='float32')
    # 使用sounddevice播放音频
    sd.play(data, fs)
    sd.wait()  # 等待音频播放完成

#语音识别转文字
def recognize_speech():
    # 初始化识别器
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("请说话...")
        # 记录音频
        audio = r.listen(source)
    try:
        # 使用Google Web Speech API进行识别，它对中英文混合语音有较好的支持
        text = r.recognize_google(audio, language='zh-CN,en-US')
        print("语音识别中...")
        print(text)
        return text
    except sr.UnknownValueError:
        return False
    except sr.RequestError as e:
        return False

def should_exit(message):
    # 定义一个函数判断是否收到结束指令
    return message.lower() == '结束'

messages = []

def listen_for_input(messages: List[Dict]) -> str:
    #监听用户的语音输入，识别后添加至对话历史记录中并返回识别的文本
    message = recognize_speech()
    messages.append({'role': 'user', 'content': message})
    return message

def generate_reply(messages: List[Dict]) -> str:
    #根据对话历史调用AI模型生成回复，将回复内容追加到对话历史并返回完整回复文本
    responses = Generation.call(Generation.Models.qwen_turbo, messages=messages, result_format='message', stream=True, incremental_output=True)
    whole_message = ''
    print('通义千问:', end='')
    for response in responses:
        content = response.output.choices[0]['message']['content']
        whole_message += content
        print(content, end='')
    print()
    messages.append({'role': 'assistant', 'content': whole_message})
    return whole_message

def speak_reply(reply_content: str) -> None:
    #将AI生成的文本回复转换为语音并播放
    text_to_speech(reply_content)
    play_audio("output.wav")

def main_loop() -> None:
    #执行主对话循环逻辑，包括监听用户输入、判断退出条件、生成及播放AI回复
    messages = []
    while True:
        user_message = listen_for_input(messages)
        # 检查是否为退出指令
        if should_exit(user_message):
            print("对话结束，程序即将退出。")
            break
        assistant_reply = generate_reply(messages)
        speak_reply(assistant_reply)

if __name__ == "__main__":
    main_loop()
