"""
SlackCogs使用ボット
"""
import asyncio
import logging
import sys

from slackcogs import SlackCogsApp
from config import Config

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class MySlackBot:
    def __init__(self):
        self.config = Config()
        
        # SlackCogsアプリ作成
        self.app = SlackCogsApp(
            token=self.config.SLACK_BOT_TOKEN,
            signing_secret=self.config.SLACK_SIGNING_SECRET,
            app_token=self.config.SLACK_APP_TOKEN
        )
    
    async def start(self):
        """ボット開始"""
        try:
            logger.info("🚀 Starting SlackBot...")
            
            # Cogを自動読み込み
            await self.app.load_cogs_from_directory("cogs")
            
            # ホットリロード有効化（開発環境のみ）
            if self.config.ENABLE_HOT_RELOAD:
                await self.app.enable_hot_reload("cogs")
                logger.info("🔥 Hot reload enabled")
            
            # ボット開始
            logger.info("✅ Bot is ready!")
            await self.app.start()
            
        except Exception as e:
            logger.error(f"❌ Failed to start bot: {e}")
            sys.exit(1)

async def main():
    bot = MySlackBot()
    try:
        await bot.start()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
