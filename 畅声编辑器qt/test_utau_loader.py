import sys
from utau_loader import UTAULoader
import os

# 测试UTAU声库加载器
if __name__ == "__main__":
    print("UTAU声库加载器测试工具")
    print("=" * 50)
    
    # 创建UTAU加载器实例
    loader = UTAULoader()
    
    # 检查是否提供了声库路径参数
    if len(sys.argv) > 1:
        voicebank_path = sys.argv[1]
    else:
        # 如果没有提供参数，提示用户输入
        voicebank_path = input("请输入UTAU声库文件夹路径: ")
    
    # 检查路径是否存在
    if not os.path.exists(voicebank_path):
        print(f"错误: 路径 '{voicebank_path}' 不存在")
        sys.exit(1)
    
    print(f"\n正在加载UTAU声库: {voicebank_path}")
    
    # 加载声库
    voicebank_info = loader.load_voicebank(voicebank_path)
    
    if voicebank_info:
        print("\n声库加载成功!")
        print("\n声库信息:")
        print(f"- 名称: {voicebank_info['name']}")
        print(f"- 路径: {voicebank_info['path']}")
        print(f"- 是否有效: {'是' if voicebank_info['valid'] else '否'}")
        
        # 显示角色信息
        if voicebank_info['character_info']:
            print("\n角色信息:")
            for key, value in voicebank_info['character_info'].items():
                print(f"- {key}: {value}")
        else:
            print("\n未找到角色信息 (character.txt)")
        
        # 显示采样文件信息
        print(f"\n采样文件数量: {len(voicebank_info['sample_files'])}")
        if voicebank_info['sample_files']:
            print("前5个采样文件:")
            for file in voicebank_info['sample_files'][:5]:
                print(f"- {os.path.basename(file)}")
            if len(voicebank_info['sample_files']) > 5:
                print(f"... 还有{len(voicebank_info['sample_files']) - 5}个文件")
        
        # 显示Oto配置信息
        if voicebank_info['oto_configs']:
            print("\nOto配置信息:")
            for section, configs in voicebank_info['oto_configs'].items():
                print(f"- {section}部分 ({len(configs)}个配置)")
                
                # 显示前3个配置作为示例
                for i, config in enumerate(configs[:3]):
                    print(f"  {i+1}. {config['alias']} ({config['wav_file']})")
                    print(f"     偏移: {config['offset']}, 辅音: {config['consonant']}, 元音: {config['vowel']}")
                
                if len(configs) > 3:
                    print(f"  ... 还有{len(configs) - 3}个配置")
        else:
            print("\n未找到Oto配置信息")
        
        print("\n测试完成!")
    else:
        print("\n声库加载失败!")
        print("请确保选择的是有效的UTAU声库文件夹。")
        sys.exit(1)