Endpoint: /products/watch/
Auth: required

Required body parameters
product (id)

# Example 1

Valid data

```
{
    'product': '11',
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
    "id": "***",
    "product": "11"
}
```

`Status code: 201 CREATED`

# Example 2

Invalid data

```
{
    "product": "5000"
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
    "product": [
        "Invalid pk \"5000\" - object does not exist."
    ]
}
```

`Status code: 400 BAD REQUEST`

# Example 3

Valid data

```

{
"product": "11"
}

```

Invalid Authorization

```

{
'Authorization': 'Token \***\*invalid\*\***',
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

Invalid data (duplicate data)

```

{
    "product": "11"
}

```

Valid Authorization

```

{
    'Authorization': 'Token \*\*\*\*',
}

```

Response

```

{
    "non_field_errors": [
        "Already watching this product!"
    ]
}

```

`Status code: 400 BAD REQUEST`
