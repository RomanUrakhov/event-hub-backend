from functools import wraps

from flask import g, jsonify, request

from src.infrastructure.services.auth import AuthException, TwitchAuthProvider


def require_authentication(func):
    auth_service = TwitchAuthProvider()

    @wraps(func)
    def wrapper(*args, **kwargs):
        id_token = request.cookies.get("id_token")

        if not id_token:
            return jsonify({"error": "Unauthorized"}), 401

        try:
            user_payload = auth_service.validate_token(id_token)
        except AuthException:
            return jsonify({"error": "Unauthorized"}), 401

        g.external_user_id = user_payload.external_id

        return func(*args, **kwargs)

    return wrapper


# def require_access(
#     event_id_field: str = None, event_action: SpecificEventAction = None
# ):
#     def decorator(func):
#         user_repository = FakeUserAccountRepository()

#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             try:
#                 user_id = g.external_user_id
#             except AttributeError as e:
#                 raise AttributeError(
#                     f"@{require_access.__name__} requires "
#                     f"@{require_authentication.__name__} decorator first"
#                 ) from e

#             event_id = None
#             if event_id_field:
#                 event_id = kwargs[event_id_field]

#             if event_id:
#                 has_access = has_event_access(
#                     user_id=user_id,
#                     event_id=event_id,
#                     action=event_action,
#                     user_account_repository=user_repository,
#                 )
#             else:
#                 has_access = has_system_access(
#                     user_id=user_id, user_account_repository=user_repository
#                 )

#             if not has_access:
#                 return jsonify({"error": "Access denied"}), 403

#             return func(*args, **kwargs)

#         return wrapper

#     return decorator
