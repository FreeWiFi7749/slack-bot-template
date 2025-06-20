"""
設定管理
"""
import os
from typing import Optional
from dotenv import load_dotenv

# .envファイルを読み込み
load_dotenv()

class Config:
    """アプリケーション設定クラス"""
    
    def __init__(self):
        """設定を初期化します"""
        # Slack認証情報
        self.SLACK_BOT_TOKEN: str = self._get_env_var("SLACK_BOT_TOKEN")
        self.SLACK_SIGNING_SECRET: str = self._get_env_var("SLACK_SIGNING_SECRET")
        self.SLACK_APP_TOKEN: str = self._get_env_var("SLACK_APP_TOKEN")
        
        # 開発設定
        self.ENABLE_HOT_RELOAD: bool = self._get_env_var("ENABLE_HOT_RELOAD", "false").lower() == "true"
        self.DEBUG_MODE: bool = self._get_env_var("DEBUG_MODE", "false").lower() == "true"
        
        # ログ設定
        self.LOG_LEVEL: str = self._get_env_var("LOG_LEVEL", "INFO").upper()
        self.LOG_FILE: Optional[str] = self._get_env_var("LOG_FILE", None)
        
        # データベース設定（将来使用）
        self.DATABASE_URL: Optional[str] = self._get_env_var("DATABASE_URL", None)
        
        # その他設定
        self.PORT: int = int(self._get_env_var("PORT", "3000"))
        self.HOST: str = self._get_env_var("HOST", "localhost")
    
    def _get_env_var(self, key: str, default: Optional[str] = None) -> str:
        """環境変数を取得します
        
        Args:
            key (str): 環境変数のキー
            default (Optional[str]): デフォルト値
            
        Returns:
            str: 環境変数の値
            
        Raises:
            ValueError: 必須の環境変数が設定されていない場合
        """
        value = os.getenv(key, default)
        if value is None and default is None:
            raise ValueError(f"環境変数 {key} が設定されていません")
        return value or ""
    
    def validate(self) -> bool:
        """設定の妥当性を検証します
        
        Returns:
            bool: 設定が有効な場合True
        """
        required_vars = [
            "SLACK_BOT_TOKEN",
            "SLACK_SIGNING_SECRET", 
            "SLACK_APP_TOKEN"
        ]
        
        for var in required_vars:
            if not getattr(self, var):
                print(f"❌ 必須設定 {var} が設定されていません")
                return False
        
        print("✅ 設定の検証が完了しました")
        return True
