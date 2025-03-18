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
import Notificationmodal from "../notificationmodal/Notificationmodal";
import Jobrequestmodal from "../jobrequestsmodal/Jobrequestmodal";
import PaymentMethodmodal from "../paymentmethodmodal/Paymentmethodmodal";


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
            <button type="button" className="notification-icon px-3" data-bs-toggle="modal" data-bs-target="#notificationModal">
              <FontAwesomeIcon className="" icon={faBell} />
            </button>
          </div>
        </div>
      </div>

      <section className="container container__data">

        <div className="row  dashboard_admin_data">
          <div className="col-6 col-md-3 user_data">
            <span><FontAwesomeIcon icon={faCircleUser} className="user_data_icon" /> </span>
            <span>
              <p>Total Workers</p>
              <h5>28</h5>
            </span>
          </div>
          <div className="col-6 col-md-3 user_data">
            <span><FontAwesomeIcon icon={faCircleUser} className="user_data_icon" /> </span>
            <span>
              <p>Active Workers</p>
              <h5>18</h5>
            </span>
          </div>
          <div className="col-6 col-md-3 user_data">
            <span><FontAwesomeIcon icon={faCircleUser} className="user_data_icon" /> </span>
            <span>
              <p>Inactive Workers</p>
              <h5>12</h5>
            </span>
          </div>
          <div className="col-6 col-md-3 user_data">
            <span><FontAwesomeIcon icon={faCircleUser} className="user_data_icon" /> </span>
            <span>
              <p>Suspended Workers</p>
              <h5>20</h5>
            </span>
          </div>
          <div className="col-6 col-md-3 user_data">
            <span><FontAwesomeIcon icon={faCircleUser} className="user_data_icon" /> </span>
            <span>
              <p>Total Clients</p>
              <h5>1,230</h5>
            </span>
          </div>
          <div className="col-6 col-md-3 user_data">
            <span><FontAwesomeIcon icon={faCircleUser} className="user_data_icon" /> </span>
            <span>
              <p>Active Clients</p>
              <h5>28</h5>
            </span>
          </div>
          <div className="col-6 col-md-3 user_data">
            <span><FontAwesomeIcon icon={faCircleUser} className="user_data_icon" /> </span>
            <span>
              <p>Inactive Clients</p>
              <h5>1,210</h5>
            </span>
          </div>
          <div className="col-6 col-md-3 user_data">
            <span><FontAwesomeIcon icon={faCircleUser} className="user_data_icon" /> </span>
            <span>
              <p>Suspended Clients</p>
              <h5>20</h5>
            </span>
          </div>
          <div className="col-6 col-md-3 user_data">
            <span><img src={iconWallet} alt="" srcSet="" className="user_data_icon" /> </span>
            <span>
              <p>Total Amount Received</p>
              <h5>₦1,280,000.00</h5>
            </span>
          </div>
          <div className="col-6 col-md-3 user_data">
            <span><img src={iconWallet} alt="" srcSet="" className="user_data_icon" /> </span>
            <span>
              <p>Total Amount Paid</p>
              <h5>₦128,000.00</h5>
            </span>
          </div>
          <div className="col-6 col-md-3 user_data">
            <span><img src={iconWallet} alt="" srcSet="" className="user_data_icon" /> </span>
            <span>
              <p>Total Income Received</p>
              <h5>₦128,000.00</h5>
            </span>
          </div>
          <div className="col-6 col-md-3 user_data">
            <span><img src={iconWallet} alt="" srcSet="" className="user_data_icon" /> </span>
            <span>
              <p>Total Income Paid</p>
              <h5>₦128,000.00</h5>
            </span>
          </div>
        </div>
        <div className="row mt-3 gap-2 notification_row">
          <div className="col-12 col-md-7 dispute_section">
            <div className="title">
              <h5>Pending Disputes & Notifications</h5>
              <a href="#">View All</a>
            </div>
            <table className="w-100">
              <thead>
                <tr>
                  <th>Pending Dispute</th>
                  <th>Opened Date</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>From Worker ”Jasminxx” to Employer “Esther Grace”</td>
                  <td>Just now</td>
                  <td> <a href="#" className="btn btn-rounded">view Details</a></td>
                </tr>
                <tr>
                  <td>From Employer “Esther Grace” to Worker ”Jasminxx”</td>
                  <td>2 hours ago</td>
                  <td> <a href="#" className="btn btn-rounded">view Details</a></td>
                </tr>
                <tr>
                  <td>From Worker ”Jasminxx” to Employer “Esther Grace”</td>
                  <td>Yesterday, 5 PM</td>
                  <td> <a href="#" className="btn btn-rounded">view Details</a></td>
                </tr>
              </tbody>
            </table>
          </div>
          <div className="col-12 col-md-5 activity_section">
            <div className="title">
              <h5>Recent Activities</h5>
              <a href="#">View Full Log</a>
            </div>
            <div className="recent_activities">
              <div className="activity">
                <span className="profile_data">
                  <div className="image_wrapper">
                    <img src={ProfileImage} alt="User Image" />
                  </div>
                  <span>
                    <span className="username">
                      <h5>John Doe</h5><span>(Just now)</span> <br />
                    </span>
                    <span className="action">Posted a Job Request</span>
                  </span>
                </span>
                <span>
                  <a href="#" className="btn">view</a>
                </span>
              </div>
            </div>

          </div>

        </div>
        <Notificationmodal />

      </section>
    </main >
  )
}

export default Main
