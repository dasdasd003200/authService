import strawberry
from typing import Optional, List


@strawberry.input
class UserFindInput:
    status: Optional[str] = strawberry.field(default=None, description="Filter by status")
    email_verified: Optional[bool] = strawberry.field(default=None, description="Filter by email verification")
    search_text: Optional[str] = strawberry.field(default=None, description="Search in name/email")
    page: int = strawberry.field(default=1, description="Page number")
    page_size: int = strawberry.field(default=10, description="Items per page")
    order_by: Optional[List[str]] = strawberry.field(default=None, description="Order by fields")
