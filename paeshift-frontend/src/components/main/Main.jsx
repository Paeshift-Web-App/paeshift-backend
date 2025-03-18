import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./Main.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faServer, faUser, faUserGroup, faSearch } from "@fortawesome/free-solid-svg-icons";
import { faBell, faBookmark } from "@fortawesome/free-regular-svg-icons";

import Stars from "../../assets/images/stars.png";
import iconWallet from "../../assets/images/wallet.png";
import iconLogo from "../../assets/images/icon-logo.png";
import Axios from "axios";
import { faBarsProgress } from "@fortawesome/free-solid-svg-icons";
import { faBars } from "@fortawesome/free-solid-svg-icons";
import ProfileImage from "../../assets/images/profile.png";
import Walletmodal from "../walletmodal/Walletmodal";


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
          <h1 className="m-0 p-0">Home</h1>
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
              <input className="form-control searchbar-input" onChange={(e)=> setSearchWork(e.target.value)} type="text" placeholder="Search" aria-label="Search" />
              <FontAwesomeIcon className="search-icon" icon={faSearch} />
            </div>
            <button type="button" className="notification-icon px-3">
              <FontAwesomeIcon className="" icon={faBell} />
            </button>
          </div>
          <button type="button" className="btn btn-wallet px-3" data-bs-toggle="modal" data-bs-target="#walletModal">
            <img src={iconWallet} alt="" srcSet="" /> ₦0.00
          </button>
        </div>
      </div>
      <section className="container container__data">
        <div className="row m-0 p-0">
          <div className="col-12 m-0 p-0">
            <div className="filter-section">
              <button type="button" className="filter-btn active">All</button>
              {/* <button type="button" className="btn filter-btn">Day Shift</button>
              <button type="button" className="btn filter-btn">Night Shift</button> */}
              <select name="shiftType" id="" >
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
                      <Link to="../jobdetails/:id" className="btn">View Job Details</Link>
                    </span>
                  </div>
                </div>
              )
            })

            }

          </div>
        </div>
        <Walletmodal />
      </section>
    </main >
  )
}

export default Main
