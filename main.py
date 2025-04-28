#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
from datetime import datetime

from mode.mode_DPSK_Apic import ClassDeepSeekHand


class NovelEditorSystem:
    """主业务逻辑模块"""

    def __init__(self):
        self.logger = None
        self._init_logger()  # 初始化系统日志
        self.api_handler = ClassDeepSeekHand(logger=self.logger)  # 传递日志记录器
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self._init_directories()
        self.task_profiles = {
            1: self._load_task_profile("文段理解处理", "text_PUP_Tas.md", 60)
            }

    def _init_logger(self):
        """初始化系统日志"""
        self.logger = logging.getLogger("NovelEditorSystem")
        self.logger.setLevel(logging.INFO)

        log_dir = os.path.join(self.base_dir, "logs")
        os.makedirs(log_dir, exist_ok=True)

        # 生成符合格式的日志文件名
        timestamp = datetime.now().strftime("%m%d_%H%M")
        log_filename = f"logs_{timestamp}.log"

        formatter = logging.Formatter(
                '[%(asctime)s] %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
                )

        file_handler = logging.FileHandler(
                filename=os.path.join(log_dir, log_filename),
                encoding="utf-8"
                )
        file_handler.setFormatter(formatter)

        if not any(isinstance(h, logging.FileHandler) for h in self.logger.handlers):
            self.logger.addHandler(file_handler)

    def _init_directories(self):
        """初始化目录结构"""
        required_dirs = {
            "config": "API配置目录",
            "text": "系统提示目录",
            "data": "输入数据目录",
            "results": "处理结果目录",
            "logs": "系统日志目录"
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
            "prompt_path": os.path.join(self.base_dir, "text", prompt_file),
            "chunk_size": chunk_size
            }

    @staticmethod
    def _show_menu():
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
            self.logger.info("主程序启动，显示交互菜单")
            self._show_menu()
            choice = input("请选择操作编号: ").strip()
            self.logger.info(f"用户输入: {choice}选项，开始执行。")

            if choice == "0":
                print("\n系统已安全退出")
                self.logger.info("用户自行退出程序。")
                break
            if choice == "1":
                self._execute_processing_task()
                self.logger.info("文段理解处理模式已开启")
            else:
                print("无效的选项，请重新输入")
                self.logger.warnning("用户输入无效选项，提示重新输入。")

    def _execute_processing_task(self):
        """执行处理任务"""
        logging.info("正在启动文段理解处理模式...")

        try:
            if len(self.task_profiles) <= 1 or "prompt_path" not in self.task_profiles[1]:
                print("\n❌ 配置文件中缺少有效的提示文件路径")
                return

            prompt_path = self.task_profiles[1].get("prompt_path")
            if not os.path.isfile(prompt_path):
                print(f"\n❌ 提示文件路径无效或文件不存在: {prompt_path}")
                return

            try:
                with open(prompt_path, "r", encoding="utf-8") as objt_file:
                    system_prompt = objt_file.read()
            except IOError as exception_IOError:
                print(f"\n❌ 无法读取提示文件: {exception_IOError}")
                return

            # 加载用户内容
            try:
                content = self._load_user_content()
                if not content:
                    print("\n❌ 用户内容为空，无法继续处理")
                    return
            except Exception as exception_Exception:
                print(f"\n❌ 加载用户内容时发生错误: {exception_Exception}")
                return

            # 执行处理流程
            try:
                result_path = self._generate_result_path()
                if not result_path:
                    print("\n❌ 结果文件路径生成失败")
                    return
            except Exception as exception_Exception:
                print(f"\n❌ 生成结果文件路径时发生错误: {exception_Exception}")
                return

            self._process_content(content, system_prompt, result_path)

            print(f"\n✅ 处理完成！结果文件已保存至:\n{result_path}")

        except FileNotFoundError as file_not_found_exception:
            print(f"\n❌ 文件未找到: {file_not_found_exception}")
        except KeyError as key_error_exception:
            print(f"\n❌ 配置文件中缺少必要的键: {key_error_exception}")
        except Exception as exception_exception:
            print(f"\n❌ 处理过程中发生未知错误: {exception_exception}")

    @staticmethod
    def _load_user_content():
        """加载用户内容"""
        data_path = os.path.join("data", "data_MAIN_Info.md")
        try:
            with open(data_path, "r", encoding="utf-8") as objt_file:
                content = objt_file.read()
            if not content:
                raise ValueError("输入文件为空")
            # 增加基本格式验证
            if not content.strip().startswith("#"):  # 假设文件应以 Markdown 标题开头
                raise ValueError("文件格式不正确，可能缺少标题")
            return content
        except FileNotFoundError:
            raise RuntimeError(f"未找到输入文件: {data_path}")

    @staticmethod
    def _generate_result_path():
        """生成结果文件路径"""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"Result_{timestamp}.md"
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
                except ConnectionError as ce:
                    raise RuntimeError(f"网络连接失败: {str(ce)}")
                except ValueError as ve:
                    raise RuntimeError(f"API 返回无效数据: {str(ve)}")
                except Exception as exception_exception:
                    raise RuntimeError(f"未知错误: {str(exception_exception)}")

                result_file.write(f"{processed}\n\n")
                progress = min((i + chunk_size) / total_chars * 100, 100)
                print(f"\r▷ 处理进度: {progress:.1f}%", end="", flush=True)


def safe_load_file(path, error_message):
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    except IOError as exception_IOError:
        logging.error(f"{error_message}: {exception_IOError}")
        return None


def safe_call(func, *args, error_message="调用失败"):
    try:
        result = func(*args)
        if not result:
            logging.error(error_message)
        return result
    except Exception as exception_exception:
        logging.error(f"{error_message}: {exception_exception}")
        return None


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

    except FileNotFoundError as e:
        print(f"\n❌ 文件未找到: {e}")
    except KeyError as e:
        print(f"\n❌ 配置文件中缺少必要的键: {e}")
    except Exception as e:
        print(f"\n❌ 处理过程中发生未知错误: {e}")
