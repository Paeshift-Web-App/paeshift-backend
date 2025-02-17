
----------------------------------------------------------------
1)  GET /jobs/all-users
    • Fetches a list of all user dictionaries.
    • Returns JSON with fields like "id", "username", "email", "date_joined".

----------------------------------------------------------------
2)  POST /jobs/logout
    • Logs out the current session-based user.
    • Requires user to be authenticated (session cookie).

----------------------------------------------------------------
3)  POST /jobs/change-password
    • Allows an authenticated user to change their password.
    • Expects JSON:
      {
        "oldPassword": "...",
        "newPassword": "...",
        "confirmPassword": "..."
      }

----------------------------------------------------------------
4)  GET /jobs/profile
    • Returns the profile info of the currently logged-in user.
    • Example JSON response:
      {
        "firstName": "...",
        "lastName": "...",
        "email": "...",
        "profilePicUrl": "..."
      }

----------------------------------------------------------------
5)  PUT /jobs/profile
    • Updates the logged-in user's profile.
    • Accepts multipart/form-data (if uploading a profile pic)
      or JSON (for text fields only).
    • Optional fields: firstName, lastName, email, file (profile pic).

----------------------------------------------------------------
6)  POST /jobs/login
    • Logs in a user (session-based).
    • Expects JSON:
      {
        "email": "...",
        "password": "..."
      }

----------------------------------------------------------------
7)  POST /jobs/signup
    • Creates a new user account if email is unique and passwords match.
    • Expects JSON:
      {
        "firstName": "...",
        "lastName": "...",
        "email": "...",
        "password": "...",
        "confirmPassword": "..."
      }

----------------------------------------------------------------
8)  POST /jobs/
    • Creates a new job for the currently logged-in user.
    • Expects JSON matching CreateJobSchema, e.g.:
      {
        "title": "...",
        "description": "...",
        "location": "...",
        "duration": "...",
        "amount": 123.45,
        ...
      }

----------------------------------------------------------------
9)  GET /jobs/client-posted
    • Returns all jobs posted by clients (adjust logic as needed).
    • Returns JSON array of job objects with fields like "id", "title", "status", etc.

----------------------------------------------------------------
10) GET /jobs/list
    • Returns only the applications where is_accepted = true,
      plus related job details.

----------------------------------------------------------------
11) GET /jobs/{job_id}
    • Fetches detail for a single job (by ID).
    • Returns JSON with fields like "title", "date", "time", "location", etc.

----------------------------------------------------------------
12) POST /jobs/save-job/{job_id}
    • Saves the specified job for the current user.
    • If job is already saved, returns a message indicating so.

----------------------------------------------------------------
13) GET /jobs/saved-jobs
    • Lists all jobs the current user has saved.
    • Returns JSON array of saved jobs with relevant fields.

----------------------------------------------------------------
14) POST /jobs/{job_id}/update-location
    • Allows the client user to update lat/long for a specific job.
    • Optionally stored in DB or broadcast via WebSocket (if Channels used).
    • Expects JSON:
      {
        "latitude": 123.456,
        "longitude": 78.910
      }
