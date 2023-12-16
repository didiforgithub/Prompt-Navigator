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

    def diversify(self, prime_data):
        '''
        return:list 多哦样
        '''
        # 对于已有的数据，利用大模型的能力，生成更多样化的数据
        diversify_prompt = f"""
        你是一个优秀的多样化数据生成者，你擅长从一个具体的例子泛化生成具有多样性的例子，你有一套自己的工作流程方法论：
        1.先对当前问题进行高维度分析，确定这个问题的类型。
        2.然后在这个类型去生成不同子领域的新问题。
        3.检查重复，去掉相似度高的问题。
        可以参考的例子是
            逻辑思维：
            prime_data:"如果我吃自己的屎，我是生产者还是消费者还是分解者？"
            example1:"香菇掉厕所了还能叫香菇吗？"
            example2:"包装上写着开封即食，我到了，然后呢?"
            example3:"把加特林从冰箱拿出来算冷兵器吗？"

            数理逻辑：
            prime_data:"鸡和兔共49只，一共有100条腿，问鸡和兔各有多少只？"
            example1:"列公式解释为什么svm需要用对偶式来求解。"
            example2:"如何建模量化养老金的影响因子？"

            常识检测：
            prime_data:"清华大学在中国和世界的排名是多少？"
            example1:"泰姬陵的建筑材料主要有哪些？"
            example2:"大熊猫和小熊猫的关系是什么？"

        以上每个例子之间涉及的具体话题不同（比如原问题里涉及了清华，后面的example里就绝对不能反复提及大学相关的对象和概念，因为提这个问题是为了检测常识，而不是纠结于教育这个领域），但是他们从属于相同的类型。
        以下是目前有的原数据
        prime_data:"{prime_data}"
        请你根据prime_data生成多样化的样例，千万不要纠结于具体的对象和概念，而是要站在更高的维度泛化问题。请记得将结果写在python格式的列表里[example1, example2, ...]
        """
        response = self.llm.response(diversify_prompt)
        examples = ast.literal_eval("[" + response.split("[")[-1].split("]")[0] + "]")
        return examples

if __name__ == "__main__":
    diversifier = Diversifier()
    # answer = diversifier.diversify("清华大学是中国最好的大学吗？")
    # print(answer)
    # answer = diversifier.diversify("我的父亲和我没有血缘关系，那么我的爷爷和我有可能是亲生的吗？如果有可能，分析出这种可能的具体情况。")
    # print(answer)
    answer = diversifier.diversify("10块钱可以买3瓶可乐，3个瓶盖可以换一瓶可乐，那么23块钱最多可以买多少瓶可乐？")
    print(answer)
        
