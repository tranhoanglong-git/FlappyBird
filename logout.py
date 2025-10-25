def logout_user():
    """Đăng xuất: xoá người dùng hiện tại, reset high_score trên màn hình"""
    return {
        'current_user': None,
        'high_score': 0,
        'auth_message': 'Logged out'
    }
