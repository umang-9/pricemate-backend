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
