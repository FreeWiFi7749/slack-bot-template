"""
サンプルCog

カスタム機能の実装例を提供します。
新しいCogを作成する際の参考にしてください。
"""
from typing import Any, Dict
import random
from datetime import datetime

# TODO: SlackCogsフレームワークが実装されたら以下のimportを有効化
# from slackcogs import BaseCog, slash_command, SlackContext, rate_limit

class ExampleCog:
    """サンプル機能を提供するCog"""
    
    def __init__(self, app: Any):
        """
        ExampleCogを初期化します。
        
        Args:
            app: SlackCogsアプリケーションインスタンス
        """
        self.app = app
        self.counter = 0
        self.user_data: Dict[str, Any] = {}
        self.quotes = [
            "継続は力なり",
            "七転び八起き",
            "塵も積もれば山となる",
            "千里の道も一歩から",
            "努力に勝る天才なし"
        ]
    
    # TODO: SlackCogsフレームワーク実装後に有効化
    # @slash_command()
    async def hello(self, ctx: Any, name: str = None) -> None:
        """
        挨拶コマンド - ユーザーに挨拶します。
        
        Args:
            ctx: Slackコンテキスト
            name: 挨拶する相手の名前（オプション）
        """
        if name:
            message = f"こんにちは、{name}さん！👋"
        else:
            message = "こんにちは！👋"
        
        await ctx.respond(message)
    
    # @slash_command()
    # @rate_limit(max_requests=5, time_window=60)
    async def count(self, ctx: Any) -> None:
        """
        カウンターコマンド - カウンターを増加させて表示します。
        
        Args:
            ctx: Slackコンテキスト
        """
        self.counter += 1
        await ctx.respond(f"🔢 カウンター: {self.counter}")
    
    # @slash_command()
    async def quote(self, ctx: Any) -> None:
        """
        名言コマンド - ランダムな名言を表示します。
        
        Args:
            ctx: Slackコンテキスト
        """
        quote = random.choice(self.quotes)
        await ctx.respond(f"💭 **今日の名言**\n\n*{quote}*")
    
    # @slash_command()
    async def time(self, ctx: Any) -> None:
        """
        時刻コマンド - 現在の時刻を表示します。
        
        Args:
            ctx: Slackコンテキスト
        """
        current_time = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
        await ctx.respond(f"🕐 現在の時刻: {current_time}")
    
    # @slash_command()
    async def user_info(self, ctx: Any, action: str = "show") -> None:
        """
        ユーザー情報コマンド - ユーザー情報の表示・設定を行います。
        
        Args:
            ctx: Slackコンテキスト
            action: 実行するアクション（show/reset）
        """
        user_id = ctx.user.id  # TODO: 実際のuser_id取得方法に修正
        
        if action == "show":
            if user_id in self.user_data:
                data = self.user_data[user_id]
                message = f"""
👤 **ユーザー情報**

🆔 ID: {user_id}
📅 初回登録: {data.get('first_seen', '不明')}
🔢 コマンド実行回数: {data.get('command_count', 0)}
                """
            else:
                message = "👤 ユーザー情報が見つかりませんでした。"
            
        elif action == "reset":
            if user_id in self.user_data:
                del self.user_data[user_id]
                message = "✅ ユーザー情報をリセットしました。"
            else:
                message = "❌ リセットするユーザー情報が見つかりませんでした。"
        
        else:
            message = "❌ 無効なアクションです。利用可能: show, reset"
        
        await ctx.respond(message)
    
    # @slash_command()
    async def example_help(self, ctx: Any) -> None:
        """
        サンプルコマンドのヘルプを表示します。
        
        Args:
            ctx: Slackコンテキスト
        """
        help_text = """
🎯 **サンプルコマンド**

👋 `/hello [名前]` - 挨拶をします
🔢 `/count` - カウンターを増加
💭 `/quote` - ランダムな名言を表示
🕐 `/time` - 現在の時刻を表示
👤 `/user_info [show/reset]` - ユーザー情報の表示・リセット
❓ `/example_help` - このヘルプを表示

これらは実装例です。実際の使用時は適宜カスタマイズしてください。
        """
        await ctx.respond(help_text)
    
    def _track_user(self, user_id: str) -> None:
        """
        ユーザーの活動を記録します。
        
        Args:
            user_id: ユーザーID
        """
        if user_id not in self.user_data:
            self.user_data[user_id] = {
                'first_seen': datetime.now().isoformat(),
                'command_count': 0
            }
        
        self.user_data[user_id]['command_count'] += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Cogの統計情報を取得します。
        
        Returns:
            Dict[str, Any]: 統計情報
        """
        return {
            'counter': self.counter,
            'total_users': len(self.user_data),
            'total_commands': sum(data.get('command_count', 0) for data in self.user_data.values())
        }
