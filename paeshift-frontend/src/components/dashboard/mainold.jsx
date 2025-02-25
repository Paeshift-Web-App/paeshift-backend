
//       {/* POST JOB BUTTON */}
//       <button
//         type="button"
//         className="btn-post px-3"
//         data-bs-toggle="modal"
//         data-bs-target="#postModal"
//       >
//         Post a new Job &nbsp; <FontAwesomeIcon icon={faSquarePlus} />
//       </button>

//       {/* MAIN CONTENT */}
//       <section className="container container__data">
//         {/* Profile Info */}
//         <div className="row m-0 mt-3 dashboard_profile">
//       <div className="col-5 col-md-4 col-xl-2 p-0">
//         <div className="profile_wrapper">
//           <img src={profileData.profileImage || "default_profile.jpg"} alt="Profile" />
//         </div>
//       </div>
//       <div className="col-7 col-md-8 col-xl-10 ps-xl-5">
//         <h3>{profileData.name || "User Name"}</h3>
//         <p>{profileData.role || "Role"}</p>
//         <p>Rating</p>
//         <span>
//           <img src={"stars_icon.png"} alt="profile" />{" "}
//           <span className="rate_score">{profileData.rating || "N/A"}</span>
//         </span>
//         <p>Email Address</p>
//         <h4>{profileData.email || "user@example.com"}</h4>
//       </div>
//       <div className="col-12 col-md-4 col-xl-2"></div>
//       <div className="col-12 col-md-8 col-xl-10 p-0 ps-xl-5">
//         <button type="button" className="btn edit-btn">
//           Edit Profile
//         </button>
//       </div>
//     </div>

//     const [profileData, setProfileData] = useState(null);

// useEffect(() => {
//   const fetchProfile = async () => {
//     try {
//       setProfileData(response.data);
//     } catch (error) {
//       console.error("Error fetching profile data:", error);
//     }
//   };

//   fetchProfile();
// }, []);

// if (!profileData) {
//   return <p>Loading...</p>; // Show loading state until data is fetched
// }










import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./Main.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faServer,
  faUser,
  faUserGroup,
  faSearch,
  faPlus,
  faBriefcase,
  faBars,
} from "@fortawesome/free-solid-svg-icons";
import {
  faBell,
  faBookmark,
  faCircleUser,
  faSquarePlus,
} from "@fortawesome/free-regular-svg-icons";

import Stars from "../../assets/images/stars.png";
import iconWallet from "../../assets/images/wallet.png";
import iconLogo from "../../assets/images/icon-logo.png";
import Axios from "axios";
import ProfileImage from "../../assets/images/profile.png";
import Profile from "../../assets/images/profileimage.png";
import Postmodal from "../postmodal/Postmodal";
import Notificationmodal from "../notificationmodal/Notificationmodal";
import Jobrequestmodal from "../jobrequestsmodal/Jobrequestmodal";

const Main = () => {
  // For searching
  const [searchWork, setSearchWork] = useState("");

  // List of jobs from the backend
  const [jobs, setJobs] = useState([]);

  // IDs of jobs the user has saved
  const [savedJobIds, setSavedJobIds] = useState([]);

  // Fetch jobs on mount
  useEffect(() => {
    // Example: "client-posted" returns a list of jobs
    Axios.get("http://127.0.0.1:8000/jobs/client-posted", { withCredentials: true })
      .then((response) => {
        // 'response.data' should be an array of jobs
        setJobs(response.data);
      })
      .catch((error) => {
        console.error("Error fetching jobs:", error);
      });
  }, []);

  // Fetch saved jobs on mount
  useEffect(() => {
    Axios.get("http://127.0.0.1:8000/jobs/saved-jobs", { withCredentials: true })
      .then((response) => {
        // response.data might look like: [
        //   { saved_job_id: 1, job_id: 10, ... },
        //   { saved_job_id: 2, job_id: 15, ... },
        //   ...
        // ]
        const savedIds = response.data.map((record) => record.job_id);
        setSavedJobIds(savedIds);
      })
      .catch((error) => {
        console.error("Error fetching saved jobs:", error);
      });
  }, []);

  // Toggle function to either POST (save) or DELETE (unsave)
  const handleToggleSave = async (jobId) => {
    const isSaved = savedJobIds.includes(jobId);

    try {
      if (isSaved) {
        // If already saved, we call DELETE to unsave
        await Axios.delete(`http://127.0.0.1:8000/jobs/save-job/${jobId}`, {
          withCredentials: true,
        });
        // Remove from local state
        setSavedJobIds((prev) => prev.filter((id) => id !== jobId));
      } else {
        // If not saved, we call POST to save
        await Axios.post(
          `http://127.0.0.1:8000/jobs/save-job/${jobId}`,
          {},
          { withCredentials: true }
        );
        // Add to local state
        setSavedJobIds((prev) => [...prev, jobId]);
      }
    } catch (error) {
      console.error("Error toggling save:", error);
    }
  };

  // Filter jobs by search term
  const filteredJobs = jobs.filter((item) => {
    if (!searchWork.trim()) return true;
    return item.title.toLowerCase().includes(searchWork.toLowerCase());
  });

  return (
    <main className="col-12 col-md-12 col-lg-9 col-xl-10 ms-sm-auto px-md-4">
      {/* HEADER */}
      <div className="d-flex justify-content-between align-items-center flex-wrap flex-md-nowrap align-items-center pb-2">
        <div className="page_header">
          <h1 className="m-0 p-0">Dashboard</h1>
          <div>
            <button
              className="navbar-toggler position-absolute d-lg-none collapsed"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#sidebarMenu"
              aria-controls="sidebarMenu"
              aria-expanded="false"
              aria-label="Toggle navigation"
            >
              <FontAwesomeIcon className="icon-bars" icon={faBars} />
            </button>
          </div>
        </div>
        <div className="searchbar-section">
          <div className="serachbar-notify">
            <div className="me-2 searchbar">
              <input
                className="form-control searchbar-input"
                onChange={(e) => setSearchWork(e.target.value)}
                type="text"
                placeholder="Search"
                aria-label="Search"
              />
              <FontAwesomeIcon className="search-icon" icon={faSearch} />
            </div>
            <button
              type="button"
              className="notification-icon px-3"
              data-bs-toggle="modal"
              data-bs-target="#notificationModal"
            >
              <FontAwesomeIcon icon={faBell} />
            </button>
          </div>
        </div>
      </div>

      {/* POST JOB BUTTON */}
      <button
        type="button"
        className="btn-post px-3"
        data-bs-toggle="modal"
        data-bs-target="#postModal"
      >
        Post a new Job &nbsp; <FontAwesomeIcon icon={faSquarePlus} />
      </button>

      {/* MAIN CONTENT */}
      <section className="container container__data">
        {/* Profile Info */}
        <div className="row m-0 mt-3 dashboard_profile">
          <div className="col-5 col-md-4 col-xl-2 p-0">
            <div className="profile_wrapper">
              <img src={Profile} alt="Profile" />
            </div>
          </div>
          <div className="col-7 col-md-8 col-xl-10 ps-xl-5">
            <h3>Esther Grace</h3>
            <p>Employer</p>
            <p>Rating</p>
            <span>
              <img src={Stars} alt="profile" /> <span className="rate_score">4.98</span>
            </span>
            <p>Email Address</p>
            <h4>eniolalucas@gmail.com</h4>
          </div>
          <div className="col-12 col-md-4 col-xl-2"></div>
          <div className="col-12 col-md-8 col-xl-10 p-0 ps-xl-5">
            <button type="button" className="btn edit-btn">
              Edit Profile
            </button>
          </div>
        </div>

        {/* Dashboard stats */}
        <div className="row dashboard_user_data">
          <div className="col-6 col-md-3 user_data">
            <span>
              <FontAwesomeIcon icon={faBriefcase} className="user_data_icon" />
            </span>
            <span>
              <p>Total Job Posted</p>
              <h5>1,230</h5>
            </span>
          </div>
          <div className="col-6 col-md-3 user_data">
            <span>
              <FontAwesomeIcon icon={faCircleUser} className="user_data_icon" />
            </span>
            <span>
              <p>Total workers engaged</p>
              <h5>28</h5>
            </span>
          </div>
          <div className="col-6 col-md-3 user_data">
            <span>
              <FontAwesomeIcon icon={faBriefcase} className="user_data_icon" />
            </span>
            <span>
              <p>Total Completed Jobs</p>
              <h5>1,210</h5>
            </span>
          </div>
          <div className="col-6 col-md-3 user_data">
            <span>
              <FontAwesomeIcon icon={faBriefcase} className="user_data_icon" />
            </span>
            <span>
              <p>Total Cancelled Jobs</p>
              <h5>20</h5>
            </span>
          </div>
        </div>

        {/* Job Listing */}
        <div className="row mt-3">
          <div className="col-12 top_title">
            <h3>Your Recent Job Requests</h3>
            <span>
              <button
                type="button"
                data-bs-toggle="modal"
                data-bs-target="#jobrequestModal"
              >
                See More
              </button>
            </span>
          </div>

          {/* Card List */}
          <div className="cards p-0">
            {filteredJobs.map((item) => {
              const isSaved = savedJobIds.includes(item.id);

              return (
                <div className="card" key={item.id}>
                  <div className="card_top">
                    <span className="profile_info">
                      <span>
                        <img className="prof" src={ProfileImage} alt="profile" />
                      </span>
                      <span>
                        <h4>{item.name || "Anonymous Client"}</h4>
                        <img src={Stars} alt="profile" />{" "}
                        <span className="rate_score">4.98</span>
                      </span>
                    </span>
                    <span className="top_cta">
                      {/* Toggle Save/Unsave */}
                      <button
                        className={`btn ${isSaved ? "active" : ""}`}
                        onClick={() => handleToggleSave(item.id)}
                      >
                        {isSaved ? "Unsave" : "Save"} &nbsp;
                        <FontAwesomeIcon icon={faBookmark} className="icon-saved" />
                      </button>
                    </span>
                  </div>
                  <div className="duration">
                    <h3>{item.duration} Contract </h3>
                    <span className="time_post">
                      {item.date_posted || "2 days ago"}
                    </span>
                  </div>
                  <span className="title">
                    <h3>{item.title}</h3>
                  </span>
                  <h4>
                    {item.date}. {item.time}
                  </h4>
                  <span className="address text-truncate">{item.location}</span>
                  <div className="price">
                    <span>
                      <h6>₦{item.amount}/hr</h6>
                      <p>{item.no_of_application || 0} applicant needed</p>
                    </span>
                    <span>
                      <Link to="../jobdetails" className="btn">
                        View Job Details
                      </Link>
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Modals */}
        <Jobrequestmodal />
        <Notificationmodal />
        <Postmodal />
      </section>
    </main>
  );
};

export default Main;
