# Gila SDET Technical Challenge

## Bug reports

| Issue description | Method / Endpoint | Environment | Expected Result | Actual Result | Tests affected |
| - | - | - | - | - | - |
| Create a user. Use same email to attempt to create another user results in Internal Server Error. | POST /users | dev, prod | Status code: 409, Error: "Duplicate email" | Status code: 500, `{"error": "Internal server error"}` | `test_create_user.py::test_create_user_with_duplicate_email` |
| Attempt to create a user with an invalid email format: `[thisisnotanemail, @domain, user@]` is successful | POST /users | dev, prod | Status code: 400, body: `{"error": "Invalid email format"}` | Status code: 201, successful user creation. | `test_create_user.py::test_create_user_invalid_email_formats` |
| Do a GET of user that doesn't exists. Results in Internal Server Error | GET /users/{email} | dev, prod | Status code: 404, `{"error": "User not found"}` | Status code: 500, `{"error": "Internal server error"}` | `test_get_user.py::test_get_non_existent_user, test_delete_user.py::test_delete_user, test_delete_user.py::test_delete_user_twice, test_update_user.py` |
| Updating a user's name is not persistent | PUT /users/{email} | dev, prod | User should be updated with new name. | User is not updated with new name. | `test_update_user.py::test_update_user` |