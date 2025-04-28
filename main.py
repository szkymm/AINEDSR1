#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from datetime import datetime

from mode.mode_DPSK_Apic import ClassDeepSeekHand


class NovelEditorSystem:
    """主业务逻辑模块"""

    def __init__(self):
        self.api_handler = ClassDeepSeekHand()
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self._init_directories()
        self.task_profiles = {
            1: self._load_task_profile("文段理解处理", "text_PUP_Tas.md", 60)
            }

    def _init_directories(self):
        """初始化目录结构"""
        required_dirs = {
            "config": "API配置目录",
            "text": "系统提示目录",
            "data": "输入数据目录",
            "results": "处理结果目录",
            "logs/main": "系统日志目录"
            }

        for dir_name, desc in required_dirs.items():
            full_path = os.path.join(self.base_dir, dir_name)
            if not os.path.exists(full_path):
                os.makedirs(full_path)
                print(f"已创建 {desc}: {full_path}")

    def _load_task_profile(self, name, prompt_file, chunk_size):
        """加载任务配置"""
        return {
            "name": name,
            "prompt_path": os.path.join("text", prompt_file),
            "chunk_size": chunk_size
            }

    def _show_menu(self):
        """显示交互菜单"""
        print("\n" + "=" * 40)
        print(" DeepSeek小说编辑系统 ".center(40, "★"))
        print("=" * 40)
        print("[1] 文段理解处理")
        print("[0] 退出系统")
        print("=" * 40)

    def run(self):
        """主运行循环"""
        while True:
            self._show_menu()
            choice = input("请选择操作编号: ").strip()

            if choice == "0":
                print("\n系统已安全退出")
                break

            if choice == "1":
                self._execute_processing_task()
            else:
                print("无效的选项，请重新输入")

    def _execute_processing_task(self):
        """执行处理任务"""
        print("\n▶ 正在启动文段理解处理模式...")

        try:
            # 加载系统提示
            prompt_path = self.task_profiles[1]["prompt_path"]
            with open(prompt_path, "r", encoding="utf-8") as f:
                system_prompt = f.read()

            # 加载用户内容
            content = self._load_user_content()

            # 执行处理流程
            result_path = self._generate_result_path()
            self._process_content(content, system_prompt, result_path)

            print(f"\n✅ 处理完成！结果文件已保存至:\n{result_path}")

        except Exception as e:
            print(f"\n❌ 处理过程中发生错误: {str(e)}")

    def _load_user_content(self):
        """加载用户内容"""
        data_path = os.path.join("data", "data_MAIN_Info.md")
        try:
            with open(data_path, "r", encoding="utf-8") as f:
                content = f.read()
            if not content:
                raise ValueError("输入文件为空")
            return content
        except FileNotFoundError:
            raise RuntimeError(f"未找到输入文件: {data_path}")

    def _generate_result_path(self):
        """生成结果文件路径"""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"Result_Processed_{timestamp}.md"
        return os.path.join("results", filename)

    def _process_content(self, content, system_prompt, result_path):
        """执行内容处理"""
        chunk_size = self.task_profiles[1]["chunk_size"]
        total_chars = len(content)

        with open(result_path, "w", encoding="utf-8") as result_file:
            for i in range(0, total_chars, chunk_size):
                chunk = content[i:i + chunk_size]
                try:
                    processed = self.api_handler.process_request(system_prompt, chunk)
                except Exception as e:
                    raise RuntimeError(f"处理中断: {str(e)}")

                result_file.write(f"{processed}\n\n")
                progress = min((i + chunk_size) / total_chars * 100, 100)
                print(f"\r▷ 处理进度: {progress:.1f}%", end="", flush=True)


if __name__ == "__main__":
    try:
        # 首次运行检查
        if not os.path.exists("config/api_key.txt"):
            print("首次使用配置指南：")
            api_key = input("请输入DeepSeek API密钥: ").strip()
            with open("config/api_key.txt", "w") as f:
                f.write(api_key)
            print("密钥已安全存储")

        NovelEditorSystem().run()

    except Exception as e:
        print(f"\n❗ 系统启动失败: {str(e)}")
        print("建议检查：")
        print("1. API密钥有效性")
        print("2. 网络连接状态")
        print("3. 必要文件是否存在")
        input("按任意键退出...")
