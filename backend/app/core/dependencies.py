from typing import Optional

async def get_guest_user():
    """Returns a hardcoded guest user for all requests"""
    return {
        "id": "00000000-0000-0000-0000-000000000000",
        "email": "guest@local",
        "role": "owner"
    }