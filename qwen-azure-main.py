from dashscope import Generation
from dashscope.api_entities.dashscope_response import Role
from recognize_speech import recognize_speech
from text_to_speech import text_to_speech
from play_audio import play_audio

# 定义一个函数判断是否收到结束指令
def should_exit(message):
    return message.lower() == '结束'

def main():
    try:
        messages = []
        while True:
            message = recognize_speech()
            messages.append({'role': 'user', 'content': message})
            
            if should_exit(message):
                print("对话结束，程序即将退出。")
                break

            whole_message = ''
            responses = Generation.call(Generation.Models.qwen_turbo, messages=messages, result_format='message', stream=True, incremental_output=True)
            print('通义千问:', end='')
            for response in responses:
                content = response.output.choices[0]['message']['content'] if response.output and response.output.choices else ""
                whole_message += content
                print(content, end='')
            print()
            messages.append({'role': 'assistant', 'content': whole_message})
            text_to_speech(whole_message)
            play_audio("output.wav")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    main()
