from fastapi import Request, HTTPException

def get_jwt_token(req: Request):
    """
    Extracts JWT token from Authorization header of request

    Args:
        req (Request): Request Object

    Returns:
        str: JWT token from Authorization header
    """
    auth = req.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Error with JWT")
    splits = auth.split()
    token = splits[1]
    return token