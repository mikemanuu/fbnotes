# API Documentation (brief)

Base: /api/v1/

Auth:
- POST /auth/register/ {username,email,password} -> 201
- POST /auth/login/ {username,password} -> {access,refresh}

Bookmarks:
- GET /bookmarks/ -> list (JWT)
- POST /bookmarks/ -> create {url, title?, tags:[], notes:[]} -> returns bookmark
- GET /bookmarks/{id}/ -> retrieve details
- PUT/PATCH /bookmarks/{id}/ -> update
- DELETE /bookmarks/{id}/ -> archives

Notes:
- POST /bookmarks/{id}/notes/ -> create note

Extension:
- POST /ext/capture/ -> accepts {url,snippet,page_title,timestamp,screenshot_base64?} -> returns draft id

Internal:
- POST /internal/fetch-metadata/ -> accepts {bookmark_id or url} and requires INTERNAL_TOKEN header set to `X-Internal-Token`
