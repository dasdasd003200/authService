import strawberry


@strawberry.input
class UserCreateInput:
    email: str = strawberry.field(description="User email address")
    password: str = strawberry.field(description="User password")
    first_name: str = strawberry.field(description="User first name")
    last_name: str = strawberry.field(description="User last name")
    email_verified: bool = strawberry.field(default=False, description="Email verification status")
