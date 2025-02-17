import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import "./Main.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSearch, faBars } from "@fortawesome/free-solid-svg-icons";
import { faBell, faBookmark } from "@fortawesome/free-regular-svg-icons";

import Stars from "../../assets/images/stars.png";
import iconWallet from "../../assets/images/wallet.png";
import ProfileImage from "../../assets/images/profile.png";
import Walletmodal from "../walletmodal/Walletmodal";
import axios from "axios";

const Main = () => {
  const [searchWork, setSearchWork] = useState("");
  const [jobs, setJobs] = useState([]); // We'll store the fetched "client-posted" jobs

  // 1) Fetch "client-posted" jobs from Django on mount
  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/jobs/client-posted") // Adjust to your actual endpoint
      .then((response) => {
        setJobs(response.data); // response.data should be an array of jobs
      })
      .catch((error) => {
        console.error("Error fetching client-posted jobs:", error);
      });
  }, []);

  // 2) Handle Save Job
  const handleSaveJob = (jobId) => {
    axios
      .post(`http://127.0.0.1:8000/jobs/save-job/${jobId}`)
      .then((response) => {
        alert(response.data.message); 
      })
      .catch((error) => {
        console.error("Error saving job:", error);
        if (error.response?.data?.error) {
          alert(error.response.data.error);
        }
      });
  };

  // 3) Filter by search input (job.title)
  const filteredJobs = jobs.filter((job) => {
    if (searchWork.trim() === "") return true;
    return job.title?.toLowerCase().includes(searchWork.toLowerCase());
  });

  return (
    <main className="col-12 col-md-12 col-lg-9 col-xl-10 ms-sm-auto px-md-4">
      <div className="d-flex justify-content-between align-items-center flex-wrap flex-md-nowrap pb-2">
        <div className="page_header">
          <h1 className="m-0 p-0">Home</h1>
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
            <button type="button" className="notification-icon px-3">
              <FontAwesomeIcon icon={faBell} />
            </button>
          </div>
          <button
            type="button"
            className="btn btn-wallet px-3"
            data-bs-toggle="modal"
            data-bs-target="#walletModal"
          >
            <img src={iconWallet} alt="wallet" /> ₦0.00
          </button>
        </div>
      </div>

      <section className="container container__data">
        <div className="row m-0 p-0">
          <div className="col-12 m-0 p-0">
            <div className="filter-section">
              <button type="button" className="filter-btn active">All</button>
              <select name="shiftType" id="">
                <option value="">Type of Shift</option>
                <option value="1">Day Shift</option>
                <option value="2">Night Shift</option>
              </select>
              <select name="jobType" id="">
                <option value="">Sort Jobs By</option>
                <option value="1">General Handyman</option>
                <option value="2">Electrician</option>
                <option value="3">Plumber</option>
              </select>
            </div>
          </div>
        </div>

        <div className="row mt-3">
          <div className="cards">
            {filteredJobs.map((item, key) => (
              <div className="card" key={key}>
                <div className="card_top">
                  <span className="profile_info">
                    <span>
                      <img className="prof" src={ProfileImage} alt="profile" />
                    </span>
                    <span>
                      <h4>{item.name || "Anonymous Client"}</h4>
                      <img src={Stars} alt="stars" /> <span className="rate_score">4.98</span>
                    </span>
                  </span>
                  <span className="top_cta">
                    {/* 4) "Save Job" button calls handleSaveJob */}
                    <button
                      className="btn active"
                      onClick={() => handleSaveJob(item.id)}
                    >
                      Save Job &nbsp; <FontAwesomeIcon icon={faBookmark} className="icon-saved" />
                    </button>
                  </span>
                </div>

                <div className="duration">
                  <h3>{item.duration} Contract </h3>
                  <span className="time_post">{item.date_posted || "2 days ago"}</span>
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
                    <p>
                      {item.no_of_application || 0} applicant
                      needed
                    </p>
                  </span>
                  <span>
                    <Link to="../jobdetails" className="btn">
                      View Job Details
                    </Link>
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <Walletmodal />
      </section>
    </main>
  );
};

export default Main;
