"""Constants for test cases"""

# User URLs
USER_LOGIN_URL = "/api/v1/users/login"
USER_REGISTRATION_URL = "/api/v1/users/register"
USER_CHANGE_PASSWORD_URL = "/api/v1/users/me/change-password"
USER_REFRESH_TOKEN_URL = "/api/v1/users/login/refresh"
USER_ME_URL = "/api/v1/users/me"
USER_LIST_URL = "/api/v1/users"
USER_DETAIL_URL = "/api/v1/users/{uid}"
USER_FORCE_RESET_PASSWORD_URL = "/api/v1/users/{uid}/force-reset-password"
USER_FORGET_PASSWORD_URL = "/api/v1/users/forget-password"

# Organization URLs
ORGANIZATION_LIST_URL = "/api/v1/organizations"
ORGANIZATION_DETAIL_URL = "/api/v1/organizations/{uid}"

# Subscription URLs
SUBSCRIPTION_LIST_URL = "/api/v1/subscriptions"
SUBSCRIPTION_DETAIL_URL = "/api/v1/subscriptions/{uid}"
