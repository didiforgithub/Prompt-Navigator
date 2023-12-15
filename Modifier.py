import copy
from ErnieLLM import ErnieLLM

class Modify:
    def __init__(self):
        self.llm = ErnieLLM()
        self.prompt_message = [
            {
                "role": "user", 
                "content": "现在，你将成为一个高效的信息整合器。\
                    我将向你提供一些重要的信息片段，并明确告诉你哪些信息是不允许包含在内的。\
                    你的任务是将这些重要信息巧妙地融合到一段流畅且连贯的话语中，同时确保所有不应出现的信息都被排除在外。\
                    请确保最终输出的信息完全符合我的要求，既包含所有重要的点，又避开了指定的禁区。\
                    最终，你应该返回一个如下json。注意标点应为英文格式。:\
                    \{\
                        \"result\": \"你整合之后的结果\",\
                    \}"
            },
            {
                'role': 'assistant',
                'content': "好的，请提供需要整合的信息片段，以及需要避开的信息片段，我会尽力帮助您。"
            }
        ]
        
        
    def ConvertToDict(self, dict_str):
        try:
            eval(dict_str)
        except:
            lines = dict_str.split('\n')
            dict_str = '\n'.join([lines[i] for i in range(1, len(lines) - 1)])
        return dict_str
    

    def GetModifyResult(self, reserve, delete, add):
        response_message = {"role" : 'assistant', 'content' : None}
        
        ## 保留信息1
        prompt_message = copy.deepcopy(self.prompt_message)
        prompt_message.append({
            "role": "user", 
            "content": "好的，要整合的信息片段是:\n{}\n\
                        以上就是你需要整合的信息片段。\
                        请你不要改变上述信息中的人称。例如我在上述信息片段中用的第二人称，你给我返回的整合信息中也应该是第二人称。\
                        同时你可以适度地发挥创造性，通过调整语序等方式，使整合后的内容不仅没有缺失任何信息，同时前后因果逻辑流畅。\
                        请你直接以定义好的dict返回给我你整合之后的结果，切勿做多余的解释和任何形式的说明。".format(reserve)
        })
        response_str = self.llm.multiple_messages_response(prompt_message)
        response_message['content'] = self.ConvertToDict(response_str)
        # print(response_message['content'])


        ## 增添信息
        prompt_message.append(response_message)
        prompt_message.append({
            "role": "user", 
            "content": "好的，你已经完成了第一阶段的整合。接下来，我会再给你一段补充信息，请你补充到上述信息中。\
                        补充信息为：\n{}\n\
                        以上就是你需要补充的信息片段。\
                        你补充后的内容不应该缺失任何信息，同时因果逻辑流畅。\
                        请你直接以定义好的dict返回给我你整合之后的结果，切勿做多余的解释和任何形式的说明。".format(add)
            })
        response_str = self.llm.multiple_messages_response(prompt_message)
        response_message['content'] = self.ConvertToDict(response_str)
        # print(response_message['content'])
        

        ## 删除信息
        prompt_message.append(response_message)
        prompt_message.append({
            "role": "user", 
            "content": 
                "好的，现在我需要你从以上信息中剔除下列信息。\
                需要剔除的信息为:\n{}\n\
                以上就是你需要剔除的信息片段。\
                注意，与需要剔除的信息含义类似的信息也需要被剔除。而未提及的信息务必全部保留，如无必要无需对这类信息进行增减和修改。\
                请你直接以定义好的dict返回给我你剔除之后的结果，切勿做多余的解释和任何形式的说明。".format(delete)
            })
        response_str = self.llm.multiple_messages_response(prompt_message)
        response_message['content'] = self.ConvertToDict(response_str)
        # print(response_message['content'])
        return eval(response_str)['result']


if __name__ == "__main__":
    modify_block = Modify()
    modified_prompt = modify_block.GetModifyResult(
        reserve = "你的回答不仅要正确无误，还要深入浅出，易于理解，即便是最复杂的数学概念也要能够娓娓道来，让任何没有数学背景的人都能够一听就懂。\n\
                你现在是一位伟大的数学家，拥有深不可测的智慧和破解任何数学难题的能力。\n\
                你可以引用历史上的数学成就。",
        delete = "你可以引用历史上的数学成就，或者提出全新的观点或方法论。同时，你所提供的解决方案要创新，能够启发思考，甚至可能引领数学领域的新发展。\n\
                让任何没有数学背景的人都能够一听就懂。",
        add = "对于四则运算之类的题目，请你根据先乘除后加减的顺序，逐步计算，得到最终的结果。你的计算过程需要有所体现。"
    )
    print(modified_prompt)