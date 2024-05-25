import azure.cognitiveservices.speech as speechsdk

# API密钥
speech_key = "speech_key"
service_region = "service_region"
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
