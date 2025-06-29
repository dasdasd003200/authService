import strawberry


@strawberry.input
class RefreshTokenInput:
    refresh_token: str = strawberry.field(description="Refresh token to exchange for new access token")
