import os
import logging

from openai import OpenAI

class ClassDeepSeekHand:
    """独立的API处理模块"""

    def __init__(self):
        self.client = None
        self.logger = None
        self._init_client()
        self._init_logger()

    def _init_client(self):
        """初始化API客户端"""
        try:
            api_key = self._load_api_key()
            self.client = OpenAI(
                api_key=api_key,
                base_url="https://api.deepseek.com"
            )
            self._verify_connection()
        except Exception as e:
            raise RuntimeError(f"API初始化失败: {str(e)}")

    @staticmethod
    def _load_api_key():
        """加载API密钥"""
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            key_path = os.path.join("config", "api_key.txt")
            try:
                with open(key_path, "r") as f:
                    api_key = f.read().strip()
            except FileNotFoundError:
                raise RuntimeError(f"API密钥文件未找到：{key_path}")
        return api_key

    def _init_logger(self):
        """初始化日志系统"""
        self.logger = logging.getLogger("DeepSeekAPI")
        self.logger.setLevel(logging.INFO)

        log_dir = os.path.join("logs", "api")
        os.makedirs(log_dir, exist_ok=True)

        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        file_handler = logging.FileHandler(
            filename=os.path.join(log_dir, "api_operations.log"),
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

    def _verify_connection(self):
        """验证API连通性"""
        try:
            self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "system", "content": "connection test"}],
                max_tokens=1
            )
        except Exception as e:
            raise RuntimeError(f"API连接测试失败: {str(e)}")

    def process_request(self, system_prompt, user_content):
        """处理API请求"""
        try:
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
            self.logger.info(f"成功处理 {len(user_content)} 字符的请求")
            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f"请求处理失败: {str(e)}")
            raise