# Gila SDET Technical Challenge

## Table of contents

- [Bug Reports](#bug-reports)
- [Code Walkthrough](#code-walkthrough)
    - [Github Actions configuration](#github-actions-configuration)
    - [Environment configuration](#environment-configuration)
    - [Clients](#clients)
    - [Tests](#tests)
    - [Users' tests](#users-tests)
- [Improvements](#improvements)

## Bug reports

| Bug no. | Issue description | Method / Endpoint | Environment | Expected Result | Actual Result | Tests affected |
| - | - | - | - | - | - | - |
| 1 | Create a user. Use same email to attempt to create another user results in Internal Server Error. | POST /users | dev, prod | Status code: 409, `{"error: "Duplicate email"}` | Status code: 500, `{"error": "Internal server error"}` | `test_create_user.py::test_create_user_with_duplicate_email` |
| 2 | Attempt to create a user with an invalid email format: `[thisisnotanemail, @domain, user@]` is successful | POST /users | dev, prod | Status code: 400, body: `{"error": "Invalid email format"}` | Status code: 201, successful user creation. | `test_create_user.py::test_create_user_invalid_email_formats` |
| 3 | Do a GET of user that doesn't exists. Results in Internal Server Error | GET /users/{email} | dev, prod | Status code: 404, `{"error": "User not found"}` | Status code: 500, `{"error": "Internal server error"}` | `test_get_user.py::test_get_non_existent_user, test_delete_user.py::test_delete_user, test_delete_user.py::test_delete_user_twice, test_update_user.py` |
| 4 | Updating a user's name is not persistent | PUT /users/{email} | dev, prod | User should be updated with new name. | User is not updated with new name. | `test_update_user.py::test_update_user` |
| 5 | Authentication token is ignored when deleting a user | DELETE /users/{email} | dev | Status code: 401, `{"error": "Authentication required or invalid"}` | Status code: 204 Empty response | `test_delete_user.py::test_delete_user_missing_auth_header` |
| 6 | Error message does not match OpenAPI spec | DELETE /users/{email} | prod | Status code: 401, `{"error": "Authentication required or invalid"}` | Status code: 401, `{"error": "Authentication required"}` | `test_delete_user.py::test_delete_user_missing_auth_header` |

## Code Walkthrough

### Github Actions configuration

Inside `.github/workflows/` we can find `api-tests.yml` file. This handles the Github Actions job configuration. Here we explicitly set:
- **What rules to use for triggering jobs**: whenever a push is made against `main`, or when a Pull Request is opened against `main`.
- **Test matrix and strategy**: which individual configurations to use for each run.
- **Steps**: what is actually running. Steps that go from setting up the environment to run against, to which command to use for running the tests, and what to do with the test report.

### Environment configuration

#### .env file

Using `dotenv` it loads the configuration into the project, we can set:
- `BASE_URL`: defaults to `http://localhost:3000`
- `AUTH_TOKEN`: for setting authorization token appended to `Authentication` header.
- `ENV`: with two possible values: `dev` or `prod`

### Clients

In `clients/` we have three files:
- `api_gateway.py`: Setups all clients and serves as a single entryway into them.
- `base_client.py`: Functions as the base class file for all other client entities. The HTTP transport logic lives in this file: handles sessions, setups the base URL, setups prefix for different staging environments, setups headers and it's in charge of logging for requests.
-  `user_client.py`: Encapsulates domain-specific endpoints of User entity.

### Tests

In `tests/` we can find globally available fixtures for tests in `conftest.py`. This handles things such as:
- Call `dotenv`'s `load_dotenv` method.
- Logging for each individual test: make sure every log is available in different files. This is set to `autouse=True`.
- Using pytest, add command line option for `--env` flag.
- Load `--env` value and make it available via fixture.
- And finally, make API Gateway available to all tests via fixture.

#### Users' tests

In `tests/users/` we can find test files that are logically arranged by the HTTP verb operation these are mainly testing:
- `test_create_user.py`
- `test_delete_user.py`
- `test_get_user.py`
- `test_list_users.py`
- `test_update_user.py`

In `conftest.py` there are fixtures available to use for the tests pertaining the User entity. There are two, which are:
- `create_user_payload`: will deliver a prebuilt payload to use with the test.
- `created_user`: will deliver a User payload from a user that was already created to use with the test.

## Improvements

- [ ] Generate a **dated** log file for each test.
- [ ] Add testing for response headers, for example: `'Content-Type': 'application/json'` is in the response of requests.
- [ ] Add schema validation testing using something like `pydantic` or OpenAPI contract validator.