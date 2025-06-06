#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《千面劫·宿命轮回》数据导入脚本
清空现有项目信息，分析拆解小说章节内容，填入当前框架
"""

import requests
import json
import os
import re
from typing import Dict, List, Any

class QianMianJieImporter:
    def __init__(self):
        self.base_url = "http://localhost:8000/api"
        self.project_id = None
        self.novel_path = "千面劫·宿命轮回"

        # 章节文件路径
        self.chapter_files = [
            "第一卷 面具觉醒/第1章  诡异的面具.txt",
            "第一卷 面具觉醒/第2章  好友相见 分外嘴贱.txt",
            "第一卷 面具觉醒/第3章  被选中的孩子.txt",
            "第一卷 面具觉醒/第4章  恶向胆边生.txt",
            "第一卷 面具觉醒/第5章  魔影初现.txt"
        ]

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
        """创建《千面劫·宿命轮回》项目"""
        print("📝 创建《千面劫·宿命轮回》项目...")

        project_data = {
            "name": "千面劫·宿命轮回",
            "description": "高考结束的夜晚，宋少雨在夜市偶遇诡异面具摊，一枚千面面具竟让他觉醒前世仙君身份——千面郎君幻三千！千年前，他因与妖帅灵蜗的禁忌之恋被仙界诛杀，今生却因面具重获力量，也招致妖族追杀与仙界猜忌。",
            "genre": "玄幻",
            "tags": ["宿命轮回", "身份觉醒", "仙妖恋情", "都市修真", "面具觉醒"],
            "status": "writing",
            "author": "原创作者",
            "is_preset": False
        }

        try:
            response = requests.post(f"{self.base_url}/projects/", json=project_data)
            if response.status_code == 200:
                result = response.json()
                self.project_id = result["project"]["id"]
                print(f"✅ 项目创建成功，ID: {self.project_id}")
                return True
            else:
                print(f"❌ 项目创建失败: {response.text}")
                return False
        except Exception as e:
            print(f"❌ 创建项目时出错: {e}")
            return False

    def read_chapter_content(self, chapter_file: str) -> str:
        """读取章节内容"""
        file_path = os.path.join(self.novel_path, chapter_file)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            print(f"❌ 读取章节文件 {chapter_file} 失败: {e}")
            return ""

    def read_novel_concept(self) -> str:
        """读取小说构思"""
        concept_file = os.path.join(self.novel_path, "千面劫·宿命轮回 构思.txt")
        try:
            with open(concept_file, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            print(f"❌ 读取构思文件失败: {e}")
            return ""

    def extract_characters_from_concept(self, concept_content: str) -> List[Dict]:
        """从构思文档中提取人物信息"""
        characters = []

        # 解析构思文档中的角色信息
        character_section = re.search(r'现有角色.*?后续新增角色', concept_content, re.DOTALL)
        if character_section:
            lines = character_section.group(0).split('\n')
            for line in lines:
                if '男/' in line or '女/' in line:
                    parts = line.split('\t')
                    if len(parts) >= 6:
                        name = parts[0].strip()
                        gender_age = parts[1].strip()
                        tag = parts[2].strip()
                        appearance = parts[3].strip()
                        personality = parts[4].strip()
                        ability = parts[5].strip()

                        # 解析性别和年龄
                        gender = "男" if "男/" in gender_age else "女"
                        age_match = re.search(r'/(\d+|未知)', gender_age)
                        age = age_match.group(1) if age_match else "未知"

                        characters.append({
                            "name": name,
                            "gender": gender,
                            "age": age,
                            "appearance": appearance,
                            "personality": personality,
                            "background": tag,
                            "abilities": ability,
                            "importance": "主要" if name in ["宋少雨", "盛百威", "灵蜗"] else "次要",
                            "status": "活跃",
                            "notes": f"标签: {tag}"
                        })

        return characters

    def extract_world_settings_from_concept(self, concept_content: str) -> Dict:
        """从构思文档中提取世界设定"""
        world_settings = {}

        # 提取世界设定部分
        world_section = re.search(r'世界设定.*?核心设定：', concept_content, re.DOTALL)
        if world_section:
            content = world_section.group(0)

            # 双轨世界设定
            if "表世界：" in content:
                surface_world = re.search(r'表世界：(.*?)里世界：', content, re.DOTALL)
                if surface_world:
                    world_settings["surface_world"] = surface_world.group(1).strip()

            if "里世界：" in content:
                inner_world = re.search(r'里世界：(.*?)核心设定：', content, re.DOTALL)
                if inner_world:
                    world_settings["inner_world"] = inner_world.group(1).strip()

        # 提取核心设定
        core_section = re.search(r'核心设定：.*?势力分布：', concept_content, re.DOTALL)
        if core_section:
            world_settings["core_settings"] = core_section.group(0).replace("核心设定：", "").strip()

        return world_settings

    def import_characters(self):
        """导入人物信息"""
        print("👥 导入人物信息...")

        concept_content = self.read_novel_concept()
        characters = self.extract_characters_from_concept(concept_content)

        for char_data in characters:
            try:
                response = requests.post(
                    f"{self.base_url}/project-data/projects/{self.project_id}/data/character",
                    json=char_data
                )
                if response.status_code == 200:
                    print(f"✅ 导入人物: {char_data['name']}")
                else:
                    print(f"❌ 导入人物 {char_data['name']} 失败: {response.text}")
            except Exception as e:
                print(f"❌ 导入人物 {char_data['name']} 时出错: {e}")

    def import_world_settings(self):
        """导入世界设定"""
        print("🌍 导入世界设定...")

        concept_content = self.read_novel_concept()
        world_settings = self.extract_world_settings_from_concept(concept_content)

        # 创建世界设定记录
        world_data = {
            "name": "千面劫世界观",
            "description": "双轨世界：表世界为现代都市，里世界为灵气复苏的修真界",
            "geography": world_settings.get("surface_world", "") + "\n" + world_settings.get("inner_world", ""),
            "history": "千年前仙妖大战，千面郎君与妖帅灵蜗的禁忌之恋引发轮回宿命",
            "culture": world_settings.get("core_settings", ""),
            "natural_laws": "因果法器连接轮回因果，灵气复苏影响修真界",
            "notes": "核心主题：宿命的轮回与身份的觉醒"
        }

        try:
            response = requests.post(
                f"{self.base_url}/project-data/projects/{self.project_id}/data/world_setting",
                json=world_data
            )
            if response.status_code == 200:
                print(f"✅ 导入世界设定: {world_data['name']}")
            else:
                print(f"❌ 导入世界设定失败: {response.text}")
        except Exception as e:
            print(f"❌ 导入世界设定时出错: {e}")

    def import_factions(self):
        """导入势力信息"""
        print("🏛️ 导入势力信息...")

        factions = [
            {
                "name": "天命观",
                "type": "道观",
                "description": "黑星道长所属道观，守护轮回秘术，与仙界敌对",
                "leader": "黑星道长",
                "members": "黑星道长、林小满",
                "territory": "广陵小山坡（已被移除）",
                "strength": "中等",
                "status": "活跃",
                "goals": "守护轮回秘术，对抗仙界阴谋",
                "notes": "天命观最后传人，掌握因果卜算和空间术法"
            },
            {
                "name": "宋氏修真族",
                "type": "修真世家",
                "description": "宋少雨家族，擅长血脉秘法，家主宋书文知晓仙界黑幕",
                "leader": "宋书文",
                "members": "宋书文、宋少雨等族人",
                "territory": "宋氏祖地",
                "strength": "强大",
                "status": "活跃",
                "goals": "保护族人，对抗仙界威胁",
                "notes": "擅长血脉封印术、丹药炼制，与仙界暗中对抗"
            },
            {
                "name": "万妖盟",
                "type": "妖族联盟",
                "description": "灵蜗旧部，部分妖族欲复活灵蜗，部分则想推翻仙界",
                "leader": "分裂状态",
                "members": "各妖族后裔",
                "territory": "妖域",
                "strength": "强大",
                "status": "分裂",
                "goals": "复活灵蜗或推翻仙界",
                "notes": "内部分化严重，对灵蜗态度不一"
            },
            {
                "name": "修真监察局",
                "type": "仙界机构",
                "description": "仙界在人间的执法机构，负责监察修真界",
                "leader": "凌专员",
                "members": "凌专员、诛仙卫等",
                "territory": "人间各地",
                "strength": "极强",
                "status": "活跃",
                "goals": "执行仙界意志，消除威胁",
                "notes": "拥有血符锁链等强力法器，执行灭世计划"
            }
        ]

        for faction_data in factions:
            try:
                response = requests.post(
                    f"{self.base_url}/project-data/projects/{self.project_id}/data/faction",
                    json=faction_data
                )
                if response.status_code == 200:
                    print(f"✅ 导入势力: {faction_data['name']}")
                else:
                    print(f"❌ 导入势力 {faction_data['name']} 失败: {response.text}")
            except Exception as e:
                print(f"❌ 导入势力 {faction_data['name']} 时出错: {e}")

    def import_cultivation_systems(self):
        """导入修炼体系"""
        print("⚡ 导入修炼体系...")

        cultivation_data = {
            "name": "千面劫修炼体系",
            "description": "基于元素能量和血脉力量的修炼体系",
            "levels": [
                "凡人阶段：普通人类，无修炼能力",
                "觉醒阶段：觉醒元素亲和力或血脉力量",
                "初修阶段：能够操控基础元素能量",
                "进阶阶段：掌握高级术法和血脉秘术",
                "散仙阶段：如千面郎君，拥有强大仙力",
                "妖帅阶段：如灵蜗，统领妖族的强者",
                "仙君阶段：仙界高层，掌控天地法则"
            ],
            "methods": [
                "元素修炼：通过冥想感应虚空宇宙能量",
                "血脉觉醒：激活体内潜藏的血脉力量",
                "法器辅助：使用因果法器增强修炼效果",
                "丹药辅助：服用各种修炼丹药"
            ],
            "characteristics": [
                "魔心天生：如盛百威，天生与各种能量契合度极高",
                "血脉传承：如宋氏血脉秘法",
                "因果轮回：通过因果法器觉醒前世能力",
                "妖族血统：拥有妖族血脉的特殊能力"
            ],
            "notes": "修炼体系融合了仙、妖、魔三种力量体系"
        }

        try:
            response = requests.post(
                f"{self.base_url}/project-data/projects/{self.project_id}/data/cultivation_system",
                json=cultivation_data
            )
            if response.status_code == 200:
                print(f"✅ 导入修炼体系: {cultivation_data['name']}")
            else:
                print(f"❌ 导入修炼体系失败: {response.text}")
        except Exception as e:
            print(f"❌ 导入修炼体系时出错: {e}")

    def import_plots(self):
        """导入剧情信息"""
        print("📖 导入剧情信息...")

        plots = [
            {
                "title": "千面面具觉醒",
                "type": "主线",
                "description": "宋少雨在夜市获得千面面具，觉醒前世记忆",
                "status": "进行中",
                "importance": "核心",
                "participants": "宋少雨、黑星道长、灵蜗",
                "location": "邻镇夜市",
                "timeline": "高考结束后",
                "outcome": "宋少雨获得千面面具，开始觉醒前世记忆",
                "notes": "故事的起点，引发后续所有事件"
            },
            {
                "title": "盛百威魔物觉醒",
                "type": "主线",
                "description": "盛百威体内魔物初现，展现魔心天生能力",
                "status": "进行中",
                "importance": "核心",
                "participants": "盛百威、哈森、盛雅奇",
                "location": "苏格兰诊所、宋氏祖地",
                "timeline": "与面具觉醒同期",
                "outcome": "盛百威觉醒元素能力，体内魔物显现",
                "notes": "与宋少雨的命运线交织，双主角设定"
            },
            {
                "title": "仙界追杀",
                "type": "主线",
                "description": "修真监察局追查千面面具，与宋少雨发生冲突",
                "status": "进行中",
                "importance": "核心",
                "participants": "凌专员、宋少雨、宋书文、诛仙卫",
                "location": "宋氏祖地祠堂",
                "timeline": "面具觉醒后",
                "outcome": "千面面具完整觉醒，仙界阴谋初露",
                "notes": "揭示仙界才是真正的反派势力"
            },
            {
                "title": "前世因果揭示",
                "type": "背景",
                "description": "灵蜗向宋少雨揭示千年前的仙妖大战真相",
                "status": "已完成",
                "importance": "重要",
                "participants": "千面郎君（幻三千）、妖帅灵蜗、仙界",
                "location": "赤湖、万妖岭",
                "timeline": "千年前",
                "outcome": "千面被诛杀，灵蜗自封妖胎等待轮回",
                "notes": "整个故事的背景设定，解释轮回宿命的由来"
            }
        ]

        for plot_data in plots:
            try:
                response = requests.post(
                    f"{self.base_url}/project-data/projects/{self.project_id}/data/plot",
                    json=plot_data
                )
                if response.status_code == 200:
                    print(f"✅ 导入剧情: {plot_data['title']}")
                else:
                    print(f"❌ 导入剧情 {plot_data['title']} 失败: {response.text}")
            except Exception as e:
                print(f"❌ 导入剧情 {plot_data['title']} 时出错: {e}")

    def import_volumes_and_chapters(self):
        """导入卷宗和章节"""
        print("📚 导入卷宗和章节...")

        # 创建第一卷
        volume_data = {
            "title": "第一卷 面具觉醒",
            "description": "宋少雨获得千面面具，觉醒前世记忆，好友盛百威体内魔物初现",
            "order_index": 1,
            "status": "writing",
            "notes": "夙世恩怨面具觉醒篇"
        }

        try:
            response = requests.post(
                f"{self.base_url}/project-data/projects/{self.project_id}/data/volume",
                json=volume_data
            )
            if response.status_code == 200:
                volume_id = response.json()["data"]["id"]
                print(f"✅ 创建卷宗: {volume_data['title']}")

                # 导入章节
                for i, chapter_file in enumerate(self.chapter_files, 1):
                    chapter_content = self.read_chapter_content(chapter_file)
                    if chapter_content:
                        chapter_title = os.path.basename(chapter_file).replace('.txt', '')

                        chapter_data = {
                            "title": chapter_title,
                            "content": chapter_content,
                            "volume_id": volume_id,
                            "order_index": i,
                            "word_count": len(chapter_content),
                            "status": "completed",
                            "summary": self.generate_chapter_summary(chapter_content, chapter_title),
                            "notes": f"第一卷第{i}章"
                        }

                        try:
                            chapter_response = requests.post(
                                f"{self.base_url}/project-data/projects/{self.project_id}/data/chapter",
                                json=chapter_data
                            )
                            if chapter_response.status_code == 200:
                                print(f"✅ 导入章节: {chapter_title}")
                            else:
                                print(f"❌ 导入章节 {chapter_title} 失败: {chapter_response.text}")
                        except Exception as e:
                            print(f"❌ 导入章节 {chapter_title} 时出错: {e}")
            else:
                print(f"❌ 创建卷宗失败: {response.text}")
        except Exception as e:
            print(f"❌ 创建卷宗时出错: {e}")

    def generate_chapter_summary(self, content: str, title: str) -> str:
        """生成章节摘要"""
        # 简单的摘要生成逻辑
        if "第1章" in title:
            return "宋少雨在夜市遇到黑星道长，获得千面面具，面具显现异象"
        elif "第2章" in title:
            return "盛百威在苏格兰治疗后回国，展现魔心天生能力，与宋少雨重逢"
        elif "第3章" in title:
            return "宋少雨用血液激活千面面具，与灵蜗建立联系，盛百威发现自己的异常"
        elif "第4章" in title:
            return "灵蜗向宋少雨揭示前世真相，盛百威梦见体内魔物，两人命运交织"
        elif "第5章" in title:
            return "修真监察局追查千面面具，宋少雨与诛仙卫交战，盛百威觉醒噬心魔"
        else:
            return content[:100] + "..." if len(content) > 100 else content

    def import_timelines(self):
        """导入时间线信息"""
        print("⏰ 导入时间线信息...")

        timelines = [
            {
                "title": "千年前仙妖大战",
                "description": "千面郎君与妖帅灵蜗的七次大战及最终结局",
                "event_type": "历史事件",
                "date": "千年前",
                "participants": "千面郎君（幻三千）、妖帅灵蜗、仙界众仙",
                "location": "赤湖、万妖岭",
                "importance": "核心",
                "outcome": "千面被诛杀，灵蜗自封妖胎，设定轮回因果",
                "notes": "整个故事的历史背景，决定了现世的宿命轮回"
            },
            {
                "title": "高考结束夜",
                "description": "宋少雨在夜市遇到黑星道长，获得千面面具",
                "event_type": "关键转折",
                "date": "现代（故事开始）",
                "participants": "宋少雨、黑星道长、吴适、马侯、萧九",
                "location": "邻镇夜市",
                "importance": "核心",
                "outcome": "宋少雨获得千面面具，开始觉醒前世记忆",
                "notes": "故事的起点，命运轮回的开始"
            },
            {
                "title": "盛百威回国",
                "description": "盛百威在苏格兰治疗后回国，与宋少雨重逢",
                "event_type": "人物汇合",
                "date": "面具觉醒后数日",
                "participants": "盛百威、哈森、盛雅奇、宋少雨、宋书文",
                "location": "机场、宋氏祖地",
                "importance": "重要",
                "outcome": "双主角汇合，魔物觉醒线与面具觉醒线交汇",
                "notes": "两条主线开始交织，命运共同体形成"
            },
            {
                "title": "千面面具完全觉醒",
                "description": "宋少雨用血液激活面具，与灵蜗建立完整联系",
                "event_type": "力量觉醒",
                "date": "回国当日",
                "participants": "宋少雨、灵蜗、宋书文、盛百威",
                "location": "宋氏祖地",
                "importance": "核心",
                "outcome": "千面面具完全觉醒，宋少雨获得变化能力",
                "notes": "标志着主角正式踏入修真世界"
            },
            {
                "title": "修真监察局袭击",
                "description": "凌专员率诛仙卫袭击宋氏祖地，争夺千面面具",
                "event_type": "重大冲突",
                "date": "面具觉醒后",
                "participants": "凌专员、诛仙卫、宋少雨、宋书文、盛百威",
                "location": "宋氏祖地祠堂",
                "importance": "核心",
                "outcome": "千面面具融合青铜面具碎片，仙界阴谋暴露",
                "notes": "第一卷的高潮，揭示真正的敌人是仙界"
            }
        ]

        for timeline_data in timelines:
            try:
                response = requests.post(
                    f"{self.base_url}/project-data/projects/{self.project_id}/data/timeline",
                    json=timeline_data
                )
                if response.status_code == 200:
                    print(f"✅ 导入时间线: {timeline_data['title']}")
                else:
                    print(f"❌ 导入时间线 {timeline_data['title']} 失败: {response.text}")
            except Exception as e:
                print(f"❌ 导入时间线 {timeline_data['title']} 时出错: {e}")

    def run(self):
        """执行完整的导入流程"""
        print("🚀 开始导入《千面劫·宿命轮回》数据...")
        print("=" * 60)

        # 1. 清空现有项目
        self.clear_all_projects()
        print()

        # 2. 创建新项目
        if not self.create_novel_project():
            print("❌ 项目创建失败，终止导入")
            return False
        print()

        # 3. 导入卷宗和章节
        self.import_volumes_and_chapters()
        print()

        # 4. 导入人物信息
        self.import_characters()
        print()

        # 5. 导入势力信息
        self.import_factions()
        print()

        # 6. 导入世界设定
        self.import_world_settings()
        print()

        # 7. 导入修炼体系
        self.import_cultivation_systems()
        print()

        # 8. 导入剧情信息
        self.import_plots()
        print()

        # 9. 导入时间线
        self.import_timelines()
        print()

        print("🎉 《千面劫·宿命轮回》数据导入完成！")
        print(f"📊 项目ID: {self.project_id}")
        print("📚 已导入内容：")
        print("   - 1个卷宗（第一卷 面具觉醒）")
        print("   - 5个章节（完整正文内容）")
        print("   - 6个主要人物")
        print("   - 4个重要势力")
        print("   - 1个世界设定")
        print("   - 1个修炼体系")
        print("   - 4个核心剧情")
        print("   - 5个关键时间线节点")
        print("=" * 60)
        return True

if __name__ == "__main__":
    importer = QianMianJieImporter()
    importer.run()
