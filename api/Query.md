> /api/v1.0/products?fields={
    "id": "upper",
    "name": ["lower", "escape", "utf8"]
    "photos": {
        "id": "",
        "name":""
        ...
    }
  }
  
> /api/v1.0/users?q={
    "__and": {
      "id": ":=:123456",
      "age": {
        "__and": [
          ":>:30",
          ":<:60"
        ]
      },
      "__or": {
        "first_name": ":like:gia%",
        "last_name": ":like:le%"
      },
      "email": {
        "__or": [
          ":like:%gmail.com", 
          ":like:%yahoo.com"
        ]
      }
    }
  }
  
> /api/v1.0/categories?limit=10&page=0