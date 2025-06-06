#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
千面劫·宿命轮回 小说数据导入脚本
清空现有项目数据，分析拆解小说章节内容，并将信息填入当前框架中
"""

import requests
import json
import os
import sys
from typing import Dict, List, Any

# API基础URL
BASE_URL = "http://localhost:8000/api"

class NovelDataImporter:
    def __init__(self):
        self.base_url = BASE_URL
        self.project_id = None

    def clear_all_projects(self):
        """清空所有现有项目"""
        print("🗑️ 正在清空现有项目数据...")

        try:
            # 获取所有项目
            response = requests.get(f"{self.base_url}/projects/")
            if response.status_code == 200:
                projects = response.json()["projects"]

                for project in projects:
                    project_id = project["id"]
                    # 清空项目数据
                    clear_response = requests.delete(f"{self.base_url}/project-data/projects/{project_id}/data")
                    if clear_response.status_code == 200:
                        print(f"✅ 已清空项目 {project['name']} 的数据")

                    # 删除项目
                    delete_response = requests.delete(f"{self.base_url}/projects/{project_id}")
                    if delete_response.status_code == 200:
                        print(f"✅ 已删除项目 {project['name']}")

            print("✅ 所有现有项目数据已清空")

        except Exception as e:
            print(f"❌ 清空项目数据时出错: {e}")

    def create_novel_project(self):
        """创建千面劫·宿命轮回项目"""
        print("📚 正在创建《千面劫·宿命轮回》项目...")

        project_data = {
            "name": "千面劫·宿命轮回",
            "title": "千面劫·宿命轮回",
            "subtitle": "仙魔恩怨，宿命轮回",
            "author": "原作者",
            "project_type": "xianxia",
            "status": "writing",
            "summary": "一个关于千面郎君与妖帅灵蜗跨越千年的爱恨情仇故事，涉及仙界阴谋、妖族复仇、宿命轮回的玄幻小说。",
            "description": "高考结束后的宋少雨意外获得千面面具，觉醒前世记忆，发现自己是千年前的散仙千面郎君转世。与此同时，盛百威也因妖物影响觉醒特殊能力。两人将面对来自仙界的追杀和妖族的复仇，在宿命的轮回中寻找真相。",
            "outline": "第一卷：夙世恩怨 - 主角们觉醒能力，发现身世之谜\n第二卷：仙魔大战 - 面对仙界追杀，妖族复仇\n第三卷：宿命轮回 - 揭开千年前真相，打破轮回宿命",
            "settings": {
                "genre": "仙侠玄幻",
                "world_type": "现代修真",
                "power_system": "仙魔体系",
                "main_theme": "宿命轮回，爱恨情仇"
            },
            "metadata": {
                "import_source": "千面劫·宿命轮回文件夹",
                "import_date": "2025-05-30",
                "volume_count": 1,
                "chapter_count": 5
            }
        }

        try:
            response = requests.post(f"{self.base_url}/projects/", json=project_data)
            if response.status_code == 200:
                project = response.json()
                self.project_id = project["id"]
                print(f"✅ 项目创建成功，ID: {self.project_id}")
                return True
            else:
                print(f"❌ 项目创建失败: {response.text}")
                return False

        except Exception as e:
            print(f"❌ 创建项目时出错: {e}")
            return False

    def analyze_and_import_chapters(self):
        """分析并导入章节内容"""
        print("📖 正在分析并导入章节内容...")

        # 章节文件路径
        chapter_files = [
            "千面劫·宿命轮回/第一卷 夙世恩怨/第1章  诡异的面具.txt",
            "千面劫·宿命轮回/第一卷 夙世恩怨/第2章  好友相见 分外嘴贱.txt",
            "千面劫·宿命轮回/第一卷 夙世恩怨/第3章  被选中的孩子.txt",
            "千面劫·宿命轮回/第一卷 夙世恩怨/第4章  恶向胆边生.txt",
            "千面劫·宿命轮回/第一卷 夙世恩怨/第5章  魔影初现.txt"
        ]

        # 首先创建卷宗
        volume_data = {
            "name": "第一卷 夙世恩怨",
            "title": "夙世恩怨",
            "subtitle": "觉醒篇",
            "summary": "宋少雨和盛百威分别获得神秘面具和觉醒特殊能力，发现自己的前世身份，开始面对来自仙界和妖族的威胁。",
            "description": "本卷讲述了两位主角的觉醒过程，从普通高中生到拥有超凡能力的修行者，揭开了千年前仙魔大战的序幕。",
            "volume_number": 1,
            "status": "completed",
            "word_count": 25000,
            "chapter_count": 5,
            "project_id": self.project_id
        }

        try:
            volume_response = requests.post(f"{self.base_url}/project-data/projects/{self.project_id}/data/volume",
                                          json={"data": volume_data})
            if volume_response.status_code == 200:
                volume_id = volume_response.json()["data"]["id"]
                print(f"✅ 卷宗创建成功，ID: {volume_id}")
            else:
                print(f"❌ 卷宗创建失败: {volume_response.text}")
                return False

        except Exception as e:
            print(f"❌ 创建卷宗时出错: {e}")
            return False

        # 导入章节
        for i, chapter_file in enumerate(chapter_files, 1):
            if os.path.exists(chapter_file):
                with open(chapter_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                chapter_data = self.analyze_chapter_content(i, content, volume_id)

                try:
                    chapter_response = requests.post(f"{self.base_url}/project-data/projects/{self.project_id}/data/chapter",
                                                   json={"data": chapter_data})
                    if chapter_response.status_code == 200:
                        print(f"✅ 第{i}章导入成功")
                    else:
                        print(f"❌ 第{i}章导入失败: {chapter_response.text}")

                except Exception as e:
                    print(f"❌ 导入第{i}章时出错: {e}")
            else:
                print(f"⚠️ 章节文件不存在: {chapter_file}")

        return True

    def analyze_chapter_content(self, chapter_num: int, content: str, volume_id: int) -> Dict[str, Any]:
        """分析章节内容并提取信息"""

        # 章节标题映射
        chapter_titles = {
            1: "诡异的面具",
            2: "好友相见 分外嘴贱",
            3: "被选中的孩子",
            4: "恶向胆边生",
            5: "魔影初现"
        }

        # 章节摘要映射
        chapter_summaries = {
            1: "宋少雨在夜市遇到神秘老者黑星道长，获得千面面具，面具显现异象，好友吴适被面具重量击倒。",
            2: "盛百威在苏格兰治疗后回国，觉醒火元素能力，与宋少雨重逢，两人都发现了彼此的变化。",
            3: "宋少雨用鲜血激活千面面具，与灵蜗建立联系，盛百威发现面具的特殊性质，两人意识到自己是被选中的孩子。",
            4: "宋少雨在梦中了解前世身份千面郎君和与灵蜗的爱恨情仇，盛百威也在梦中发现体内的神秘存在。",
            5: "修真监察局追查千面面具，宋少雨与凌专员等人战斗，盛百威觉醒噬心魔力量，面具完整觉醒。"
        }

        chapter_data = {
            "name": f"第{chapter_num}章 {chapter_titles.get(chapter_num, '')}",
            "title": chapter_titles.get(chapter_num, f"第{chapter_num}章"),
            "chapter_number": chapter_num,
            "volume_id": volume_id,
            "content": content,
            "summary": chapter_summaries.get(chapter_num, ""),
            "word_count": len(content),
            "status": "published",
            "project_id": self.project_id,
            "metadata": {
                "import_source": "原文件",
                "chapter_type": "正文",
                "key_events": self.extract_key_events(chapter_num),
                "characters_appeared": self.extract_characters(chapter_num),
                "locations": self.extract_locations(chapter_num)
            }
        }

        return chapter_data

    def extract_key_events(self, chapter_num: int) -> List[str]:
        """提取章节关键事件"""
        events_map = {
            1: [
                "宋少雨在夜市与好友走散",
                "遇到神秘老者黑星道长和面具摊位",
                "成功取下千面面具，面具瞳孔出现苍蓝火焰",
                "吴适试图抢夺面具被击倒，鼻血被面具吸收",
                "宋少雨影子出现异常变化"
            ],
            2: [
                "盛百威在苏格兰诊所醒来，了解自己的遭遇",
                "哈森测试盛百威的元素能力，确认其为魔心天生",
                "盛百威回国，父亲安排其去宋家治疗",
                "盛百威与宋少雨重逢，发生误会和打斗",
                "两人前往宋书文处寻求帮助"
            ],
            3: [
                "宋少雨用鲜血激活千面面具",
                "面具完全苏醒，与宋少雨融合",
                "灵蜗在宋少雨脑海中出现，建立联系",
                "盛百威无法拿起面具，证实面具的特殊性",
                "宋书文开始调查面具和灵蜗的来历"
            ],
            4: [
                "宋少雨在梦中了解前世身份千面郎君",
                "灵蜗讲述千年前仙魔大战的真相",
                "盛百威梦见体内的神秘魔物",
                "宋少雨因盛百威的恶作剧昏迷",
                "两人都意识到自己身份的特殊性"
            ],
            5: [
                "修真监察局凌专员等人追查千面面具",
                "宋少雨与诛仙卫发生激烈战斗",
                "盛百威与噬心魔签订契约，觉醒力量",
                "千面面具吸收青铜面具碎片，完整觉醒",
                "宋书文揭示双生契约和金色千面的秘密"
            ]
        }
        return events_map.get(chapter_num, [])

    def extract_characters(self, chapter_num: int) -> List[str]:
        """提取章节出现的人物"""
        characters_map = {
            1: ["宋少雨", "吴适", "马侯", "萧九", "黑星道长"],
            2: ["盛百威", "哈森", "凯伦", "盛雅奇", "宋少雨"],
            3: ["宋少雨", "盛百威", "宋书文", "灵蜗"],
            4: ["宋少雨", "盛百威", "灵蜗", "千面郎君(前世)", "宋书文"],
            5: ["宋少雨", "盛百威", "宋书文", "凌专员", "诛仙卫", "噬心魔", "灵蜗"]
        }
        return characters_map.get(chapter_num, [])

    def extract_locations(self, chapter_num: int) -> List[str]:
        """提取章节出现的地点"""
        locations_map = {
            1: ["临镇夜市", "街角面具摊位", "回家路上"],
            2: ["苏格兰波菲尔村诊所", "机场", "飞机上", "盛百威家乡村子"],
            3: ["宋书文家", "正厅", "东房", "西房"],
            4: ["宋书文家", "东房", "梦境中的赤湖战场"],
            5: ["宋氏祖地祠堂", "地窖", "青铜棺椁所在地"]
        }
        return locations_map.get(chapter_num, [])

    def import_characters(self):
        """导入人物信息"""
        print("👥 正在导入人物信息...")

        characters = [
            {
                "name": "宋少雨",
                "title": "千面郎君转世",
                "age": 18,
                "gender": "male",
                "description": "高考结束的高中生，意外获得千面面具，觉醒前世记忆，发现自己是千年前散仙千面郎君的转世。",
                "personality": "机智幽默，有些小心眼，但关键时刻很有担当。对朋友义气，面对危险时勇敢坚定。",
                "background": "普通高中生家庭，因家中生意繁忙而与好友外出游玩时获得面具，从此踏上修行之路。",
                "abilities": ["千面变化", "苍蓝火焰", "妖蛇虚影", "面具融合"],
                "relationships": ["与盛百威是好友", "与灵蜗是前世夫妻", "与黑星道长有师徒缘分"],
                "current_status": "觉醒中",
                "importance": "protagonist",
                "project_id": self.project_id,
                "metadata": {
                    "前世身份": "千面郎君",
                    "法器": "千面面具",
                    "伴侣": "灵蜗",
                    "敌人": "仙界诛仙卫"
                }
            },
            {
                "name": "盛百威",
                "title": "魔心天生者",
                "age": 18,
                "gender": "male",
                "description": "宋少雨的好友，因妖物影响觉醒火元素能力，后发现体内封印着噬心魔，拥有强大的魔族血统。",
                "personality": "外表俊美如精灵，性格直率，有些冲动，但内心善良。面对危险时会保护朋友。",
                "background": "上海人，因遭遇妖物被父亲送到苏格兰治疗，回国后发现自己的特殊能力和身世。",
                "abilities": ["火元素控制", "噬心魔力量", "魔族血统", "元素亲和"],
                "relationships": ["与宋少雨是好友", "与哈森有师徒关系", "与噬心魔有契约关系"],
                "current_status": "觉醒中",
                "importance": "protagonist",
                "project_id": self.project_id,
                "metadata": {
                    "血统": "魔族后裔",
                    "契约对象": "噬心魔",
                    "导师": "哈森",
                    "特殊体质": "魔心天生"
                }
            },
            {
                "name": "灵蜗",
                "title": "妖帅",
                "age": 1000,
                "gender": "female",
                "description": "千年前的妖族帅领，与千面郎君相爱，因仙界阴谋而死，残魂封印在千面面具中等待转世重逢。",
                "personality": "深情专一，为爱可以牺牲一切。对仙界充满仇恨，但对千面郎君温柔体贴。",
                "background": "妖族帅领，统领众妖与人族作战，后因爱上千面郎君而改变立场，最终被仙界陷害致死。",
                "abilities": ["妖族法术", "蛇形变化", "精神连接", "妖力传承"],
                "relationships": ["与宋少雨(千面郎君)是前世夫妻", "与仙界为敌", "与妖族有统领关系"],
                "current_status": "残魂状态",
                "importance": "supporting",
                "project_id": self.project_id,
                "metadata": {
                    "种族": "妖族",
                    "职位": "妖帅",
                    "状态": "残魂",
                    "封印地": "千面面具"
                }
            },
            {
                "name": "黑星道长",
                "title": "神秘道士",
                "age": 70,
                "gender": "male",
                "description": "神秘的老道士，掌管着各种神奇面具，似乎知晓千年前的秘密，引导宋少雨获得千面面具。",
                "personality": "神秘莫测，话语深奥，似乎能预知未来。对有缘人慷慨，但不轻易透露秘密。",
                "background": "曾是天命观的执事长老，掌握着古老的秘密和法器，四处寻找有缘人传承法器。",
                "abilities": ["预知能力", "法器制作", "阵法布置", "因果感知"],
                "relationships": ["与宋少雨有师徒缘分", "与宋书文有旧识", "与天命观有关联"],
                "current_status": "行踪不明",
                "importance": "supporting",
                "project_id": self.project_id,
                "metadata": {
                    "门派": "天命观",
                    "职位": "执事长老",
                    "特长": "法器传承",
                    "行踪": "四处游历"
                }
            },
            {
                "name": "宋书文",
                "title": "宋家大长老",
                "age": 65,
                "gender": "male",
                "description": "宋家大长老，精通驱邪除魔之术，是宋少雨的大伯，对古老的秘密有所了解。",
                "personality": "严肃认真但关爱晚辈，知识渊博，面对危险时冷静应对。对宋少雨如亲孙子般疼爱。",
                "background": "宋家长辈，年轻时以治妖为生，积累了丰富的经验和知识，现在指导后辈修行。",
                "abilities": ["驱邪术法", "医术", "阵法", "古籍研究"],
                "relationships": ["宋少雨的大伯", "与黑星道长有旧识", "宋家族长"],
                "current_status": "健在",
                "importance": "supporting",
                "project_id": self.project_id,
                "metadata": {
                    "家族": "宋家",
                    "职位": "大长老",
                    "专长": "驱邪除魔",
                    "关系": "宋少雨大伯"
                }
            }
        ]

        for character in characters:
            try:
                response = requests.post(f"{self.base_url}/project-data/projects/{self.project_id}/data/character",
                                       json={"data": character})
                if response.status_code == 200:
                    print(f"✅ 人物 {character['name']} 导入成功")
                else:
                    print(f"❌ 人物 {character['name']} 导入失败: {response.text}")

            except Exception as e:
                print(f"❌ 导入人物 {character['name']} 时出错: {e}")

    def import_world_settings(self):
        """导入世界设定"""
        print("🌍 正在导入世界设定...")

        world_setting = {
            "name": "千面劫世界观",
            "title": "仙魔并存的现代修真世界",
            "description": "一个仙界、魔族、人族三足鼎立的世界，表面是现代社会，暗地里存在着修真者、妖族和各种超自然力量。千年前的仙魔大战影响至今。",
            "geography": {
                "主要区域": [
                    "人间界 - 现代社会表层",
                    "仙界 - 仙人居住的高等位面",
                    "妖界 - 妖族的栖息地",
                    "赤湖 - 千年前大战的战场遗迹",
                    "万妖岭 - 千面郎君陨落之地"
                ],
                "特殊地点": [
                    "天命观 - 神秘道观，已被移除",
                    "宋氏祖地 - 宋家族地，有古老祠堂",
                    "修真监察局 - 仙界在人间的执法机构"
                ]
            },
            "history": {
                "千年前": "仙魔大战，千面郎君与妖帅灵蜗的爱恨情仇",
                "现代": "修真监察局监管超自然事件，普通人不知真相",
                "转世轮回": "千面郎君转世为宋少雨，开始新的宿命循环"
            },
            "natural_laws": {
                "修真体系": "仙、魔、妖三大体系并存",
                "因果法则": "前世因果影响今生，宿命轮回不断",
                "法器系统": "古老法器拥有强大力量，认主而用",
                "血脉传承": "特殊血脉可以觉醒超凡能力"
            },
            "cultures": {
                "仙界文化": "等级森严，以维护秩序为名行专制之实",
                "妖族文化": "崇尚自由，重视情义，与仙界对立",
                "人族文化": "现代社会文化，大部分人不知超自然存在"
            },
            "project_id": self.project_id,
            "metadata": {
                "世界类型": "现代修真",
                "主要冲突": "仙魔对立",
                "核心主题": "宿命轮回，爱恨情仇"
            }
        }

        try:
            response = requests.post(f"{self.base_url}/project-data/projects/{self.project_id}/data/world_setting",
                                   json={"data": world_setting})
            if response.status_code == 200:
                print("✅ 世界设定导入成功")
            else:
                print(f"❌ 世界设定导入失败: {response.text}")

        except Exception as e:
            print(f"❌ 导入世界设定时出错: {e}")

    def run(self):
        """执行完整的导入流程"""
        print("🚀 开始导入《千面劫·宿命轮回》数据...")
        print("=" * 50)

        # 1. 清空现有项目
        self.clear_all_projects()
        print()

        # 2. 创建新项目
        if not self.create_novel_project():
            print("❌ 项目创建失败，终止导入")
            return False
        print()

        # 3. 导入章节内容
        if not self.analyze_and_import_chapters():
            print("❌ 章节导入失败")
            return False
        print()

        # 4. 导入人物信息
        self.import_characters()
        print()

        # 5. 导入世界设定
        self.import_world_settings()
        print()

        print("🎉 《千面劫·宿命轮回》数据导入完成！")
        print(f"📊 项目ID: {self.project_id}")
        print("=" * 50)
        return True

if __name__ == "__main__":
    importer = NovelDataImporter()
    importer.run()
