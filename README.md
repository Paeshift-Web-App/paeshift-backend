Here is the complete list of endpoints formatted as requested:

---

1) **GET /jobs/all-users**  
   • Fetches a list of all user dictionaries.  
   • Returns JSON with fields like `"id"`, `"username"`, `"email"`, `"date_joined"`.

---

2) **POST /jobs/logout**  
   • Logs out the current session-based user.  
   • Requires user to be authenticated (session cookie).

---

3) **POST /jobs/change-password**  
   • Allows an authenticated user to change their password.  
   • Expects JSON:  
     ```json
     {
       "oldPassword": "...",
       "newPassword": "...",
       "confirmPassword": "..."
     }
     ```

---

4) **GET /jobs/profile**  
   • Returns the profile info of the currently logged-in user.  
   • Example JSON response:  
     ```json
     {
       "firstName": "...",
       "lastName": "...",
       "email": "...",
       "profilePicUrl": "..."
     }
     ```

---

5) **PUT /jobs/profile**  
   • Updates the logged-in user's profile.  
   • Accepts multipart/form-data (if uploading a profile pic) or JSON (for text fields only).  
   • Optional fields: `firstName`, `lastName`, `email`, `file` (profile pic).

---

6) **POST /jobs/login**  
   • Logs in a user (session-based).  
   • Expects JSON:  
     ```json
     {
       "email": "...",
       "password": "..."
     }
     ```

---

7) **POST /jobs/signup**  
   • Creates a new user account if email is unique and passwords match.  
   • Expects JSON:  
     ```json
     {
       "firstName": "...",
       "lastName": "...",
       "email": "...",
       "password": "...",
       "confirmPassword": "..."
     }
     ```

---

8) **POST /jobs/create-job**  
   • Creates a new job for the currently logged-in user.  
   • Expects JSON matching `CreateJobSchema`, e.g.:  
     ```json
     {
       "title": "...",
       "industry": "...",
       "subcategory": "...",
       "applicants_needed": 1,
       "job_type": "...",
       "shift_type": "...",
       "date": "...",
       "start_time": "...",
       "end_time": "...",
       "rate": 123.45,
       "location": "..."
     }
     ```

---

9) **GET /jobs/clientjobs**  
   • Returns all jobs posted by the currently logged-in client.  
   • Returns JSON array of job objects with fields like `"id"`, `"title"`, `"status"`, `"date"`, `"start_time"`, `"end_time"`, `"location"`, `"rate"`, etc.

---

10) **GET /jobs/accepted-list**  
    • Returns only the applications where `is_accepted = true`, plus related job details.  
    • Returns JSON array of accepted applications with fields like `"application_id"`, `"applicant_name"`, `"job"`, `"client_name"`, etc.

---

11) **GET /jobs/{job_id}**  
    • Fetches detail for a single job (by ID).  
    • Returns JSON with fields like `"title"`, `"date"`, `"start_time"`, `"end_time"`, `"location"`, `"rate"`, `"status"`, etc.

---

12) **POST /jobs/save-job/{job_id}**  
    • Saves the specified job for the current user.  
    • If the job is already saved, returns a message indicating so.

---

13) **GET /jobs/saved-jobs**  
    • Lists all jobs the current user has saved.  
    • Returns JSON array of saved jobs with fields like `"saved_job_id"`, `"saved_at"`, `"job"` (including `"title"`, `"industry"`, `"subcategory"`, `"status"`, `"location"`, etc.).

---

14) **POST /jobs/{job_id}/update-location**  
    • Allows the client user to update lat/long for a specific job.  
    • Optionally stored in DB or broadcast via WebSocket (if Channels used).  
    • Expects JSON:  
      ```json
      {
        "latitude": 123.456,
        "longitude": 78.910
      }
      ```

---

15) **POST /jobs/update-location**  
    • Updates the user's location and marks them as online.  
    • Expects JSON:  
      ```json
      {
        "lat": 123.456,
        "lng": 78.910
      }
      ```

---

16) **GET /jobs/track-applicant/{applicant_id}**  
    • Retrieves the last known location of an applicant.  
    • Returns JSON with fields like `"coordinates"` (`"lat"`, `"lng"`) and `"last_updated"`.

---

17) **POST /jobs/ratings**  
    • Submits a rating for another user.  
    • Expects JSON:  
      ```json
      {
        "reviewed_id": 1,
        "rating": 5,
        "feedback": "..."
      }
      ```

---

18) **GET /jobs/ratings/{user_id}**  
    • Retrieves all ratings for a user.  
    • Returns JSON with fields like `"user_id"`, `"username"`, `"average_rating"`, and `"ratings"` (including `"reviewer"`, `"rating"`, `"feedback"`, `"created_at"`).

---

19) **POST /jobs/{job_id}/disputes**  
    • Creates a dispute for a job.  
    • Expects JSON:  
      ```json
      {
        "title": "...",
        "description": "..."
      }
      ```

---

20) **GET /jobs/disputes/{dispute_id}**  
    • Fetches details for a dispute.  
    • Returns JSON with fields like `"id"`, `"title"`, `"description"`, `"status"`, `"created_by"`, `"created_at"`, `"updated_at"`.

---

21) **PUT /jobs/disputes/{dispute_id}**  
    • Updates an existing dispute.  
    • Expects JSON:  
      ```json
      {
        "status": "..."
      }
      ```

---

22) **GET /jobs/whoami**  
    • Returns the current user's ID, username, role, wallet balance, and reviews.  
    • Example JSON response:  
      ```json
      {
        "user_id": 1,
        "username": "...",
        "first_name": "...",
        "last_name": "...",
        "email": "...",
        "role": "...",
        "wallet_balance": "123.45",
        "badges": "...",
        "rating": 4.5,
        "user_reviews": [
          {
            "reviewer__username": "...",
            "rating": 5,
            "feedback": "...",
            "created_at": "..."
          }
        ]
      }
      ```

---

23) **GET /jobs/check-session**  
    • Checks the current session and returns the logged-in user's ID.  
    • Returns JSON:  
      ```json
      {
        "user_id": 1
      }
      ```

---

24) **GET /jobs/job-industries/**  
    • Returns all job industries.  
    • Returns JSON array of industries with fields like `"id"`, `"name"`.

---

25) **GET /jobs/job-subcategories/**  
    • Returns all job subcategories.  
    • Returns JSON array of subcategories with fields like `"id"`, `"name"`, `"industry_id"`.

---

26) **GET /jobs/payment**  
    • Renders the payment page.  
    • No input required.

---

27) **WebSocket: ws/chat/{job_id}/**  
    • Real-time chat messages for a specific job.  
    • No input required.

---

28) **WebSocket: ws/jobs/{job_id}/location/**  
    • Real-time job location updates for a specific job.  
    • No input required.

---

29) **WebSocket: ws/jobs/matching/**  
    • Real-time job matching updates.  
    • No input required.

---

This format provides a clear and concise description of each endpoint, its purpose, expected input (if any), and example output. The frontend developer can use this as a reference to integrate with the backend API.
