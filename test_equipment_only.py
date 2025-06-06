#!/usr/bin/env python3
"""
单独测试装备体系模型的脚本
"""
import sys
import os

# 添加后端路径到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_equipment_system():
    """测试装备体系模型"""
    try:
        print("正在导入装备体系模型...")
        from app.models.equipment_system import EquipmentSystem, EquipmentType, EquipmentGrade
        print("✓ 装备体系模型导入成功")

        print("正在创建装备实例...")
        equipment = EquipmentSystem(
            name="青云剑",
            description="青云宗的传承宝剑",
            equipment_type=EquipmentType.WEAPON,
            equipment_grade=EquipmentGrade.RARE
        )
        print("✓ 装备实例创建成功")

        print("正在设置威力属性...")
        equipment.offensive_power = 150.0
        equipment.defensive_power = 100.0
        print(f"✓ 攻击力: {equipment.offensive_power}, 防御力: {equipment.defensive_power}")

        print("正在添加特殊能力...")
        equipment.add_special_ability({
            "name": "青云斩",
            "description": "释放青云剑气",
            "power": 200
        })
        print("✓ 特殊能力添加成功")

        print("正在计算装备评分...")
        score = equipment.calculate_equipment_score()
        print(f"✓ 装备评分计算成功: {score:.1f}")

        print("✓ 装备体系测试通过")
        return True

    except Exception as e:
        print(f"✗ 装备体系测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("开始单独测试装备体系...")
    print("=" * 50)
    success = test_equipment_system()
    print("=" * 50)
    if success:
        print("🎉 装备体系测试成功！")
    else:
        print("❌ 装备体系测试失败！")
    sys.exit(0 if success else 1)
