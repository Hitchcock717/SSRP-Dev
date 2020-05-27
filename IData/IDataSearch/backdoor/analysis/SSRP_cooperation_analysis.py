# -*- coding: utf-8 -*-
'''
    SSRP分析平台之关系图分析 --- 作者两两合作
'''

import itertools
from .SSRP_convert2num import *


class CooperateAnalysis(object):

    def __init__(self):
        # self.two_aus = ['王曜 陈舜胜', '郝勇 陈斌', '王洪荣 季昀', '周贤婧 师彦平', '王明智 杜建忠', '侯殿志 沈群', '张玉洁 付丽红', '凃璨 熊飞', '晓影 晓蓉', '李宗吉 赵巍', '邱澄宇 林杰曦', '申培博 韩秀珍', '李清 冶贵生', '何元丽 李国英', '李婷 翁武银', '石晶 陈荣冰', '石晶 陈荣冰', '臧学丽 陈光', '刘芊麟 陈亚楠', '刘芊麟 陈亚楠', '潘征 潘兴寿', '荣立洋 李毓秋', '潘振伟 侯宪云', '秦超燕 宁带连', '涂宽 崔鸿', '马娟 唐仕芳', '麦麦提艾力·阿卜杜纳斯尔 马纪', '廖晓峰 于荣', '郑贤金 汤斌', '杨旭 谢盈', '田顺立 郑春阳', '王洪 赵亚军', '周礼元 姜孝珣', '张丽琼 李博', '张金龙 蒋高喜', '徐澜 黄孟', '罗志祥 罗志忠', '佘宁 何伟先', '李伟龙 周晓肖', '肖永仁 杨连玉', '赵振东 王洁', '张树泽 吴国豪', '杨建芬 刘瑶', '小兵 植观', '祝远超 熊勇刚', '鲁佩玉 孙青华', '周芳 索化夷', '王姣 李宗孝', '闵建华 王浩', '闫文华 欧杰', '王清 陈舜胜', '马本贺 王海华', '张志浩 张继平', '成依依 周红宁', '王妍 令狐恩强', '黄嘉禾 贺平安', '王美迟 王贤纯', '苏艳玲 张谨华', '谢剑飞 杨欣卉', '黄啟亮 宋晓东', '田畅 王洋', '钱红 刘克明', '赵文鹏 黄国欣']
        # self.more_aus = ['周冰心 傅勇 刘群 刘晶', '郝长波 张洁 谢建伟 王磊磊', '韩加敏 董霞 王小平 周昱恒', '麦麦提艾力·阿卜杜纳斯尔 李梦鸽 包静 随慧', '王晓岩 图力古尔 包海鹰', '陈丽花 朱楚楚 李冉冉', '何晓红 杨宏国 伍晓丽 刘飞 谢永芳 蒋龙星 王宇 冉玲芳', '程楠 项黛徽 沈雅园 付建新 张超', '施魁 唐燕妮 刘炀 管武太 陈芳 邓跃林', '王英明 徐亚欧 王志敏 徐珑洋 杨磊 林亚秋', '刘翠 潘健存 李媛媛 陈勇 蒋士龙', '王芳 乔璐 张庆庆 沈斌', '李景芳 王燕 陆东林', '农玉琴 李金婷 陈远权 陆金梅 廖春文 韦持章 韦锦坚', '王澍 冯力 李倩 杜鹃', '尹敬 任晓镤 钱烨 王震 彭增起 张雅玮', '刘中成 刘世芳 张苏 杨艳蕾 李飞 张楠 袁欣 张艳芬', '张勇 李弘文 曹晋良 南晓洁 杨丽', '金春爱 崔松焕 赵卉 嵩之松 王艳梅 刘畅 孙印石', '陈怡颖 丁奇 赵静 孙颖 张玉玉 孙宝国 郑福平', '郭丹 王晶 齐广海 张涛 高俊 张海军 武书庚', '周玉照 张小苗 赵天智 普星星 张以芳', '赵诗瑜 张帆 周晓龙 汪涵 赵阿勇 杨松柏']
        self.search = SearchDictBuild()

    def build_two_authors(self, two_aus):
        two_aus_data = []
        two_aus_list = [aus.split(' ') for aus in two_aus]
        for au in two_aus_list:
            aus_combi = list(itertools.combinations(au, 2))
            two_aus_data.extend(aus_combi)

        return two_aus_data

    def build_more_authors(self, more_aus):
        more_aus_data = []
        more_aus_list = [aus.split(' ') for aus in more_aus]
        for au in more_aus_list:
            aus_combi = list(itertools.combinations(au, 2))
            more_aus_data.extend(aus_combi)

        return more_aus_data

    def prepare_data(self, two_aus, more_aus):
        data = []
        two_aus = self.build_two_authors(two_aus)
        more_aus = self.build_more_authors(more_aus)
        data.extend(two_aus)
        data.extend(more_aus)

        # 清洗,删去无用关系
        for aus in data:
            aus_check = aus[1]
            if aus_check == '':
                data.remove(aus)

        # print(data)
        return data

    def build_au_id(self, two_aus, more_aus):
        data = self.prepare_data(two_aus, more_aus)
        s_li = self.search.aus_build(data)
        aus_li = self.search.de_duplication(s_li)
        ids_li = self.search.ids_build(aus_li)
        au_id_dict = self.search.dict_build(aus_li, ids_li)

        return au_id_dict

    def build_au_relation(self, two_aus, more_aus):
        relations = []
        for k in self.prepare_data(two_aus, more_aus):
            relation = {}
            p_au1, q_au2 = k[0], k[1]
            p = self.build_au_id(two_aus, more_aus).get(p_au1)
            q = self.build_au_id(two_aus, more_aus).get(q_au2)
            relation['from'] = str(p)
            relation['to'] = str(q)
            relations.append(relation)
        print(relations)

        ids = []
        for k,v in zip(list(self.build_au_id(two_aus, more_aus).keys()), list(self.build_au_id(two_aus, more_aus).values())):
            id = {}
            id['id'] = int(v)
            id['label'] = str(k)
            ids.append(id)
        print(ids)
        return ids, relations


if __name__ == '__main__':
    cooper = CooperateAnalysis()
    cooper.build_au_relation(two_aus, more_aus)
