# TeleForge
A Telegram Bot Manager

## API authentication

The REST API uses JWT bearer authentication. Register with `POST /register/`,
activate the account with `POST /register/otp/`, or sign in with
`POST /login/`. Successful activation and sign-in responses include `access`
and `refresh` tokens alongside the existing message.

Send the access token on protected API requests:

```http
Authorization: Bearer <access>
```

Access tokens expire after 5 minutes. Exchange a refresh token with
`POST /token/refresh/` using `{"refresh": "<refresh>"}`; refresh tokens rotate
on use, so persist the newly returned refresh token securely in the Flutter
client. Sign out with an authenticated `POST /logout/` containing the current
refresh token; this revokes it. Django sessions remain enabled for the built-in
admin, but are not used to authenticate REST API requests.
