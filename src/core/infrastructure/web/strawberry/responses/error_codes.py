from enum import Enum


class StandardErrorCodes(Enum):
    # Validation errors
    VALIDATION_ERROR = "VALIDATION_ERROR"
    FIELD_REQUIRED = "FIELD_REQUIRED"
    FIELD_EMPTY = "FIELD_EMPTY"
    INVALID_FORMAT = "INVALID_FORMAT"
    INVALID_UUID = "INVALID_UUID"
    INVALID_EMAIL = "INVALID_EMAIL"

    # Business logic errors
    NOT_FOUND = "NOT_FOUND"
    ALREADY_EXISTS = "ALREADY_EXISTS"
    CONFLICT = "CONFLICT"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"

    # System errors
    SYSTEM_ERROR = "SYSTEM_ERROR"
    DATABASE_ERROR = "DATABASE_ERROR"
    EXTERNAL_SERVICE_ERROR = "EXTERNAL_SERVICE_ERROR"

    # Operation specific
    CREATE_FAILED = "CREATE_FAILED"
    UPDATE_FAILED = "UPDATE_FAILED"
    DELETE_FAILED = "DELETE_FAILED"
    FIND_FAILED = "FIND_FAILED"

    # Criteria specific
    CRITERIA_REQUIRED = "CRITERIA_REQUIRED"
    INVALID_CRITERIA = "INVALID_CRITERIA"


class StandardMessages:
    # Success messages
    CREATED_SUCCESS = "Item created successfully"
    UPDATED_SUCCESS = "Item updated successfully"
    DELETED_SUCCESS = "Item deleted successfully"
    FOUND_SUCCESS = "Items retrieved successfully"
    FOUND_ONE_SUCCESS = "Item retrieved successfully"

    # Error messages
    NOT_FOUND_ERROR = "Item not found"
    VALIDATION_ERROR = "Validation failed"
    UNAUTHORIZED_ERROR = "Unauthorized access"
    SYSTEM_ERROR = "System error occurred"
