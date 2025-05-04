#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import re
import sys
from datetime import datetime
from pathlib import Path

from mode.mode_DPSK_Apic import ClassDeepSeekHand


class NovelEditorSystem:
    def __init__(self):
        self.base_dir = Path(sys.argv[0]).resolve().parent  # 基础文件夹
        self.data_dir = self.base_dir / "data"  # 数据文件夹
        self.text_dir = self.base_dir / "text"  # 指令文件夹
        self.logs_dir = self.base_dir / "logs"  # 日志文件夹
        self.results_dir = self.base_dir / "results"  # 结果文件夹
        self.config_dir = self.base_dir / "config"  # 配置文件夹
        self.logger = None
        self.api_handler = None
        self._init_logger()
        self._init_api_handler()
        self._init_directories()
        self.task_profiles = {
            1: self._load_task_profile("文段理解处理", "text_SYST_Inst.md", 20),
            2: self._load_task_profile("文段整合处理", "text_TAII_Prmt.md", 120),
            }

    def _init_logger(self):
        self.logger = logging.getLogger("NovelEditorSystem")
        self.logger.setLevel(logging.INFO)
        log_dir = self.base_dir / "logs"
        log_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%m%d_%H%M")
        log_filename = f"logs_{timestamp}.log"
        formatter = logging.Formatter(
                '[%(asctime)s] %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
                )
        file_handler = logging.FileHandler(log_dir / log_filename, encoding="utf-8")
        file_handler.setFormatter(formatter)
        if not any(isinstance(h, logging.FileHandler) for h in self.logger.handlers):
            self.logger.addHandler(file_handler)
        self.logger.info("✅ 日志处理器初始化正常、结束。")

    def _init_api_handler(self):
        try:
            self.api_handler = ClassDeepSeekHand(logger=self.logger)
            self.logger.info("✅ API处理器初始化正常、结束。")
        except Exception as exception_error:
            self.logger.error(f"API处理器初始化失败: {exception_error}")
            raise RuntimeError("API处理器初始化失败，请检查配置文件和网络连接。")

    def _init_directories(self):
        required_dirs = {
            "config": "API配置目录",
            "text": "系统提示目录",
            "data": "输入数据目录",
            "results": "处理结果目录",
            "logs": "系统日志目录"
            }
        for dir_name, desc in required_dirs.items():
            full_path = self.base_dir / dir_name
            if not full_path.exists():
                full_path.mkdir()
                self.logger.info(f"已创建 {desc}: {full_path}")
                print(f"已创建 {desc}: {full_path}")

    def _load_task_profile(self, name, prompt_file, chunk_size):
        return {
            "name": name,
            "prompt_path": self.text_dir / prompt_file,
            "chunk_size": chunk_size
            }

    @staticmethod
    def _show_menu():
        print("\n" + "=" * 40)
        print(" DeepSeek小说编辑系统 ".center(15, "★"))
        print("=" * 40)
        print("[1] 💬 文段理解处理。")
        print("[2] 💬 文段整合处理。")
        print("[0] ❗ 退出系统。")
        print("=" * 40)

    def run(self):
        print("程序启动 ❗")
        self.logger.info("系统初始化正常、结束，脚本开始运行。")
        while True:
            self.logger.info("主程序启动，显示交互菜单。")
            self._show_menu()
            choice = input("请选择操作编号: ").strip()
            self.logger.info(f"用户输入: {choice}选项，开始执行。")
            if choice == "0":
                print("\n❗ 系统已安全退出。")
                self.logger.info("❗ 用户自行退出程序。")
                break
            elif choice == "1":
                self.logger.info("💬 文段理解处理模式已开启。")
                print("💬 用户选择1，文段理解处理模式已开启。")
                file_data = "data_CTAX_Info.md"
                self._execute_processing_task(choice, file_data)
            elif choice == "2":
                self.logger.info("💬 文段整合处理模式已开启。")
                print("💬 用户选择2，文段整合处理模式已开启。")
                file_data = "data_TXAN_Info.md"
                self._execute_processing_task(choice, file_data)
            else:
                self.logger.warning("❌ 用户输入无效选项，提示重新输入。")
                print("❌ 无效的选项，请重新输入。")

    def _execute_processing_task(self, choice_number, file_path):
        number = int(choice_number)
        try:
            task_profile = self.task_profiles.get(number)
            if not task_profile or "prompt_path" not in task_profile:
                self.logger.error("❌ 配置文件中缺少有效的提示文件路径。")
                print("\n❌ 配置文件中缺少有效的提示文件路径。")
                return
            prompt_path = task_profile["prompt_path"]
            if not prompt_path.exists():
                self.logger.error(f"❌ 提示文件路径无效或文件不存在: {prompt_path}。")
                print(f"\n❌ 提示文件路径无效或文件不存在: {prompt_path}。")
                return
            with open(prompt_path, "r", encoding="utf-8") as objt_file:
                system_prompt = objt_file.read()
                self.logger.info(f"✅ 提示文件: {prompt_path.name}，正常读取。")
                print("✅ 提示文件正常读取。")
            content = self._load_user_content(file_path)
            self.logger.info("💬 开始读取用户内容")
            if not content:
                self.logger.error("❌ 用户内容为空，无法继续处理。")
                print("\n❌ 用户内容为空，无法继续处理。")
                return
            self.logger.info(f"💬 用户内容为:\n {content}\n")
            self.logger.info("✅ 用户内容文件正常读取。")
            result_path = self._generate_result_path()
            if not result_path:
                self.logger.error("❌ 结果文件路径生成失败。")
                print("\n❌ 结果文件路径生成失败。")
                return
            self.logger.info(f"✅ 结果文件：{result_path.name}已生成。")
            self.logger.info("💬 开始发送文段，进行处理。")
            print("💬 开始发送文段，进行处理。")
            chunk_size = task_profile["chunk_size"]
            self._process_content(chunk_size, content, system_prompt, result_path)
            self.logger.info(f"✅ 处理结束，结果已保存。")
            print(f"\n✅ 处理完成！结果文件已保存至:\n{result_path.name}。")
        except Exception as exception_error:
            self.logger.error(f"❌ 处理过程中发生未知错误: {exception_error}")
            print(f"\n❌ 处理过程中发生未知错误: {exception_error}")

    def _load_user_content(self, data_info):
        data_path = self.data_dir / data_info
        if not data_path.exists():
            self.logger.error(f"❌ 未找到输入文件: {data_path}")
            print(f"\n❌ 未找到输入文件: {data_path}")
            raise FileExistsError(f"未找到输入文件: {data_path}")
        with open(data_path, "r", encoding="utf-8") as objt_file:
            content = objt_file.read()
        if not content.strip().startswith("#"):
            self.logger.error("❌ 用户输入文件格式不正确，可能缺少标题。")
            print("\n❌ 用户输入文件格式不正确，可能缺少标题。")
            return ""
        return content

    def _generate_result_path(self):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"Result_{timestamp}.md"
        return self.results_dir / filename

    def extract_optimized_text(self, file_input):
        try:
            file_name = file_input.name
            output_file_name = f"Content_{file_name}.md"
            with open(file_input, "r", encoding="utf-8") as reading_file:
                content = reading_file.read()
            matches = re.findall(r"```plaintext(.*?)```", content, re.DOTALL)
            if matches:
                result_content = ""
                for match in matches:
                    gain_content = match.strip()
                    processed_content = "  \n".join(gain_content.splitlines())
                    processed_content = re.sub(r" {4,}\n", "  \n", processed_content)
                    result_content += processed_content + "\n\n"
                output_file_path = self.results_dir / output_file_name
                with open(output_file_path, "w", encoding="utf-8") as writing_file:
                    writing_file.write(result_content)
                print(f"✅ 成功提取并保存所有内容块到文件: {output_file_name}")
            else:
                print(f"❌ 未发现匹配的内容块: {file_input}")
                raise FileExistsError(f"❌ 未发现匹配的内容块: {file_input}")
        except Exception as exception_error:
            self.logger.error(f"发现了一个未知错误: {exception_error}")
            print(f"发现了一个未知错误: {exception_error}")

    def _process_content(self, chunk_size, content, system_prompt, result_path):
        lines = content.split('\n')
        range_number = 0
        with open(result_path, "w", encoding="utf-8") as result_file:
            result_file.write("# DeepSeek-R1处理结果\n\n")
        for i in range(0, len(lines), chunk_size):
            chunk_lines = lines[i:i + chunk_size]
            chunk = '\n'.join(chunk_lines)
            range_number += 1
            try:
                self.logger.info(f"✅ 第{str(range_number)}组已提交，等待API反馈。")
                processed, reasoning = self.api_handler.process_request(system_prompt, chunk)
            except Exception as exception_error:
                self.logger.error(f"❌ 处理请求失败: {exception_error}")
                print(f"\n❌ 处理请求失败: {exception_error}")
                return
            self.logger.info(f"✅ 第{str(range_number)}组API已反馈，正在处理写入。")
            reason_content = "<br>".join(reasoning.splitlines()).replace("<br><br>", "<br>")
            processed_content = "  \n".join(processed.splitlines()).replace("  \n  \n", "  \n")
            processed_content = processed_content.replace("  \n", "  \n  \n")
            result_content = f"---\n[思考]\n<think>{reason_content}</think>\n\n---\n\n{processed_content}\n\n"
            with open(result_path, "a", encoding="utf-8") as result_file:
                result_file.write(f"{result_content}" + "▲▽△▼" * 15 + "\n\n")
            self.logger.info(f"✅ 第{str(range_number)}组API写入成功。")
            progress = min((i + chunk_size) / len(lines) * 100, 100)
            print(f"\r▷ 处理进度: {progress:.1f}%", end="", flush=True)
        self.extract_optimized_text(result_path)
        self.logger.info("✅ 处理结束。")


if __name__ == "__main__":
    try:
        if not (Path("config") / "api_key.txt").exists():
            print("首次使用配置指南：")
            api_key = input("请输入DeepSeek API密钥: ").strip()
            with open(Path("config") / "api_key.txt", "w") as f:
                f.write(api_key)
            print("密钥已安全存储")
        else:
            print("API密钥已存在，脚本程序启动！")
        NovelEditorSystem().run()
    except Exception as error_exception:
        print(f"\n❌ 处理过程中发生未知错误: {error_exception}")
