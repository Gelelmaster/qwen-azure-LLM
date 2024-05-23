from dashscope import Generation
from dashscope.api_entities.dashscope_response import Role
import azure.cognitiveservices.speech as speechsdk
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr

# Azure语音服务的API密钥和服务区域
speech_key = "你的Azure语音服务API密钥"
service_region = "你的服务区域"

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

messages = []

while True:
    message = recognize_speech()
    messages.append({'role': Role.USER, 'content': message})
    whole_message = ''
    responses = Generation.call(Generation.Models.qwen_turbo, messages=messages, result_format='message', stream=True, incremental_output=True)
    print('通义千问:', end='')
    for response in responses:
        whole_message += response.output.choices[0]['message']['content']
        print(response.output.choices[0]['message']['content'], end='')
    print()
    messages.append({'role': 'assistant', 'content': whole_message})

    # 将生成的回复转换为语音并保存为文件
    text_to_speech(whole_message)
    
    # 播放生成的语音
    play_audio("output.wav")
