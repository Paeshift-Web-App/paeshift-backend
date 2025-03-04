/* eslint-disable no-unused-vars */
import React, { useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { sidebarRoutes } from "./Sidebarroutes";
import { applicantSidebarRoutes } from "./Sidebarroutes";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCircleArrowLeft, faGear } from "@fortawesome/free-solid-svg-icons";
import brandLogo from "../../assets/images/logo-sm.png";
import ProfileImage from "../../assets/images/profile.png";
import { faArrowRightFromBracket } from "@fortawesome/free-solid-svg-icons";
import { faClose } from "@fortawesome/free-solid-svg-icons/faClose";
import { userInfo } from "../../atoms/User.jsx";
import { useRecoilValue, useRecoilState } from "recoil";
import Axios from "axios";

import "./Sidebar.css";



const Sidebar = () => {
  let user = useRecoilValue(userInfo);

  let [signout, setSignout] = useRecoilState(userInfo);
  let [profile, setProfile] = useState("");

  let redir = useNavigate()

  Axios.get("http://localhost:8000/jobs/whoami")
  .then((response) => {
    // setProfile(response.data);
    console.log(response);
  })
  .catch((error) => console.error(error));

  const handleLogout = () => {
    setSignout({ isLoggedIn: false, data: {} })
    redir("../")
  }
  // console.log(user);
  // console.log(user.data.role);
  return (
    <section className="container_sidebar">
      <nav id="sidebarMenu" className="col-12 col-md-4 col-lg-3 col-xl-2 d-lg-block sidebar collapse p-3 p-md-1 p-lg-3 pt-4" >
        <div className="position-sticky sidebar-sticky bg-white">
          <div className="sidebar-brand">
            <NavLink to="../">
              <img src={brandLogo} className="brand-logo" alt="Paeshift logo" />
            </NavLink>
            <button
              className="navbar-toggler position-absolute d-lg-none collapsed"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#sidebarMenu"
              aria-controls="sidebarMenu"
              aria-expanded="false"
              aria-label="Toggle navigation"
            >
              <FontAwesomeIcon className="icon-close" icon={faClose} />
            </button>
          </div>
          <ul className="nav flex-column mt-4">
            
              {
                sidebarRoutes.map((item, key) => {
                  return (
                    item.title !== "Home" ?
                    <li
                      style={{ display: "block" }}
                      className="nav-item" key={key}>
                      <NavLink
                        className={item.current ? "nav-link active" : "nav-link"}
                        aria-current="page"
                        to={item.to}
                      >
                        {item.icon} {item.title}
                      </NavLink>
                    </li> 
                    : ""

                  );
                }
                )
              }
              {/* {
                user.data.role === "applicant" &&
                applicantSidebarRoutes.map((item, key) => {
                  return (
                    item.title !== "Dashboard" ?
                    <li
                      style={{ display: "block" }}
                      className="nav-item" key={key}>
                      <NavLink
                        className={item.current ? "nav-link active" : "nav-link"}
                        aria-current="page"
                        to={item.to}
                      >
                        {item.icon} {item.title}
                      </NavLink>
                    </li> 
                    : ""

                  );

                }

                )
              } */}
            

          </ul>
          <div className="profile-logout">
            <div className="profile">
              <div className="profile-dp">
                <img src={ProfileImage} alt="profile" />
              </div>
              <div className="profile-info">
                <h2>Eniola Lucas</h2>
                <p>Applicant</p>
              </div>
            </div>
            <ul className="nav flex-column logout-link">
              <li className="nav-item my-2" >
                <NavLink className="nav-link logout" onClick={() => handleLogout()} aria-current="page" to="#" >
                  <FontAwesomeIcon className='me-2' icon={faArrowRightFromBracket} /> <p> Logout</p>
                </NavLink>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </section>
  );
};

export default Sidebar;
