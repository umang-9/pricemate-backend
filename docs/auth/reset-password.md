Endpoint: /reset-password/
Auth: required

Required body parameters
old_password
new_password

Required headers
Authorization

# Example 1

Valid data

```
{
    'old_password': '****',
    'new_password': '****',
}
```

Valid Authorization

```
{
    'Authorization': 'Token ****',
}
```

Response

```
{
    "detail": "Password updated!",
}
```

`Status code: 200 OK`

# Example 2

Invalid data

```
{
    'old_password': '****invalid****',
    'new_password': '****',
}
```

Valid Authorization

```
{
    'Authorization': 'Token ****',
}
```

Response

```
{
    "detail": "Invalid password!"
}
```

`Status code: 400 BAD REQUEST`

# Example 3

Valid data

```
{
    'old_password': '****',
    'new_password': '****',
}
```

Invalid Authorization

```
{
    'Authorization': 'Token ****invalid****',
}
```

Response

```
{
    "detail": "Invalid token."
}
```

`Status code: 401 UNAUTHORIZED`
Consider deleting the token from the frontend!

# Example 4

Invalid data (weak password)

```
{
    'old_password': '****',
    'new_password': '****invalid****',
}
```

Valid Authorization

```
{
    'Authorization': 'Token ****',
}
```

Response

```
{
{
    "new_password": [
        "This password is too short. It must contain at least 8 characters.",
        "This password is too common.",
        "This password is entirely numeric."
    ]
}}
```

`Status code: 400 BAD REQUEST`
