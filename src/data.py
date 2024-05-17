BASE_URL = 'https://stellarburgers.nomoreparties.site/'


class Endpoints:
    create_user_path = 'api/auth/register'
    login_path = 'api/auth/login'
    user_path = 'api/auth/user'
    get_ingredients_path = 'api/ingredients'
    order_path = 'api/orders'


class ResponseTexts:
    error_user_already_exists = '{"success":false,"message":"User already exists"}'
    error_missing_mandatory_field = '{"success":false,"message":"Email, password and name are required fields"}'
    error_incorrect_password_or_email = '{"success":false,"message":"email or password are incorrect"}'
    error_unauthorised_user = '{"success":false,"message":"You should be authorised"}'
    error_empty_ingredients = '{"success":false,"message":"Ingredient ids must be provided"}'
    error_incorrect_ids = '{"success":false,"message":"One or more ids provided are incorrect"}'
