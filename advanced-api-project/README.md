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

# Book API - Advanced Querying Guide

## Filtering

### By Title

- Endpoint: `/api/books/`
- Query Parameter: `title`
- Example: `/api/books/?title=Django`
- Matches books with titles containing "Django" (case-insensitive)

### By Publication Year

- Exact Match: `/api/books/?publication_year=2023`
- Greater Than: `/api/books/?publication_year__gt=2020`
- Less Than: `/api/books/?publication_year__lt=2022`

### By Author Name

- Endpoint: `/api/books/`
- Query Parameter: `author_name`
- Example: `/api/books/?author_name=John`
- Matches books by authors with names containing "John"

## Searching

### Full-Text Search

- Endpoint: `/api/books/`
- Query Parameter: `search`
- Example: `/api/books/?search=Python`
- Searches across title and author name

## Ordering

### Sort Books

- Endpoint: `/api/books/`
- Query Parameter: `ordering`
- Ascending: `/api/books/?ordering=title`
- Descending: `/api/books/?ordering=-publication_year`

### Supported Ordering Fields

- `title`
- `publication_year`
- `author__name`

## Combining Queries

You can combine multiple query parameters:
`/api/books/?title=Django&publication_year__gt=2020&ordering=-publication_year&search=Web`

## Example Requests

1. Find Django books published after 2020, sorted by publication year:

   ```
   GET /api/books/?title=Django&publication_year__gt=2020&ordering=-publication_year
   ```

2. Search for books by an author, sorted alphabetically:
   ```
   GET /api/books/?search=John&ordering=title
   ```
