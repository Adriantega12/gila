# Gila SDET Technical Challenge

## Bug reports

| Test Case ID | Test Scenario | Method / Endpoint | Environment | Expected Result | Actual Result |
| - | - | - | - | - | - |
| `test_create_user_with_duplicate_email` | Create a user. Use same email to attempt to create another user. | POST /users | dev, prod | Status code: 409, Error: "Duplicate email" | Status code: 500, `{"error": "Internal server error"}` |
| `test_create_user_invalid_email_formats` | Attempt to create a user with an invalid email format: `[thisisnotanemail, @domain, user@]` | POST /users | dev, prod | Status code: 400, body: `{"error": "Invalid email format"}` | Status code: 201, successful user creation. |
| `test_get_non_existent_user` | Do a GET of user that doesn't exists | GET /users/{email} | dev, prod | Status code: 404, `{"error": "User not found"}` | Status code: 500, `{"error": "Internal server error"}` |