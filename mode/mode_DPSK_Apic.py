import logging
import os

import openai
from openai import OpenAI


class APIClientError(Exception):
    pass


class APIConnectionError(APIClientError):
    pass


class AuthenticationError(APIClientError):
    pass


class ClassDeepSeekHand:
    """独立的API处理模块"""

    def __init__(self, logger=None):
        self.client = None
        self.logger = logger or logging.getLogger("DeepSeekHand")
        self._init_client()
        self.api_key = self._load_api_key()

    def _init_client(self):
        """初始化API客户端"""
        try:
            key_api = self._load_api_key()
            link_base = "https://api.deepseek.com"
            self.client = OpenAI(
                    api_key=key_api,
                    base_url=link_base
                    )
            self._verify_connection()
        except Exception as e:
            raise RuntimeError(f"API初始化失败: {str(e)}")

    def _load_api_key(self):
        """加载API密钥"""
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            key_path = os.path.join("config", "api_key.txt")
            try:
                with open(key_path, "r") as f:
                    api_key = f.read().strip()
                    if not api_key:
                        raise ValueError("API密钥文件为空")
                    self.logger.info("成功加载API密钥")  # 使用外部传入的日志记录器
            except FileNotFoundError as f:
                self.logger.error(f"加载API密钥失败: {str(f)}", exc_info=True)
                raise RuntimeError(f"API密钥文件未找到：{key_path}")
            except Exception as e:
                self.logger.error(f"加载API密钥失败: {str(e)}", exc_info=True)
                raise RuntimeError(f"无法加载API密钥，请检查配置文件。")
        return api_key

    def close_logger(self):
        """关闭日志处理器"""
        for handler in self.logger.handlers[:]:
            handler.close()
            self.logger.removeHandler(handler)

    def _verify_connection(self):
        try:
            self.client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[{"role": "system", "content": "connection test"}],
                    max_tokens=1
                    )
        except openai.AuthenticationError as e:
            raise AuthenticationError(f"API认证失败: {str(e)}")
        except openai.APIConnectionError as e:
            raise APIConnectionError(f"API连接失败: {str(e)}")
        except Exception as e:
            raise APIClientError(f"未知错误: {str(e)}")

    def process_request(self, system_prompt, user_content):
        try:
            self.logger.info("正在发送请求到DeepSeek API")  # 使用外部传入的日志记录器
            response = self.client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_content}
                        ],
                    temperature=0.7,
                    max_tokens=2000,
                    stream=False
                    )
            if not response.choices or not hasattr(response.choices[0], "message"):
                raise ValueError("API返回的数据结构不符合预期")
            self.logger.info("API请求成功，返回数据已处理")
            self.logger.info(f"成功处理 {len(user_content)} 字符的请求")
            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f"请求处理失败: {str(e)}")
            raise
