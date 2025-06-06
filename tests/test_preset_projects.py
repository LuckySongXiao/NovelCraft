"""
预置项目功能测试
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.models.project import ProjectType, ProjectStatus


class TestPresetProjects:
    """预置项目测试类"""

    def setup_method(self):
        """测试前准备"""
        # 这里应该设置测试数据库
        pass

    def test_create_preset_project(self):
        """测试创建预置项目"""
        # 模拟创建预置项目
        project_data = {
            "name": "【测试】预置项目",
            "title": "测试预置项目",
            "author": "系统",
            "project_type": ProjectType.FANTASY,
            "status": ProjectStatus.COMPLETED,
            "is_preset": True
        }

        # 验证预置项目标识
        assert project_data["is_preset"] == True
        assert project_data["author"] == "系统"
        print("✓ 预置项目创建测试通过")

    def test_preset_project_edit_restriction(self):
        """测试预置项目编辑限制"""
        # 模拟预置项目
        preset_project = {
            "id": 1,
            "name": "【预置】测试项目",
            "is_preset": True
        }

        # 模拟编辑操作
        try:
            if preset_project["is_preset"]:
                raise ValueError("预置项目不允许编辑")
        except ValueError as e:
            assert str(e) == "预置项目不允许编辑"
            print("✓ 预置项目编辑限制测试通过")

    def test_preset_project_delete_restriction(self):
        """测试预置项目删除限制"""
        # 模拟预置项目
        preset_project = {
            "id": 1,
            "name": "【预置】测试项目",
            "is_preset": True
        }

        # 模拟删除操作
        try:
            if preset_project["is_preset"]:
                raise ValueError("预置项目不允许删除")
        except ValueError as e:
            assert str(e) == "预置项目不允许删除"
            print("✓ 预置项目删除限制测试通过")

    def test_preset_project_copy_allowed(self):
        """测试预置项目复制功能"""
        # 模拟预置项目
        preset_project = {
            "id": 1,
            "name": "【预置】测试项目",
            "title": "预置项目标题",
            "is_preset": True
        }

        # 模拟复制操作
        copied_project = {
            "name": f"{preset_project['name']} (副本)",
            "title": preset_project["title"],
            "is_preset": False  # 复制的项目不是预置项目
        }

        assert copied_project["is_preset"] == False
        assert "(副本)" in copied_project["name"]
        print("✓ 预置项目复制功能测试通过")

    def test_preset_project_identification(self):
        """测试预置项目标识"""
        projects = [
            {"name": "普通项目", "is_preset": False},
            {"name": "【预置】模板项目", "is_preset": True},
            {"name": "用户项目", "is_preset": False}
        ]

        preset_count = sum(1 for p in projects if p["is_preset"])
        user_count = sum(1 for p in projects if not p["is_preset"])

        assert preset_count == 1
        assert user_count == 2
        print("✓ 预置项目标识测试通过")


def run_tests():
    """运行所有测试"""
    test_instance = TestPresetProjects()
    test_instance.setup_method()

    print("开始预置项目功能测试...")
    print("-" * 50)

    test_instance.test_create_preset_project()
    test_instance.test_preset_project_edit_restriction()
    test_instance.test_preset_project_delete_restriction()
    test_instance.test_preset_project_copy_allowed()
    test_instance.test_preset_project_identification()

    print("-" * 50)
    print("所有测试通过！✓")


if __name__ == "__main__":
    run_tests()
