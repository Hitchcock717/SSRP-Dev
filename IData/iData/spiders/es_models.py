# 字段类型
from elasticsearch_dsl import Document, Completion, Keyword, Text, Boolean, Integer, Date
# 链接函数
from elasticsearch_dsl.connections import connections
# 分析器
from elasticsearch_dsl.analysis import CustomAnalyzer
 
# 1. 创建es连接,参数就是es的地址
connections.create_connection(hosts=["127.0.0.1"])
 
 
# 自定义一个分词器
class Analyzer(CustomAnalyzer):
    # 返回分析器对象
    def get_analysis_definition(self):
        return {}
 
 
# 创建分析器对象
ik_analyzer = Analyzer('ik_max_word', filter=['lowercase'])
 
 
class IdataSpider(Document):
    # 搜索框中的自动补齐功能
    suggest = Completion(analyzer=ik_analyzer)
    # ik_max_word 分词策略 细分
    # ik_smart 分词策略 粗分
    # analyzer: 分析器(意思)
    d_url = Text(analyzer="ik_max_word")
    title = Text(analyzer="ik_max_word")
    author = Text(analyzer="ik_max_word")
    source = Keyword()
    info = Text(analyzer="ik_max_word")
    date = Date()
    kws = Keyword()
    cited = Integer()
    downed = Integer()
    download = Text(analyzer="ik_max_word")
    abstract = Text(analyzer="ik_max_word")
    fund = Text(analyzer="ik_max_word")
 
    class Index:  # es7.0+
        name = 'idata_doc'
        print('Create new index successfully!')


if __name__ == '__main__':
    IdataSpider.init()
