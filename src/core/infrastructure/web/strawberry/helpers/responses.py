from typing import Dict, Any, List, Type, Optional
import strawberry


def create_base_response_type(name: str, data_type: Optional[Type] = None):
    @strawberry.type(name=name)
    class BaseResponse:
        success: bool = strawberry.field(description="Operation success status")
        message: Optional[str] = strawberry.field(description="Human readable message")
        error_code: Optional[str] = strawberry.field(description="Error code for client handling")

        if data_type:
            data: Optional[data_type] = strawberry.field(description="Operation result data")
        else:
            data: Optional[str] = strawberry.field(description="Operation result", default=None)

    return BaseResponse


def create_pagination_response(items: list, total_count: int, page: int, page_size: int) -> Dict[str, Any]:
    total_pages = (total_count + page_size - 1) // page_size

    return {"items": items, "pagination": {"current_page": page, "page_size": page_size, "total_items": total_count, "total_pages": total_pages, "has_next": page < total_pages, "has_previous": page > 1}}


def extract_domain_errors(errors: list) -> Dict[str, str]:
    error_dict = {}
    for error in errors:
        if hasattr(error, "field") and hasattr(error, "message"):
            error_dict[error.field] = error.message
        else:
            error_dict["general"] = str(error)
    return error_dict
