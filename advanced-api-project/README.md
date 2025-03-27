# Advanced API Project with Django REST Framework

## View Configurations

### Book Views

#### `BookListView` (/api/books/)

- **Methods**: GET (list books), POST (create book)
- **Permissions**:
  - GET: Open to all users
  - POST: Admin users only

#### `BookDetailView` (/api/books/\<id\>/)

- **Methods**: GET (retrieve book), PUT (update book), DELETE (delete book)
- **Permissions**:
  - GET: Open to all users
  - PUT, DELETE: Admin users only

#### `BookSearchView` (/api/books/search/)

- **Methods**: GET
- **Query Parameters**:
  - `author`: Filter books by author name (case-insensitive)
  - `min_year`: Minimum publication year
  - `max_year`: Maximum publication year

## Authentication

- Supports session-based and basic authentication
- Admin users have write permissions
- Read-only access for non-admin users

## Testing

1. Create a superuser
2. Use Postman or curl to interact with endpoints
3. Verify permissions and functionality
