"""
Cogテスト

各Cogの機能をテストします。
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime

# TODO: SlackCogsフレームワーク実装後にimportを修正
from cogs.general import GeneralCog
from cogs.admin import AdminCog
from cogs.example import ExampleCog

class TestGeneralCog:
    """GeneralCogのテストクラス"""
    
    @pytest.fixture
    def general_cog(self):
        """GeneralCogのテスト用インスタンスを作成"""
        mock_app = MagicMock()
        return GeneralCog(mock_app)
    
    @pytest.fixture
    def mock_context(self):
        """モックコンテキストを作成"""
        ctx = AsyncMock()
        ctx.respond = AsyncMock()
        return ctx
    
    @pytest.mark.asyncio
    async def test_ping_command(self, general_cog, mock_context):
        """pingコマンドのテスト"""
        await general_cog.ping(mock_context)
        
        mock_context.respond.assert_called_once()
        call_args = mock_context.respond.call_args[0][0]
        assert "ポン" in call_args
        assert general_cog.command_count == 1
    
    @pytest.mark.asyncio
    async def test_help_command(self, general_cog, mock_context):
        """helpコマンドのテスト"""
        await general_cog.help(mock_context)
        
        mock_context.respond.assert_called_once()
        call_args = mock_context.respond.call_args[0][0]
        assert "利用可能なコマンド" in call_args
        assert "/ping" in call_args
    
    @pytest.mark.asyncio
    async def test_status_command(self, general_cog, mock_context):
        """statusコマンドのテスト"""
        await general_cog.status(mock_context)
        
        mock_context.respond.assert_called_once()
        call_args = mock_context.respond.call_args[0][0]
        assert "ボットステータス" in call_args
        assert "正常稼働中" in call_args
    
    def test_get_uptime(self, general_cog):
        """get_uptimeメソッドのテスト"""
        uptime = general_cog.get_uptime()
        assert isinstance(uptime, str)
        assert "日" in uptime

class TestAdminCog:
    """AdminCogのテストクラス"""
    
    @pytest.fixture
    def admin_cog(self):
        """AdminCogのテスト用インスタンスを作成"""
        mock_app = MagicMock()
        return AdminCog(mock_app)
    
    @pytest.fixture
    def mock_context(self):
        """モックコンテキストを作成"""
        ctx = AsyncMock()
        ctx.respond = AsyncMock()
        return ctx
    
    @pytest.mark.asyncio
    async def test_admin_help_command(self, admin_cog, mock_context):
        """admin_helpコマンドのテスト"""
        await admin_cog.admin_help(mock_context)
        
        mock_context.respond.assert_called_once()
        call_args = mock_context.respond.call_args[0][0]
        assert "管理者コマンド" in call_args
        assert "/reload" in call_args
    
    @pytest.mark.asyncio
    async def test_list_cogs_empty(self, admin_cog, mock_context):
        """list_cogsコマンドのテスト（空の場合）"""
        await admin_cog.list_cogs(mock_context)
        
        mock_context.respond.assert_called_once()
        call_args = mock_context.respond.call_args[0][0]
        assert "読み込まれているCogはありません" in call_args
    
    @pytest.mark.asyncio
    async def test_list_cogs_with_data(self, admin_cog, mock_context):
        """list_cogsコマンドのテスト（データあり）"""
        admin_cog.loaded_cogs = ["general", "example"]
        await admin_cog.list_cogs(mock_context)
        
        mock_context.respond.assert_called_once()
        call_args = mock_context.respond.call_args[0][0]
        assert "読み込み済みCog一覧" in call_args
        assert "general" in call_args
        assert "example" in call_args

class TestExampleCog:
    """ExampleCogのテストクラス"""
    
    @pytest.fixture
    def example_cog(self):
        """ExampleCogのテスト用インスタンスを作成"""
        mock_app = MagicMock()
        return ExampleCog(mock_app)
    
    @pytest.fixture
    def mock_context(self):
        """モックコンテキストを作成"""
        ctx = AsyncMock()
        ctx.respond = AsyncMock()
        ctx.user = MagicMock()
        ctx.user.id = "test_user_123"
        return ctx
    
    @pytest.mark.asyncio
    async def test_hello_command_no_name(self, example_cog, mock_context):
        """helloコマンドのテスト（名前なし）"""
        await example_cog.hello(mock_context)
        
        mock_context.respond.assert_called_once()
        call_args = mock_context.respond.call_args[0][0]
        assert "こんにちは" in call_args
    
    @pytest.mark.asyncio
    async def test_hello_command_with_name(self, example_cog, mock_context):
        """helloコマンドのテスト（名前あり）"""
        await example_cog.hello(mock_context, "太郎")
        
        mock_context.respond.assert_called_once()
        call_args = mock_context.respond.call_args[0][0]
        assert "太郎さん" in call_args
    
    @pytest.mark.asyncio
    async def test_count_command(self, example_cog, mock_context):
        """countコマンドのテスト"""
        initial_count = example_cog.counter
        await example_cog.count(mock_context)
        
        assert example_cog.counter == initial_count + 1
        mock_context.respond.assert_called_once()
        call_args = mock_context.respond.call_args[0][0]
        assert "カウンター" in call_args
    
    @pytest.mark.asyncio
    async def test_quote_command(self, example_cog, mock_context):
        """quoteコマンドのテスト"""
        await example_cog.quote(mock_context)
        
        mock_context.respond.assert_called_once()
        call_args = mock_context.respond.call_args[0][0]
        assert "今日の名言" in call_args
    
    @pytest.mark.asyncio
    async def test_time_command(self, example_cog, mock_context):
        """timeコマンドのテスト"""
        await example_cog.time(mock_context)
        
        mock_context.respond.assert_called_once()
        call_args = mock_context.respond.call_args[0][0]
        assert "現在の時刻" in call_args
        assert "年" in call_args
    
    def test_track_user(self, example_cog):
        """_track_userメソッドのテスト"""
        user_id = "test_user_123"
        
        # 初回記録
        example_cog._track_user(user_id)
        assert user_id in example_cog.user_data
        assert example_cog.user_data[user_id]['command_count'] == 1
        
        # 2回目記録
        example_cog._track_user(user_id)
        assert example_cog.user_data[user_id]['command_count'] == 2
    
    def test_get_stats(self, example_cog):
        """get_statsメソッドのテスト"""
        # テストデータ追加
        example_cog.counter = 5
        example_cog.user_data = {
            "user1": {"command_count": 3},
            "user2": {"command_count": 2}
        }
        
        stats = example_cog.get_stats()
        assert stats['counter'] == 5
        assert stats['total_users'] == 2
        assert stats['total_commands'] == 5

class TestCogIntegration:
    """複数Cog間の統合テスト"""
    
    @pytest.mark.asyncio
    async def test_multiple_cogs_initialization(self):
        """複数Cogの初期化テスト"""
        mock_app = MagicMock()
        
        general_cog = GeneralCog(mock_app)
        admin_cog = AdminCog(mock_app)
        example_cog = ExampleCog(mock_app)
        
        assert general_cog.app is mock_app
        assert admin_cog.app is mock_app
        assert example_cog.app is mock_app
        assert isinstance(general_cog.start_time, datetime)
        assert isinstance(admin_cog.loaded_cogs, list)
        assert isinstance(example_cog.counter, int)

# pytest設定
@pytest.fixture(scope="session")
def event_loop():
    """テスト用イベントループを作成"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

if __name__ == "__main__":
    pytest.main([__file__])
