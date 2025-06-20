"""
ログユーティリティ

構造化ログとログ管理機能を提供します。
"""
import logging
import json
from datetime import datetime
from typing import Any, Dict, Optional
from pathlib import Path

def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    enable_json_logging: bool = False
) -> logging.Logger:
    """
    ログシステムを設定します。
    
    Args:
        log_level (str): ログレベル
        log_file (Optional[str]): ログファイルのパス
        enable_json_logging (bool): JSON形式でのログ出力を有効にするか
        
    Returns:
        logging.Logger: 設定されたロガー
    """
    # ログレベルを設定
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # ロガーを取得
    logger = logging.getLogger("slackbot")
    logger.setLevel(numeric_level)
    
    # 既存のハンドラーをクリア
    logger.handlers.clear()
    
    # フォーマッターを作成
    if enable_json_logging:
        formatter = JsonFormatter()
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    # コンソールハンドラーを追加
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # ファイルハンドラーを追加（指定された場合）
    if log_file:
        # ログディレクトリを作成
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

class JsonFormatter(logging.Formatter):
    """JSON形式でログを出力するフォーマッター"""
    
    def format(self, record: logging.LogRecord) -> str:
        """
        ログレコードをJSON形式にフォーマットします。
        
        Args:
            record (logging.LogRecord): ログレコード
            
        Returns:
            str: JSON形式のログメッセージ
        """
        log_data = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # 例外情報があれば追加
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        # 追加のコンテキストがあれば追加
        if hasattr(record, 'extra_data'):
            log_data['extra'] = record.extra_data
        
        return json.dumps(log_data, ensure_ascii=False)

def log_command_usage(
    command_name: str,
    user_id: str,
    channel_id: str,
    args: Optional[Dict[str, Any]] = None,
    execution_time: Optional[float] = None,
    success: bool = True,
    error: Optional[str] = None
) -> None:
    """
    コマンドの使用状況をログに記録します。
    
    Args:
        command_name (str): コマンド名
        user_id (str): ユーザーID
        channel_id (str): チャンネルID
        args (Optional[Dict[str, Any]]): コマンド引数
        execution_time (Optional[float]): 実行時間（秒）
        success (bool): 実行が成功したか
        error (Optional[str]): エラーメッセージ（失敗時）
    """
    logger = logging.getLogger("slackbot.commands")
    
    log_data = {
        'command': command_name,
        'user_id': user_id,
        'channel_id': channel_id,
        'success': success,
        'timestamp': datetime.now().isoformat()
    }
    
    if args:
        log_data['args'] = args
    
    if execution_time is not None:
        log_data['execution_time'] = execution_time
    
    if error:
        log_data['error'] = error
    
    # LogRecordに追加データを設定
    extra = {'extra_data': log_data}
    
    if success:
        logger.info(f"コマンド実行成功: {command_name}", extra=extra)
    else:
        logger.error(f"コマンド実行失敗: {command_name} - {error}", extra=extra)

def log_cog_event(
    event_type: str,
    cog_name: str,
    details: Optional[Dict[str, Any]] = None,
    success: bool = True,
    error: Optional[str] = None
) -> None:
    """
    Cogのイベント（ロード、アンロード、リロードなど）をログに記録します。
    
    Args:
        event_type (str): イベントタイプ（load, unload, reload, error）
        cog_name (str): Cog名
        details (Optional[Dict[str, Any]]): 追加の詳細情報
        success (bool): イベントが成功したか
        error (Optional[str]): エラーメッセージ（失敗時）
    """
    logger = logging.getLogger("slackbot.cogs")
    
    log_data = {
        'event_type': event_type,
        'cog_name': cog_name,
        'success': success,
        'timestamp': datetime.now().isoformat()
    }
    
    if details:
        log_data['details'] = details
    
    if error:
        log_data['error'] = error
    
    extra = {'extra_data': log_data}
    
    if success:
        logger.info(f"Cogイベント: {event_type} - {cog_name}", extra=extra)
    else:
        logger.error(f"Cogイベント失敗: {event_type} - {cog_name} - {error}", extra=extra)

def log_security_event(
    event_type: str,
    user_id: str,
    details: Optional[Dict[str, Any]] = None,
    severity: str = "WARNING"
) -> None:
    """
    セキュリティ関連のイベントをログに記録します。
    
    Args:
        event_type (str): イベントタイプ（unauthorized_access, rate_limit_exceeded, etc.）
        user_id (str): ユーザーID
        details (Optional[Dict[str, Any]]): 追加の詳細情報
        severity (str): 重要度レベル
    """
    logger = logging.getLogger("slackbot.security")
    
    log_data = {
        'event_type': event_type,
        'user_id': user_id,
        'severity': severity,
        'timestamp': datetime.now().isoformat()
    }
    
    if details:
        log_data['details'] = details
    
    extra = {'extra_data': log_data}
    
    if severity == "CRITICAL":
        logger.critical(f"セキュリティイベント: {event_type} - {user_id}", extra=extra)
    elif severity == "ERROR":
        logger.error(f"セキュリティイベント: {event_type} - {user_id}", extra=extra)
    else:
        logger.warning(f"セキュリティイベント: {event_type} - {user_id}", extra=extra)

class ContextFilter(logging.Filter):
    """ログにコンテキスト情報を追加するフィルター"""
    
    def __init__(self, context_data: Dict[str, Any]):
        """
        コンテキストフィルターを初期化します。
        
        Args:
            context_data (Dict[str, Any]): 追加するコンテキストデータ
        """
        super().__init__()
        self.context_data = context_data
    
    def filter(self, record: logging.LogRecord) -> bool:
        """
        ログレコードにコンテキスト情報を追加します。
        
        Args:
            record (logging.LogRecord): ログレコード
            
        Returns:
            bool: フィルターを通すかどうか
        """
        for key, value in self.context_data.items():
            setattr(record, key, value)
        return True

def create_logger_with_context(
    name: str,
    context: Dict[str, Any]
) -> logging.Logger:
    """
    コンテキスト情報を含むロガーを作成します。
    
    Args:
        name (str): ロガー名
        context (Dict[str, Any]): コンテキスト情報
        
    Returns:
        logging.Logger: コンテキスト付きロガー
    """
    logger = logging.getLogger(name)
    context_filter = ContextFilter(context)
    logger.addFilter(context_filter)
    return logger

def get_log_stats(log_file: str) -> Dict[str, Any]:
    """
    ログファイルの統計情報を取得します。
    
    Args:
        log_file (str): ログファイルのパス
        
    Returns:
        Dict[str, Any]: ログファイルの統計情報
    """
    log_path = Path(log_file)
    
    if not log_path.exists():
        return {
            'exists': False,
            'size': 0,
            'line_count': 0
        }
    
    with open(log_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    return {
        'exists': True,
        'size': log_path.stat().st_size,
        'line_count': len(lines),
        'last_modified': datetime.fromtimestamp(log_path.stat().st_mtime).isoformat()
    }
