# from django.conf import settings
# from django.shortcuts import redirect
# from rest_framework_simplejwt.tokens import RefreshToken
# from social_core.pipeline.partial import partial
#
# @partial
# def jwt_popup_redirect(strategy, backend, user, request, *args, **kwargs):
#     """Create JWT tokens for user that logged in using social auth"""
#
#     # Generate token
#     # refresh = RefreshToken.for_user(user)
#     #
#     # # Store tokens in session
#     # strategy.session_set('jwt_access_token', str(refresh.access_token))
#     # strategy.session_set('jwt_refresh_token', str(refresh))
#     #
#     # return {
#     #     'user': user,
#     #     'access_token': str(refresh.access_token),
#     #     'refresh_token': str(refresh)
#     # }
#     print('JWT popup redirect||||', user, type(user), request.user)
#     return redirect(settings.FRONTEND_URL.rstrip('/') + '/oauth/popup')
#
def save_google_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'google-oauth-2':
        return

    given_name = response.get('given_name')
    family_name = response.get('family_name')
    picture = response.get('picture')
    email = response.get('email')

    if given_name:
        user.first_name = given_name
    if family_name:
        user.last_name = family_name

    if not user.username and email:
        user.username = email.split('@')[0]

    # TODO: Add profile
    user.save()