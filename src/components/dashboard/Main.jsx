import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./Main.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faServer, faUser, faUserGroup, faSearch, faPlus, faBriefcase, } from "@fortawesome/free-solid-svg-icons";
import { faBell, faBookmark, faCircleUser, faSquarePlus } from "@fortawesome/free-regular-svg-icons";

import Stars from "../../assets/images/stars.png";
import iconWallet from "../../assets/images/wallet.png";
import iconLogo from "../../assets/images/icon-logo.png";
import Axios from "axios";
import { faBarsProgress } from "@fortawesome/free-solid-svg-icons";
import { faBars } from "@fortawesome/free-solid-svg-icons";
import ProfileImage from "../../assets/images/profile.png";
import Profile from "../../assets/images/profileimage.png";
import Postmodal from "../postmodal/Postmodal";


import { JobsData } from "../JobsData";
// import { defaults } from "chart.js/auto";
// import { Bar, Line } from "react-chartjs-2";
// import { ChartData } from "./Chartdata";
// import { userInfo } from "../../atoms/User.jsx";
// import { useRecoilValue } from "recoil";



// defaults.maintainAspectRatio = false;
// defaults.responsive = true;

// defaults.plugins.title.display = true;
// defaults.plugins.title.align = "start";
// defaults.plugins.title.font.size = 20;
// defaults.plugins.title.color = "black";

const Main = () => {
  // let user = useRecoilValue(userInfo);
  const [searchWork, setSearchWork] = useState("");

  const [users, setUsers] = useState();



  // useEffect(() => {

  //   Axios.get("http://localhost:8000/Products")
  //     .then((response) => {
  //       setProduct(response.data);
  //     })
  //     .catch((error) => console.error(error));



  //   Axios.get("http://localhost:8000/Admin")
  //     .then((response) => {
  //       setAdmins(response.data);
  //     })
  //     .catch((error) => console.error(error));

  //   Axios.get("http://localhost:8000/Users")
  //     .then((response) => {
  //       setUsers(response.data);
  //       })
  //       .catch((error) => console.error(error));
  // }, []);

  // console.log(user.data)


  return (
    <main className="col-12 col-md-12 col-lg-9 col-xl-10 ms-sm-auto  px-md-4">
      <div className="d-flex justify-content-between align-items-center flex-wrap flex-md-nowrap align-items-center pb-2">
        <div className="page_header">
          <h1 className="m-0 p-0">Dashboard</h1>
          <div className="">
            <button className="navbar-toggler position-absolute d-lg-none collapsed" type="button"
              data-bs-toggle="collapse" data-bs-target="#sidebarMenu" aria-controls="sidebarMenu" aria-expanded="false" aria-label="Toggle navigation"
            >
              <FontAwesomeIcon className="icon-bars" icon={faBars} />
            </button>
          </div>
        </div>
        <div className="searchbar-section">
          <div className="serachbar-notify">
            <div className="me-2 searchbar">
              <input className="form-control searchbar-input" onChange={(e) => setSearchWork(e.target.value)} type="text" placeholder="Search" aria-label="Search" />
              <FontAwesomeIcon className="search-icon" icon={faSearch} />
            </div>
            <button type="button" className="notification-icon px-3">
              <FontAwesomeIcon className="" icon={faBell} />
            </button>
          </div>
        </div>
      </div>
      <button type="button" className=" btn-post px-3" data-bs-toggle="modal" data-bs-target="#postModal">
        Post a new Job &nbsp; <FontAwesomeIcon icon={faSquarePlus} />
      </button>
      <section className="container container__data">
        <div className="row m-0 mt-3 dashboard_profile">
          <div className="col-5 col-md-4 col-xl-2 p-0">
            <div className="profile_wrapper">
              <img src={Profile} alt="Profile Image" />
            </div>
          </div>
          <div className="col-7 col-md-8 col-xl-10 ps-xl-5 ">
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
            <button type="button" className="btn edit-btn">Edit Profile</button>
          </div>
        </div>
        <div className="row  dashboard_user_data">
          <div className="col-6 col-md-3 user_data">
            <span><FontAwesomeIcon icon={faBriefcase} className="user_data_icon" /> </span>
            <span>
              <p>Total Job Posted</p>
              <h5>1,230</h5>
            </span>
          </div>
          <div className="col-6 col-md-3 user_data">
            <span><FontAwesomeIcon icon={faCircleUser} className="user_data_icon" /> </span>
            <span>
              <p>Total workers engaged</p>
              <h5>28</h5>
            </span>
          </div>
          <div className="col-6 col-md-3 user_data">
            <span><FontAwesomeIcon icon={faBriefcase} className="user_data_icon" /> </span>
            <span>
              <p>Total Completed Jobs</p>
              <h5>1,210</h5>
            </span>
          </div>
          <div className="col-6 col-md-3 user_data">
            <span><FontAwesomeIcon icon={faBriefcase} className="user_data_icon" /> </span>
            <span>
              <p>Total Cancelled Jobs</p>
              <h5>20</h5>
            </span>
          </div>
        </div>
        <div className="row mt-3">
          <div className="col-12 top_title">
            <h3>Your Recent Job Requests</h3>
            <span><Link to="#">See More</Link></span>
          </div>
          <div className="cards">
            {JobsData && JobsData.filter((item) => {
              return searchWork.toLowerCase() === "" ? item : item.title.toLowerCase().includes(searchWork.toLowerCase());
            }).map((item, key) => {

              return (
                <div className="card" key={key}>
                  <div className="card_top">
                    <span className="profile_info">
                      <span>
                        <img className="prof" src={ProfileImage} alt="profile" />
                      </span>
                      <span>
                        <h4>{item.name}</h4>
                        <img src={Stars} alt="profile" /> <span className="rate_score">4.98</span>
                      </span>
                    </span>
                    <span className="top_cta">
                      <button className="btn active">Saved &nbsp; <FontAwesomeIcon icon={faBookmark} className="icon-saved" /> </button>
                    </span>
                  </div>
                  <div className="duration">
                    <h3>{item.duration} Contract </h3> <span className="time_post">{item.date_posted}</span>
                  </div>
                  <span className="title">
                    <h3>{item.title}</h3>
                  </span>
                  <h4>{item.date}. {item.time}</h4>
                  <span className="address text-truncate">{item.location}</span>
                  <div className="price">
                    <span>
                      <h6>₦{item.amount}/hr</h6>
                      <p>{item.no_of_application} applicant needed</p>
                    </span>
                    <span>
                      <Link to="../jobdetails" className="btn">View Job Details</Link>
                    </span>
                  </div>
                </div>
              )
            })

            }

          </div>
        </div>
        <Postmodal />
      </section>
    </main >
  )
}

export default Main
