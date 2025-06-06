#!/usr/bin/env python3
"""
测试所有新增体系模型的脚本
"""
import sys
import os

# 添加后端路径到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_equipment_system():
    """测试装备体系模型"""
    try:
        from app.models.equipment_system import EquipmentSystem, EquipmentType, EquipmentGrade

        equipment = EquipmentSystem(
            name="青云剑",
            description="青云宗的传承宝剑",
            equipment_type=EquipmentType.WEAPON,
            equipment_grade=EquipmentGrade.RARE
        )

        # 设置威力属性
        equipment.offensive_power = 150.0
        equipment.defensive_power = 100.0

        equipment.add_special_ability({
            "name": "青云斩",
            "description": "释放青云剑气",
            "power": 200
        })

        score = equipment.calculate_equipment_score()
        print(f"✓ 装备体系测试通过 - 装备评分: {score:.1f}")
        return True

    except Exception as e:
        print(f"✗ 装备体系测试失败: {e}")
        return False

def test_pet_system():
    """测试宠物体系模型"""
    try:
        from app.models.pet_system import PetSystem, PetType, PetRarity

        pet = PetSystem(
            name="青鸾",
            description="传说中的神鸟",
            pet_type=PetType.MYTHICAL,
            pet_rarity=PetRarity.LEGENDARY,
            current_level=50,
            max_level=100
        )

        pet.add_innate_skill({
            "name": "凤凰涅槃",
            "description": "重生技能",
            "cooldown": 3600
        })

        combat_power = pet.calculate_combat_power()
        print(f"✓ 宠物体系测试通过 - 战斗力: {combat_power:.1f}")
        return True

    except Exception as e:
        print(f"✗ 宠物体系测试失败: {e}")
        return False

def test_map_structure():
    """测试地图结构模型"""
    try:
        from app.models.map_structure import MapStructure, MapType, TerrainType

        map_area = MapStructure(
            name="青云山脉",
            description="青云宗所在的山脉",
            map_type=MapType.REGION,
            terrain_type=TerrainType.MOUNTAIN,
            area_size=10000.0
        )

        map_area.add_settlement({
            "name": "青云宗",
            "type": "sect",
            "population": 5000
        })

        danger_level = map_area.calculate_danger_level()
        print(f"✓ 地图结构测试通过 - 危险等级: {danger_level:.1f}")
        return True

    except Exception as e:
        print(f"✗ 地图结构测试失败: {e}")
        return False

def test_dimension_structure():
    """测试维度结构模型"""
    try:
        from app.models.dimension_structure import DimensionStructure, DimensionType, DimensionStability

        dimension = DimensionStructure(
            name="灵界",
            description="修仙者的精神世界",
            dimension_type=DimensionType.SPIRITUAL,
            stability=DimensionStability.STABLE,
            time_flow=0.5
        )

        dimension.add_portal({
            "name": "灵界之门",
            "location": "青云宗后山",
            "activation": "灵力激活"
        })

        danger_level = dimension.calculate_danger_level()
        print(f"✓ 维度结构测试通过 - 危险等级: {danger_level:.1f}")
        return True

    except Exception as e:
        print(f"✗ 维度结构测试失败: {e}")
        return False

def test_spiritual_treasure_system():
    """测试灵宝体系模型"""
    try:
        from app.models.spiritual_treasure_system import SpiritualTreasureSystem, TreasureType, TreasureGrade

        treasure = SpiritualTreasureSystem(
            name="混元金丹",
            description="传说中的仙丹",
            treasure_type=TreasureType.PILL,
            treasure_grade=TreasureGrade.SAINT,
            spiritual_power=1000.0
        )

        treasure.add_special_ability({
            "name": "境界突破",
            "description": "帮助修仙者突破境界",
            "success_rate": 90
        })

        total_power = treasure.calculate_total_power()
        print(f"✓ 灵宝体系测试通过 - 总体威力: {total_power:.1f}")
        return True

    except Exception as e:
        print(f"✗ 灵宝体系测试失败: {e}")
        return False

def test_resource_distribution():
    """测试资源分布模型"""
    try:
        from app.models.resource_distribution import ResourceDistribution, ResourceType, ResourceRarity

        resource = ResourceDistribution(
            resource_name="灵石矿脉",
            resource_type=ResourceType.MAGICAL,
            resource_rarity=ResourceRarity.RARE,
            market_value=1000.0
        )

        resource.add_concentration_area({
            "name": "青云山灵石矿",
            "coordinates": {"x": 100, "y": 200},
            "reserves": 50000
        })

        economic_value = resource.calculate_economic_value()
        print(f"✓ 资源分布测试通过 - 经济价值: {economic_value:.1f}")
        return True

    except Exception as e:
        print(f"✗ 资源分布测试失败: {e}")
        return False

def test_race_distribution():
    """测试种族分布模型"""
    try:
        from app.models.race_distribution import RaceDistribution, PopulationDensity, DominanceLevel

        race_dist = RaceDistribution(
            race_name="人族",
            population_density=PopulationDensity.HIGH,
            dominance_level=DominanceLevel.MAJORITY,
            total_population=1000000
        )

        race_dist.add_primary_territory({
            "name": "中原大陆",
            "area": 500000,
            "control_level": "complete"
        })

        influence_level = race_dist.calculate_influence_level()
        print(f"✓ 种族分布测试通过 - 影响力等级: {influence_level:.1f}")
        return True

    except Exception as e:
        print(f"✗ 种族分布测试失败: {e}")
        return False

def test_secret_realm_distribution():
    """测试秘境分布模型"""
    try:
        from app.models.secret_realm_distribution import SecretRealmDistribution, RealmType, DangerLevel

        secret_realm = SecretRealmDistribution(
            name="青云秘境",
            description="青云宗的试炼之地",
            realm_type=RealmType.TRIAL,
            danger_level=DangerLevel.MODERATE,
            floor_levels=10
        )

        secret_realm.add_treasure({
            "name": "青云心法",
            "type": "technique",
            "rarity": "rare"
        })

        difficulty_score = secret_realm.calculate_difficulty_score()
        print(f"✓ 秘境分布测试通过 - 难度评分: {difficulty_score:.1f}")
        return True

    except Exception as e:
        print(f"✗ 秘境分布测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("开始测试所有新增体系模型...")
    print("=" * 60)

    tests = [
        ("装备体系", test_equipment_system),
        ("宠物体系", test_pet_system),
        ("地图结构", test_map_structure),
        ("维度结构", test_dimension_structure),
        ("灵宝体系", test_spiritual_treasure_system),
        ("资源分布", test_resource_distribution),
        ("种族分布", test_race_distribution),
        ("秘境分布", test_secret_realm_distribution)
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n测试 {test_name}:")
        print("-" * 30)
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} 测试失败")

    print("\n" + "=" * 60)
    print(f"测试结果: {passed}/{total} 通过")

    if passed == total:
        print("🎉 所有新增体系模型测试通过！")
        print("\n新增的体系包括：")
        print("📦 设定管理：装备体系、宠物体系、地图结构、维度结构、灵宝体系")
        print("📊 内容管理：资源分布、种族分布、秘境分布")
        return True
    else:
        print("❌ 部分测试失败，请检查错误信息")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
