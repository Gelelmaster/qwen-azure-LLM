from dashscope import Generation
from dashscope.api_entities.dashscope_response import Role

def model(message):
    messages = ''
                
    # 调用通义千问大模型，接收流式输出到 messages
    responses = Generation.call(Generation.Models.qwen_plus, messages=message, result_format='message', stream=True, incremental_output=True)
    print('通义千问:', end='')
    
    # 把流式输出的所有消息合成一条输出
    for response in responses:
        content = response.output.choices[0]['message']['content'] if response.output and response.output.choices else ""
        messages += content
        print(content, end='')
    return messages
