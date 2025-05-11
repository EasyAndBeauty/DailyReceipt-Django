SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Firebase ID Token을 입력하세요. 예: Bearer <token>",
        }
    },
    "SECURITY": [{"Bearer": []}],
    "USE_SESSION_AUTH": False,
    "VALIDATOR_URL": None,
}
