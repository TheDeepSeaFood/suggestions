from .base import *  # noqa: F401, F403

DEBUG = False

ALLOWED_HOSTS = [
    "suggestions.thedeepseafood.com",
    "40.172.112.124",
    "localhost",
]  # Example - Need to Replace with the server IP - Do not remove localhost

FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10 MB (in bytes)

DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10 MB (in bytes)

# Database
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.mysql",
#         "NAME": os.getenv("NAME"),  # noqa: F405
#         "USER": os.getenv("USER"),  # noqa: F405
#         "PASSWORD": os.getenv("PASSWORD"),  # noqa: F405
#         "HOST": os.getenv("HOST"),  # noqa: F405
#         "PORT": os.getenv("PORT"),  # noqa: F405
#         "OPTIONS": {
#             "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
#         },
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
    }
}
