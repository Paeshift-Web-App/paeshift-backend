
### Summary of Endpoints

| **Category**         | **Endpoint**                          | **Method** | **Description**                                                                 |
|-----------------------|---------------------------------------|------------|---------------------------------------------------------------------------------|
| **Authentication**    | `/jobs/login`                         | POST       | Authenticates and logs in a user.                                               |
|                       | `/jobs/signup`                        | POST       | Creates a new user and profile.                                                 |
|                       | `/jobs/logout`                        | POST       | Logs out the current user.                                                      |
|                       | `/jobs/change-password`               | POST       | Changes the user's password.                                                    |
|                       | `/jobs/csrf-token`                    | GET        | Returns the CSRF token.                                                         |
| **User/Profile**      | `/jobs/all-users`                     | GET        | Returns a list of all users.                                                    |
|                       | `/jobs/profile`                       | GET        | Fetches the current user's profile info.                                        |
|                       | `/jobs/profile`                       | PUT        | Updates the user's profile.   
                                                  |

                                                  
| **Jobs**              | `/jobs/job-industries/`               | GET        | Returns all job industries.                                                     |
|                       | `/jobs/job-subcategories/`            | GET        | Returns all job subcategories.                                                  |
|                       | `/jobs/create-job`                    | POST       | Creates a new job.                                                              |
|                       | `/jobs/clientjobs`                    | GET        | Retrieves jobs posted by a client with pagination.                              |
|                       | `/jobs/alljobs`                       | GET        | Returns all jobs.                                                               |
|                       | `/jobs/{job_id}`                      | GET        | Returns details for a single job.                                               |
| **Saved Jobs**        | `/jobs/save-job/{job_id}`             | POST       | Saves a job for the current user.                                               |
|                       | `/jobs/save-job/{job_id}`             | DELETE     | Removes a job from the user's saved list.                                       |
|                       | `/jobs/saved-jobs`                    | GET        | Lists all saved jobs for the authenticated user.                                |
| **Ratings**           | `/jobs/ratings`                       | POST       | Submits a rating for another user.                                              |
|                       | `/jobs/ratings/{user_id}`             | GET        | Retrieves all ratings for a user.                                               |
| **Disputes**          | `/jobs/{job_id}/disputes`             | POST       | Creates a dispute for a job.                                                    |
|                       | `/jobs/disputes/{dispute_id}`         | GET        | Fetches details for a dispute.                                                  |
|                       | `/jobs/disputes/{dispute_id}`         | PUT        | Updates an existing dispute.                                                    |
| **Location**          | `/jobs/update-location`               | POST       | Updates the user's location.                                                    |
|                       | `/jobs/track-applicant/{applicant_id}`| GET        | Retrieves the last known location of an applicant.                              |
|                       | `/jobs/{job_id}/update-location`      | POST       | Updates the location of a job seeker for a specific job.                        |
| **WebSocket**         | `ws/chat/{job_id}/`                   | WebSocket  | Real-time chat messages.                                                        |
|                       | `ws/jobs/{job_id}/location/`          | WebSocket  | Real-time job location updates.                                                 |
|                       | `ws/jobs/matching/`                   | WebSocket  | Real-time job matching updates.                                                 |
| **Miscellaneous**     | `/jobs/check-session`                 | GET        | Checks the current session.                                                     |
|                       | `/jobs/accepted-list`                 | GET        | Returns accepted applications with job details.                                 |
|                       | `/jobs/industries`                    | GET        | Returns all job industries.                                                     |
|                       | `/jobs/subcategories`                 | GET        | Returns job subcategories.                                                      |
|                       | `/jobs/payment`                       | POST       | Renders the payment page.                                                       |
|                       | `/jobs/whoami`                        | GET        | Returns the current user's ID, username, role, wallet balance, and reviews.     |

---
