from LLM import ErnieLLM, OpenAILLM, Llama
import ast

class Diversifier():
    def __init__(self, model_series="ernie-bot-4"):
        if model_series == "ernie-bot-4":
            self.llm = ErnieLLM()
        elif model_series == "gpt-3.5-turbo":
            self.llm = OpenAILLM()
        elif model_series == "llama-7b":
            self.llm = Llama()
        else:
            self.llm = ErnieLLM()

    def diversify(self, prime_data):
        '''
        return:list 多样化的数据
        '''
        # 对于已有的数据，利用大模型的能力，生成更多样化的数据
        diversify_prompt = f"""
        你是一个优秀的数据生成者，你擅长根据当前的数据，去随机生成彼此间毫不相关的新数据。
        以下是目前有的原数据
        prime_data:"{prime_data}"
        请你根据prime_data随机生成example，example和原问题没有任何关系，example彼此之间也没有任何关系。请记得将结果写在python格式的列表里[example1, example2, ...]
        """
        response = self.llm.response(diversify_prompt)
        examples = ast.literal_eval("[" + response.split("[")[-1].split("]")[0] + "]")
        return examples

if __name__ == "__main__":
    diversifier = Diversifier()
    answer = diversifier.diversify("清华大学是中国最好的大学吗？")
    print(answer)
    answer = diversifier.diversify("我的父亲和我没有血缘关系，那么我的爷爷和我有可能是亲生的吗？如果有可能，分析出这种可能的具体情况。")
    print(answer)
    answer = diversifier.diversify("10块钱可以买3瓶可乐，3个瓶盖可以换一瓶可乐，那么23块钱最多可以买多少瓶可乐？")
    print(answer)
        
