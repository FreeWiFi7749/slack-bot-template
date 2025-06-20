"""
基本コマンドCog

ping, help, statusなどの基本的なコマンドを提供します。
"""
from datetime import datetime
from typing import Any

# TODO: SlackCogsフレームワークが実装されたら以下のimportを有効化
# from slackcogs import BaseCog, slash_command, SlackContext

class GeneralCog:
    """基本コマンドを管理するCog"""
    
    def __init__(self, app: Any):
        """
        GeneralCogを初期化します。
        
        Args:
            app: SlackCogsアプリケーションインスタンス
        """
        self.app = app
        self.start_time = datetime.now()
        self.command_count = 0
    
    # TODO: SlackCogsフレームワーク実装後に有効化
    # @slash_command()
    async def ping(self, ctx: Any) -> None:
        """
        Pingコマンド - ボットの応答性をテストします。
        
        Args:
            ctx: Slackコンテキスト
        """
        self.command_count += 1
        await ctx.respond("🏓 ポン！ボットは正常に動作しています。")
    
    # @slash_command()
    async def help(self, ctx: Any) -> None:
        """
        ヘルプコマンド - 利用可能なコマンドの一覧を表示します。
        
        Args:
            ctx: Slackコンテキスト
        """
        help_text = """
📚 **利用可能なコマンド**

🔹 `/ping` - ボットの応答テスト
🔹 `/help` - このヘルプメッセージを表示
🔹 `/status` - ボットのステータス情報を表示

管理者コマンドについては `/admin help` をご確認ください。
        """
        await ctx.respond(help_text)
    
    # @slash_command()
    async def status(self, ctx: Any) -> None:
        """
        ステータスコマンド - ボットの動作状況を表示します。
        
        Args:
            ctx: Slackコンテキスト
        """
        uptime = datetime.now() - self.start_time
        status_text = f"""
📊 **ボットステータス**

🟢 **状態**: 正常稼働中
⏰ **稼働時間**: {uptime.days}日 {uptime.seconds // 3600}時間 {(uptime.seconds % 3600) // 60}分
📈 **実行コマンド数**: {self.command_count}
🔧 **バージョン**: 1.0.0
        """
        await ctx.respond(status_text)
    
    def get_uptime(self) -> str:
        """
        稼働時間を文字列で取得します。
        
        Returns:
            str: 稼働時間の文字列表現
        """
        uptime = datetime.now() - self.start_time
        return f"{uptime.days}日 {uptime.seconds // 3600}時間 {(uptime.seconds % 3600) // 60}分"
