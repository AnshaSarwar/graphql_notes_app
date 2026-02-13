# Testing URL Parameters in FastAPI

FastAPI allows you to pass data via the URL using **Path Parameters** and **Query Parameters**.

## 1. Path Parameters
These are part of the URL path itself, defined in the code with curly braces like `{note_id}`.

- **Example Route**: `@router.get("/notes/{note_id}")`
- **How to test**: Replace the placeholder with a real value in the URL.
- **URL**: `http://127.0.0.1:8000/notes/5` (where `5` is the `note_id`)

## 2. Query Parameters
These are optional key-value pairs added to the end of a URL after a `?`.

- **Example Route**: 
  ```python
  @app.get("/items/")
  def read_item(skip: int = 0, limit: int = 10):
      return {"skip": skip, "limit": limit}
  ```
- **How to test**: Append `?key=value` to the URL. Use `&` to separate multiple parameters.
- **URL**: `http://127.0.0.1:8000/items/?skip=20&limit=50`

## 3. Testing via Swagger UI (Recommended)
The easiest way to test both is via the interactive documentation:
1. Go to: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
2. Expand a route (e.g., `GET /notes/{note_id}`).
3. Click "Try it out".
4. Fill in the fields for path or query parameters.
5. Click "Execute". FastAPI will show you the exact curl command and request URL it generated.

## 4. Testing via Browser/PowerShell
For simple `GET` requests:
- **Browser**: Just paste the URL (e.g., `http://127.0.0.1:8000/notes/1`) in the address bar.
- **PowerShell**:
  ```powershell
  Invoke-RestMethod -Uri "http://127.0.0.1:8000/notes/1"
  ```
> [!NOTE]
> For routes that require authentication (like `/notes/`), you must provide a Bearer Token in the headers, which is easier to do via Swagger UI or a tool like Postman.
