"""
ヘルパー関数

よく使用される便利な関数を提供します。
"""
from datetime import datetime
from typing import Any, Dict, Optional
import re

def format_time(dt: datetime, format_type: str = "default") -> str:
    """
    日時を指定された形式でフォーマットします。
    
    Args:
        dt (datetime): フォーマットする日時
        format_type (str): フォーマットの種類
            - "default": YYYY年MM月DD日 HH:MM:SS
            - "short": MM/DD HH:MM
            - "date_only": YYYY年MM月DD日
            - "time_only": HH:MM:SS
            
    Returns:
        str: フォーマットされた日時文字列
    """
    formats = {
        "default": "%Y年%m月%d日 %H:%M:%S",
        "short": "%m/%d %H:%M",
        "date_only": "%Y年%m月%d日",
        "time_only": "%H:%M:%S"
    }
    
    format_str = formats.get(format_type, formats["default"])
    return dt.strftime(format_str)

def safe_get_user(user_data: Dict[str, Any], key: str, default: Any = "不明") -> Any:
    """
    ユーザーデータから安全に値を取得します。
    
    Args:
        user_data (Dict[str, Any]): ユーザーデータ
        key (str): 取得するキー
        default (Any): デフォルト値
        
    Returns:
        Any: 取得された値またはデフォルト値
    """
    return user_data.get(key, default)

def create_embed_message(
    title: str,
    description: str = "",
    color: str = "good",
    fields: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Slackの添付メッセージ（リッチメッセージ）を作成します。
    
    Args:
        title (str): メッセージのタイトル
        description (str): メッセージの説明
        color (str): メッセージの色（good, warning, danger）
        fields (Optional[Dict[str, str]]): 追加フィールド
        
    Returns:
        Dict[str, Any]: Slack添付メッセージの辞書
    """
    attachment = {
        "color": color,
        "title": title,
        "text": description,
        "fields": []
    }
    
    if fields:
        for field_title, field_value in fields.items():
            attachment["fields"].append({
                "title": field_title,
                "value": field_value,
                "short": True
            })
    
    return attachment

def calculate_uptime(start_time: datetime) -> Dict[str, int]:
    """
    稼働時間を計算します。
    
    Args:
        start_time (datetime): 開始時刻
        
    Returns:
        Dict[str, int]: 日、時、分、秒の辞書
    """
    uptime_delta = datetime.now() - start_time
    
    days = uptime_delta.days
    hours, remainder = divmod(uptime_delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    return {
        "days": days,
        "hours": hours,
        "minutes": minutes,
        "seconds": seconds
    }

def format_uptime(uptime_dict: Dict[str, int]) -> str:
    """
    稼働時間を読みやすい文字列にフォーマットします。
    
    Args:
        uptime_dict (Dict[str, int]): calculate_uptime()の結果
        
    Returns:
        str: フォーマットされた稼働時間
    """
    parts = []
    
    if uptime_dict["days"] > 0:
        parts.append(f"{uptime_dict['days']}日")
    if uptime_dict["hours"] > 0:
        parts.append(f"{uptime_dict['hours']}時間")
    if uptime_dict["minutes"] > 0:
        parts.append(f"{uptime_dict['minutes']}分")
    if uptime_dict["seconds"] > 0 or not parts:
        parts.append(f"{uptime_dict['seconds']}秒")
    
    return " ".join(parts)

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    テキストを指定された長さで切り詰めます。
    
    Args:
        text (str): 切り詰めるテキスト
        max_length (int): 最大文字数
        suffix (str): 切り詰め時に追加する文字列
        
    Returns:
        str: 切り詰められたテキスト
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix

def parse_mention(text: str) -> Optional[str]:
    """
    Slackのメンション文字列からユーザーIDを抽出します。
    
    Args:
        text (str): メンション文字列（例: <@U123456789>）
        
    Returns:
        Optional[str]: ユーザーID、見つからない場合はNone
    """
    match = re.search(r'<@([A-Z0-9]+)>', text)
    return match.group(1) if match else None

def generate_progress_bar(
    current: int, 
    total: int, 
    width: int = 20, 
    fill_char: str = "█", 
    empty_char: str = "░"
) -> str:
    """
    プログレスバーを生成します。
    
    Args:
        current (int): 現在の値
        total (int): 最大値
        width (int): バーの幅
        fill_char (str): 埋める文字
        empty_char (str): 空の文字
        
    Returns:
        str: プログレスバーの文字列
    """
    if total == 0:
        percentage = 0
    else:
        percentage = min(current / total, 1.0)
    
    filled_width = int(width * percentage)
    empty_width = width - filled_width
    
    bar = fill_char * filled_width + empty_char * empty_width
    return f"{bar} {current}/{total} ({percentage:.1%})"

def chunk_list(lst: list, chunk_size: int) -> list:
    """
    リストを指定されたサイズのチャンクに分割します。
    
    Args:
        lst (list): 分割するリスト
        chunk_size (int): チャンクのサイズ
        
    Returns:
        list: チャンクのリスト
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

def format_file_size(size_bytes: int) -> str:
    """
    ファイルサイズを人間が読みやすい形式にフォーマットします。
    
    Args:
        size_bytes (int): バイト数
        
    Returns:
        str: フォーマットされたファイルサイズ
    """
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    
    while size_bytes >= 1024.0 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"
