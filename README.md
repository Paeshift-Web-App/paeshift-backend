<<<<<<< HEAD


## 1) **GET** `/jobs/all-users`
**Description**: Returns a list of all users in the system.

- **Request**: 
  - No JSON body required.
- **Response** (200 OK):
  ```json
  {
    "users": [
      {
        "id": 1,
        "username": "john@example.com",
        "email": "john@example.com",
        "date_joined": "2025-02-18T10:10:00Z"
      },
      {
        "id": 2,
        "username": "alice@example.com",
        "email": "alice@example.com",
        "date_joined": "2025-02-18T10:12:00Z"
      }
    ]
  }
  ```

---

## 2) **POST** `/jobs/logout`
**Description**: Logs out the currently logged-in user (session-based).

- **Request**:
  - No JSON body required (just a POST).
- **Response**:
  - **200 OK**:
    ```json
    {
      "message": "Logged out successfully"
    }
    ```
  - **401** if user is not logged in:
    ```json
    {
      "error": "Not logged in"
    }
    ```

---

## 3) **POST** `/jobs/change-password`
**Description**: Changes the current user’s password if old password is correct.

- **Request** (JSON body):
  ```json
  {
    "oldPassword": "old_password_here",
    "newPassword": "new_password_here",
    "confirmPassword": "new_password_here"
  }
  ```
- **Response**:
  - **200 OK**:
    ```json
    {
      "message": "Password changed successfully"
    }
    ```
  - **400** if old password is wrong or passwords do not match:
    ```json
    {
      "error": "Incorrect old password"
    }
    ```
    or
    ```json
    {
      "error": "Passwords do not match"
    }
    ```
  - **401** if user is not logged in.

---

## 4) **GET** `/jobs/profile`
**Description**: Retrieves the current user’s profile info.

- **Request**:
  - No JSON body (just GET).
- **Response**:
  - **200 OK**:
    ```json
    {
      "first_name": "John",
      "last_name": "Doe",
      "email": "john@example.com",
      "profilePicUrl": ""
    }
    ```
  - **401** if not logged in:
    ```json
    {
      "error": "Not logged in"
    }
    ```

---

## 5) **PUT** `/jobs/profile`
**Description**: Updates the logged-in user’s profile (names, email, optional file upload).

- **Request**:
  - **Multipart/form-data** if sending a file (`profilePic`). Otherwise, JSON or form data. Example JSON:
    ```json
    {
      "first_name": "John",
      "last_name": "Doe",
      "email": "john@example.com"
    }
    ```
- **Response**:
  - **200 OK**:
    ```json
    {
      "message": "Profile updated successfully"
    }
    ```
  - **400** if email is taken, etc.
  - **401** if not logged in.

---

## 6) **POST** `/jobs/login`
**Description**: Logs a user in via email & password (session-based).

- **Request** (JSON):
  ```json
  {
    "email": "john@example.com",
    "password": "secret123"
  }
  ```
- **Response**:
  - **200 OK**:
    ```json
    {
      "message": "Login successful"
    }
    ```
  - **401**:
    ```json
    {
      "error": "Invalid credentials"
    }
    ```

---

## 7) **POST** `/jobs/signup`
**Description**: Creates a new user account + profile, then logs them in.

- **Request** (JSON):
  ```json
  {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "password": "secret123",
    "confirm_password": "secret123",
    "role": "client"  // or "applicant"
  }
  ```
- **Response**:
  - **201 Created**:
    ```json
    {
      "message": "Registration successful"
    }
    ```
  - **400** if fields missing, email exists, or passwords mismatch:
    ```json
    {
      "error": "Passwords do not match"
    }
    ```
    etc.

---

## 8) **POST** `/jobs/`
**Description**: Creates a new Job for the logged-in user (assumes user is a client).

- **Request** (JSON):
  ```json
  {
    "title": "House Cleaning",
    "description": "Need help cleaning my apartment",
    "location": "Lagos, Nigeria",
    "duration": "2 hours",
    "amount": 50.00
  }
  ```
- **Response**:
  - **200 OK**:
    ```json
    {
      "message": "Job created successfully",
      "job_id": 123
    }
    ```
  - **401** if not logged in.

---

## 9) **GET** `/jobs/client-posted`
**Description**: Returns a list of all jobs posted by clients (adjust logic if needed).

- **Request**: 
  - No body (just GET).
- **Response** (200 OK):
  ```json
  [
    {
      "id": 1,
      "name": "John", 
      "status": "upcoming",
      "title": "House Cleaning",
      "date": "",
      "time": "",
      "duration": "2 hours",
      "amount": "50.00",
      "location": "Lagos, Nigeria",
      "date_posted": "2 days ago",
      "no_of_application": 3
    },
    ...
  ]
  ```

---

## 10) **GET** `/jobs/list`
**Description**: Returns only the applications where `is_accepted = true`, plus job details.

- **Request**: 
  - No body (just GET).
- **Response**:
  ```json
  [
    {
      "application_id": 10,
      "applicant_name": "Alice",
      "is_accepted": true,
      "applied_at": "2025-02-18T09:12:00Z",
      "job_id": 1,
      "client_name": "John",
      "status": "upcoming",
      "title": "House Cleaning",
      "date": "",
      "time": "",
      "duration": "2 hours",
      "amount": "50.00",
      "location": "Lagos, Nigeria",
      "date_posted": "2 days ago",
      "no_of_application": 3
    },
    ...
  ]
  ```

---

## 11) **GET** `/jobs/{job_id}`
**Description**: Returns detail for a single job.

- **Request**: 
  - No body.
- **Response**:
  ```json
  {
    "id": 1,
    "employerName": "John",
    "title": "House Cleaning",
    "date": "",
    "time": "",
    "duration": "2 hours",
    "amount": "50.00",
    "location": "Lagos, Nigeria",
    "applicantNeeded": 1,
    "startDate": "",
    "startTime": ""
  }
  ```
  - **404** if job not found.

---

## 12) **POST** `/jobs/save-job/{job_id}`
**Description**: Saves a job (favorite) for the current user.

- **Request**:
  - No JSON body (just POST).
- **Response**:
  - **201 Created**:
    ```json
    {
      "message": "Job saved successfully."
    }
    ```
  - **200** if job is already saved:
    ```json
    {
      "message": "Job is already saved."
    }
    ```
  - **404** if job doesn’t exist.
  - **401** if user not logged in.

---

## 13) **GET** `/jobs/saved-jobs`
**Description**: Returns all jobs the current user has saved.

- **Request**:
  - No JSON body.
- **Response** (200 OK):
  ```json
  [
    {
      "saved_job_id": 5,
      "saved_at": "2025-02-18T09:15:00Z",
      "job_id": 1,
      "title": "House Cleaning",
      "status": "upcoming",
      "date": "",
      "time": "",
      "duration": "2 hours",
      "amount": "50.00",
      "location": "Lagos, Nigeria"
    },
    ...
  ]
  ```
  - **401** if not logged in.

---

## 14) **POST** `/jobs/{job_id}/update-location`
**Description**: Optionally updates lat/long for a specific job (real-time usage with Channels, if desired).

- **Request** (JSON):
  ```json
  {
    "latitude": 6.5244,
    "longitude": 3.3792
  }
  ```
- **Response**:
  ```json
  {
    "message": "Location updated (optionally broadcasted)"
  }
  ```
  - **401** if not logged in.

---

## 15) **POST** `/jobs/ratings`
**Description**: Allows a user to submit a rating for another user.

- **Request** (JSON):
  ```json
  {
    "reviewedUserId": 2,
    "rating": 90,  // out of 100
    "feedback": "Great experience!"
  }
  ```
- **Response** (200 OK):
  ```json
  {
    "message": "Rating submitted",
    "rating_id": 123
  }
  ```
  - **401** if not logged in.

---

## 16) **GET** `/jobs/ratings/{user_id}`
**Description**: Retrieves all ratings for a specific user, plus average rating.

- **Request**:
  - No body.
- **Response** (200 OK):
  ```json
  {
    "user_id": 2,
    "username": "alice@example.com",
    "average_rating": 85.5,
    "ratings": [
      {
        "id": 10,
        "reviewer": "john@example.com",
        "rating": 90,
        "feedback": "Great experience!",
        "created_at": "2025-02-18T09:15:00Z"
      },
      ...
    ]
  }
  ```
  - **404** if user doesn’t exist.

---

## 17) **POST** `/jobs/{job_id}/disputes`
**Description**: Creates a new dispute regarding a specific job.

- **Request** (JSON):
  ```json
  {
    "title": "Payment issue",
    "description": "Client refused to release payment after job completion"
  }
  ```
- **Response** (200 OK):
  ```json
  {
    "message": "Dispute created",
    "dispute_id": 456
  }
  ```
  - **401** if not logged in.
  - **404** if job not found.

---

## 18) **GET** `/jobs/{job_id}/disputes`
**Description**: Returns all disputes for a specific job.

- **Request**:
  - No JSON body.
- **Response** (200 OK):
  ```json
  [
    {
      "id": 456,
      "title": "Payment issue",
      "description": "Client refused to release payment after job completion",
      "status": "open",
      "created_by": "alice@example.com",
      "created_at": "2025-02-18T10:00:00Z",
      "updated_at": "2025-02-18T10:00:00Z"
    },
    ...
  ]
  ```
  - **404** if job not found.

---

## 19) **GET** `/jobs/disputes/{dispute_id}`
**Description**: Fetches detail for a single dispute.

- **Request**:
  - No JSON body.
- **Response** (200 OK):
  ```json
  {
    "id": 456,
    "title": "Payment issue",
    "description": "Client refused to release payment after job completion",
    "status": "open",
    "created_by": "alice@example.com",
    "created_at": "2025-02-18T10:00:00Z",
    "updated_at": "2025-02-18T10:00:00Z"
  }
  ```
  - **404** if dispute not found.

---

## 20) **PUT** `/jobs/disputes/{dispute_id}`
**Description**: Updates an existing dispute (e.g., changing status or resolution).

- **Request** (JSON):
  ```json
  {
    "status": "resolved",
    "resolution": "Paid partial refund"  // if you have such a field
  }
  ```
- **Response** (200 OK):
  ```json
  {
    "message": "Dispute updated",
    "dispute_id": 456
  }
  ```
  - **401** if not logged in.
  - **404** if dispute not found.

---

#
=======
# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react/README.md) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh





>>>>>>> bf1ab8d6de2b1bbbfd7db3d87049d9d68ada6e3f
