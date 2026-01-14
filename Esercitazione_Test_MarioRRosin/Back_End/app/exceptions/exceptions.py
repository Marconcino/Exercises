# The exception file has the intention to raise 
# any message anytime the program finds an error

from fastapi import HTTPException, status

# Custom exception for user not found
class UserNotFound(HTTPException):
    # Raised when user ID doesn't exist
    def __init__(self, user_id: int):
        super().__init__(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"User with ID {user_id} not found"
        )


# Custom exception for email already exists
class EmailAlreadyExists(HTTPException):
    # Raised when trying to create/update user with duplicate email
    def __init__(self, email: str):
        super().__init__(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = f"Email '{email}' already exists in database"
        )


# Custom exception for invalid email format
class InvalidEmailFormat(HTTPException):
    # Raised when email format is invalid
    def __init__(self, email: str):
        super().__init__(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = f"Email '{email}' is not in valid format"
        )


# Custom exception for invalid name
class InvalidNameFormat(HTTPException):
    # Raised when name is empty or too short
    def __init__(self, reason: str = "Name cannot be empty"):
        super().__init__(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = reason
        )


# Generic database error
class DatabaseError(HTTPException):
    # Raised when database operation fails
    def __init__(self, message: str = "Database operation failed"):
        super().__init__(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = message
        )