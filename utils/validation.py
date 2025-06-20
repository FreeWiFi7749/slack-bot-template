"""
バリデーション関数

入力値の検証とサニタイゼーション機能を提供します。
"""
import re
from typing import Any, List, Optional, Union
import html

def validate_slack_token(token: str, token_type: str = "bot") -> bool:
    """
    Slackトークンの形式を検証します。
    
    Args:
        token (str): 検証するトークン
        token_type (str): トークンの種類（bot, app, user）
        
    Returns:
        bool: トークンが有効な形式の場合True
    """
    if not token or not isinstance(token, str):
        return False
    
    patterns = {
        "bot": r"^xoxb-[0-9]+-[0-9]+-[a-zA-Z0-9]+$",
        "app": r"^xapp-[0-9]+-[A-Z0-9]+-[a-zA-Z0-9]+$",
        "user": r"^xoxp-[0-9]+-[0-9]+-[0-9]+-[a-zA-Z0-9]+$"
    }
    
    pattern = patterns.get(token_type)
    if not pattern:
        return False
    
    return bool(re.match(pattern, token))

def sanitize_input(input_text: str, max_length: int = 1000) -> str:
    """
    ユーザー入力をサニタイズします。
    
    Args:
        input_text (str): サニタイズする文字列
        max_length (int): 最大文字数
        
    Returns:
        str: サニタイズされた文字列
    """
    if not isinstance(input_text, str):
        return ""
    
    # HTMLエスケープ
    sanitized = html.escape(input_text)
    
    # 最大長を制限
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    # 危険な文字列パターンを除去
    dangerous_patterns = [
        r'<script[^>]*>.*?</script>',
        r'javascript:',
        r'vbscript:',
        r'on\w+\s*=',
    ]
    
    for pattern in dangerous_patterns:
        sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE | re.DOTALL)
    
    return sanitized.strip()

def validate_user_id(user_id: str) -> bool:
    """
    SlackユーザーIDの形式を検証します。
    
    Args:
        user_id (str): 検証するユーザーID
        
    Returns:
        bool: 有効な形式の場合True
    """
    if not user_id or not isinstance(user_id, str):
        return False
    
    # SlackユーザーIDの形式: U + 8-11桁の英数字
    pattern = r"^U[A-Z0-9]{8,11}$"
    return bool(re.match(pattern, user_id))

def validate_channel_id(channel_id: str) -> bool:
    """
    SlackチャンネルIDの形式を検証します。
    
    Args:
        channel_id (str): 検証するチャンネルID
        
    Returns:
        bool: 有効な形式の場合True
    """
    if not channel_id or not isinstance(channel_id, str):
        return False
    
    # SlackチャンネルIDの形式: C + 8-11桁の英数字
    pattern = r"^C[A-Z0-9]{8,11}$"
    return bool(re.match(pattern, channel_id))

def validate_command_name(command_name: str) -> bool:
    """
    コマンド名の形式を検証します。
    
    Args:
        command_name (str): 検証するコマンド名
        
    Returns:
        bool: 有効な形式の場合True
    """
    if not command_name or not isinstance(command_name, str):
        return False
    
    # コマンド名: 英数字、ハイフン、アンダースコアのみ、3-32文字
    pattern = r"^[a-zA-Z0-9_-]{3,32}$"
    return bool(re.match(pattern, command_name))

def validate_email(email: str) -> bool:
    """
    メールアドレスの形式を検証します。
    
    Args:
        email (str): 検証するメールアドレス
        
    Returns:
        bool: 有効な形式の場合True
    """
    if not email or not isinstance(email, str):
        return False
    
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))

def validate_url(url: str, allowed_schemes: Optional[List[str]] = None) -> bool:
    """
    URLの形式を検証します。
    
    Args:
        url (str): 検証するURL
        allowed_schemes (Optional[List[str]]): 許可するスキーム一覧
        
    Returns:
        bool: 有効な形式の場合True
    """
    if not url or not isinstance(url, str):
        return False
    
    if allowed_schemes is None:
        allowed_schemes = ["http", "https"]
    
    # 基本的なURL形式をチェック
    pattern = r"^https?://[^\s/$.?#].[^\s]*$"
    if not re.match(pattern, url):
        return False
    
    # スキームをチェック
    scheme = url.split("://")[0].lower()
    return scheme in allowed_schemes

def validate_numeric_range(
    value: Union[int, float], 
    min_value: Optional[Union[int, float]] = None,
    max_value: Optional[Union[int, float]] = None
) -> bool:
    """
    数値が指定された範囲内にあるかを検証します。
    
    Args:
        value (Union[int, float]): 検証する数値
        min_value (Optional[Union[int, float]]): 最小値
        max_value (Optional[Union[int, float]]): 最大値
        
    Returns:
        bool: 範囲内の場合True
    """
    if not isinstance(value, (int, float)):
        return False
    
    if min_value is not None and value < min_value:
        return False
    
    if max_value is not None and value > max_value:
        return False
    
    return True

def validate_string_length(
    text: str, 
    min_length: int = 0, 
    max_length: int = 1000
) -> bool:
    """
    文字列の長さを検証します。
    
    Args:
        text (str): 検証する文字列
        min_length (int): 最小文字数
        max_length (int): 最大文字数
        
    Returns:
        bool: 有効な長さの場合True
    """
    if not isinstance(text, str):
        return False
    
    length = len(text)
    return min_length <= length <= max_length

def is_safe_filename(filename: str) -> bool:
    """
    ファイル名が安全かを検証します。
    
    Args:
        filename (str): 検証するファイル名
        
    Returns:
        bool: 安全なファイル名の場合True
    """
    if not filename or not isinstance(filename, str):
        return False
    
    # 危険な文字をチェック
    dangerous_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    if any(char in filename for char in dangerous_chars):
        return False
    
    # システムファイル名をチェック
    forbidden_names = [
        'CON', 'PRN', 'AUX', 'NUL',
        'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
        'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
    ]
    
    name_without_extension = filename.split('.')[0].upper()
    if name_without_extension in forbidden_names:
        return False
    
    # 長さをチェック
    if len(filename) > 255:
        return False
    
    return True

def validate_json_structure(data: Any, required_keys: List[str]) -> bool:
    """
    JSON構造に必要なキーが含まれているかを検証します。
    
    Args:
        data (Any): 検証するデータ
        required_keys (List[str]): 必須キーの一覧
        
    Returns:
        bool: 必要なキーが全て含まれている場合True
    """
    if not isinstance(data, dict):
        return False
    
    return all(key in data for key in required_keys)

def validate_permission_level(permission: str) -> bool:
    """
    権限レベルが有効かを検証します。
    
    Args:
        permission (str): 検証する権限レベル
        
    Returns:
        bool: 有効な権限レベルの場合True
    """
    valid_permissions = [
        "admin",
        "moderator", 
        "user",
        "guest",
        "readonly"
    ]
    
    return permission.lower() in valid_permissions

class ValidationError(Exception):
    """バリデーションエラーを表すカスタム例外"""
    
    def __init__(self, message: str, field: str = None):
        """
        バリデーションエラーを初期化します。
        
        Args:
            message (str): エラーメッセージ
            field (str): エラーが発生したフィールド名
        """
        super().__init__(message)
        self.field = field
        self.message = message

def validate_required_fields(data: dict, required_fields: List[str]) -> None:
    """
    必須フィールドが存在することを検証します。
    
    Args:
        data (dict): 検証するデータ
        required_fields (List[str]): 必須フィールドの一覧
        
    Raises:
        ValidationError: 必須フィールドが不足している場合
    """
    missing_fields = []
    
    for field in required_fields:
        if field not in data or data[field] is None or data[field] == "":
            missing_fields.append(field)
    
    if missing_fields:
        raise ValidationError(
            f"必須フィールドが不足しています: {', '.join(missing_fields)}",
            field="required_fields"
        )

def clean_and_validate_text(
    text: str,
    min_length: int = 1,
    max_length: int = 1000,
    allow_empty: bool = False
) -> str:
    """
    テキストをクリーニングして検証します。
    
    Args:
        text (str): クリーニングする文字列
        min_length (int): 最小文字数
        max_length (int): 最大文字数
        allow_empty (bool): 空文字を許可するか
        
    Returns:
        str: クリーニングされた文字列
        
    Raises:
        ValidationError: バリデーションに失敗した場合
    """
    if not isinstance(text, str):
        raise ValidationError("テキストは文字列である必要があります")
    
    # クリーニング
    cleaned = sanitize_input(text.strip(), max_length)
    
    # 長さの検証
    if not allow_empty and len(cleaned) == 0:
        raise ValidationError("テキストは空にできません")
    
    if len(cleaned) < min_length:
        raise ValidationError(f"テキストは{min_length}文字以上である必要があります")
    
    if len(cleaned) > max_length:
        raise ValidationError(f"テキストは{max_length}文字以下である必要があります")
    
    return cleaned
