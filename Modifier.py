import copy
from LLM import ErnieLLM


class Modify:
    def __init__(self):
        self.llm = ErnieLLM()

    def CombineInfo(self, Strategy_Prompt):
        s = str()
        i = 0
        for value in Strategy_Prompt.values():
            i += 1
            s += f"第{i}段话：\n{value}\n"
        return s
    
    def GetJsonResult(self, response):
        start = response.find("{")
        end = response.rfind("}")
        response_dictstr = response[start : end+1]

        try:
            return eval(response_dictstr)['result']
        except:
            return response


    def GetModifiedResult(self, Strategy_Prompt, modify_guide):
        CombinedInfo = self.CombineInfo(Strategy_Prompt)
        initial_message = {
            "role":"user", 
            "content":"请你为我将以下{}段话的信息整合一下：\
                      \n{}\n\
                      以上就是你要整合{}段信息。请你将上述信用通顺的语言重新组织，然后返回给我。\
                      整合后的信息应该前后因果关系顺畅。\
                      你可以调换句子顺序，但你不能改变语言风格或者省略信息。\
                    ".format(len(Strategy_Prompt), CombinedInfo, len(Strategy_Prompt))
        }

        model_reply = {
            "role":"assistant", 
            "content":"好的，我明白了，我稍后会为你整合信息。请问还有其他要求吗？\
                    ".format(len(Strategy_Prompt), CombinedInfo, len(Strategy_Prompt))
        }

        additional_guide = {
            "role":"user", 
            "content": "{}\n".format(modify_guide) + "接下来，请你结合上述所有信息和要求，以{\"result\": 整合后的结果}的格式返回整合后的结果。"
        }
        prompt_messages = [initial_message, model_reply, additional_guide]

        response = self.llm.multiple_messages_response(messages = prompt_messages)
        return self.GetJsonResult(response)



if __name__ == "__main__":
    test_chat = ErnieLLM()
    import erniebot

    modify_block = Modify()
    modify_guide = "增加一个要求：如果是在面对连续除法的时候，请先算前面的除法，得到结果之后再算后面的除法。"
    Strategy_Prompt = {
    's1' : '你是一个数学大师，擅长解决各种复杂的数学问题。\
    在你面对一个数学问题时，你会首先分析问题的难点所在，然后运用你的专业知识和技能来解决问题。\
    例如，当面对一个复杂的微积分问题时，你会注意到其中的难点可能包括复杂的函数形式、多变的变量和需要巧妙运用的微积分规则。\
    请你在解决这类问题时，特别留意这些难点，并运用你的数学技巧来给出准确的解答。',
    's2' : '你是一个数学大师，善于将复杂的问题拆解成简单的步骤。当你面对一个数学难题时，你会首先理解问题的本质，然后将其拆分成一个个可以解决的子问题，并逐一解决。\
    最后，你会将子问题的解决方案组合起来，得到原问题的答案。\n\
    现在，请你利用这种分步骤解决问题的方法，帮我解决以下的数学问题：\n\
    [具体的数学问题]\n\
    首先，请你理解这个问题的本质是什么？\n\
    然后，请你将这个问题拆分成哪些可以解决的子问题？\n\
    接着，请你逐一解决这些子问题，并给出每一步的详细推导过程。\n\
    最后，请你将子问题的解决方案组合起来，得到原问题的答案。'
    }
    response = modify_block.GetModifiedResult(Strategy_Prompt = Strategy_Prompt,
                                            modify_guide = modify_guide)
    print(response)
