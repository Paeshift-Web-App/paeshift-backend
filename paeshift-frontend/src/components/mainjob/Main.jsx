import React, { useState, useEffect } from "react";
import "./Jobs.css";
import { Link } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faSearch,
  faBars,
  faBarsProgress,
} from "@fortawesome/free-solid-svg-icons";
import { faBell } from "@fortawesome/free-regular-svg-icons";

import Stars from "../../assets/images/stars.png";
import iconWallet from "../../assets/images/wallet.png";
import ProfileImage from "../../assets/images/profile.png";
import Walletmodal from "../walletmodal/Walletmodal";
import axios from "axios";

// Filter buttons data
let id = 0;
export const filterButton = [
  { id: id++, title: "All", value: "all" },
  { id: id++, title: "Upcoming", value: "upcoming" },
  { id: id++, title: "Ongoing", value: "ongoing" },
  { id: id++, title: "Completed", value: "completed" },
  { id: id++, title: "Canceled", value: "canceled" },
];

const Main = () => {
  // Search input
  const [searchWork, setSearchWork] = useState("");
  // Filter state for status
  const [filterState, setFilterState] = useState("all");
  // Jobs fetched from Django
  const [jobs, setJobs] = useState([]);

  // Fetch jobs from Django on mount
  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/jobs/list") // Adjust if your endpoint differs
      .then((response) => {
        // response.data should be an array of job objects
        setJobs(response.data);
      })
      .catch((error) => {
        console.error("Error fetching jobs:", error);
      });
  }, []);

  // Handle filter button click
  const filterFunction = (e) => {
    const buttons = document.getElementsByClassName("filter-btn");
    setFilterState(e.target.value);

    // Remove 'active' from all filter buttons
    for (let index = 0; index < buttons.length; index++) {
      buttons[index].classList.remove("active");
    }
    // Add 'active' to the clicked button
    e.target.classList.add("active");
  };

  // Filter + search logic
  const filteredJobs = jobs
    // 1) Filter by status (if filterState is not "all")
    .filter((job) => {
      if (filterState === "all") return true; // show all
      return job.status?.toLowerCase() === filterState;
    })
    // 2) Filter by search input (matching job.title, for example)
    .filter((job) => {
      if (searchWork.trim() === "") return true;
      return job.title?.toLowerCase().includes(searchWork.toLowerCase());
    });

  return (
    <main className="col-12 col-md-12 col-lg-9 col-xl-10 ms-sm-auto px-md-4">
      <div className="d-flex justify-content-between align-items-center flex-wrap flex-md-nowrap pb-2">
        <div className="page_header">
          <h1 className="m-0 p-0">Jobs</h1>
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
              {filterButton.map((item) => (
                <button
                  type="button"
                  key={item.id}
                  value={item.value}
                  onClick={filterFunction}
                  className={
                    item.value === "all" ? "filter-btn active" : "filter-btn"
                  }
                >
                  {item.title}
                </button>
              ))}
            </div>
          </div>
        </div>

        <div className="row mt-3">
          <div className="cards jobs">
            {filteredJobs.map((job, key) => (
              <div className="card" key={key}>
                <div className="card_top">
                  <span className="profile_info">
                    <span>
                      <img className="prof" src={ProfileImage} alt="profile" />
                    </span>
                    <span>
                      <h4>{job.name || "Anonymous"}</h4>
                      <span className="rate_score">{job.role || "Applicant"}</span>
                    </span>
                  </span>
                  <span className="top_cta">
                    {/* status button with capital first letter */}
                    <button className={"btn " + job.status}>
                      {job.status
                        ? job.status.charAt(0).toUpperCase() +
                          job.status.slice(1)
                        : "Status"}
                    </button>
                  </span>
                </div>

                <div className="row">
                  <div className="col-12">
                    <h2>{job.title}</h2>
                  </div>
                </div>

                <div className="row">
                  <div className="col-3 pe-0">
                    <p>Location:</p>
                  </div>
                  <div className="col-9">
                    <h4 className="text-truncate">{job.location}</h4>
                  </div>
                </div>

                <div className="row">
                  <div className="col-4 pe-0">
                    <p>Date:</p>
                  </div>
                  <div className="col-8">
                    <h4>{job.date}</h4>
                  </div>
                </div>

                <div className="row">
                  <div className="col-6 pe-0">
                    <p>Time:</p>
                  </div>
                  <div className="col-6">
                    <h4>{job.time}</h4>
                  </div>
                </div>

                <div className="row">
                  <div className="col-6 pe-0">
                    <p>Contract Duration:</p>
                  </div>
                  <div className="col-6">
                    <h4>{job.duration}</h4>
                  </div>
                </div>

                <div className="row">
                  <div className="col-6 pe-0">
                    <p>Amount:</p>
                  </div>
                  <div className="col-6">
                    <h4>₦{job.amount}.00</h4>
                  </div>
                </div>

                {/* Conditionally show bottom buttons based on job.status */}
                {job.status === "upcoming" && (
                  <div className="bottom">
                    <span>
                      <button className="cancel">Cancel</button>
                    </span>
                    <span>
                      <button className="track-btn">Track Location</button>
                    </span>
                  </div>
                )}
                {job.status === "ongoing" && (
                  <div className="bottom">
                    <span>
                      <button className="cancel">01:59:48</button>
                    </span>
                    <span>
                      <button className="track-btn">Share Location</button>
                    </span>
                  </div>
                )}
                {(job.status === "completed" || job.status === "canceled") && (
                  <div className="bottom">
                    <button className="track-btn w-100">Feedback Client</button>
                  </div>
                )}
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
