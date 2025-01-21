import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./Settings.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faServer, faUser, faUserGroup, faSearch, faBars, faKey, faBarsProgress, faChevronRight, faUserPen, faWallet, faClipboard, faStar, faCamera, faClose } from "@fortawesome/free-solid-svg-icons";
import { faBell, faBookmark } from "@fortawesome/free-regular-svg-icons";

import Stars from "../../assets/images/stars.png";
import iconWallet from "../../assets/images/wallet.png";
import iconLogo from "../../assets/images/icon-logo.png";
import Axios from "axios";

import ProfileImage from "../../assets/images/profile.png";
import Walletmodal from "../walletmodal/Walletmodal";

import { Formik, Form, Field } from "formik";
import * as Yup from "yup";

import { JobsData } from "./JobsData";



const Schema = Yup.object().shape({
  firstName: Yup.string().required("Required").min(2, "Too short!").required("Required"),
  lastName: Yup.string().required("Required").min(2, "Too short!").required("Required"),
  email: Yup.string().email("Invalid email").required("Required"),
});

const Main = () => {
  // let user = useRecoilValue(userInfo);
  const [activeTab, setActiveTab] = useState(1);
  const [showSlide, setShowSlide] = useState(0);




  return (
    <main className="col-12 col-md-12 col-lg-9 col-xl-10 ms-sm-auto p-0  px-md-2">
      <div className="d-flex justify-content-between align-items-center flex-wrap flex-md-nowrap align-items-center pb-2 ">
        <div className="page_header">
          <h1 className="m-0 p-0">Settings</h1>
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
              <input className="form-control searchbar-input" type="text" placeholder="Search" aria-label="Search" />
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
      <section className="container container__data m-0" id="settings">
        <div className="row m-0 p-4 px-2">
          <div className={showSlide === 1 ? "animate__animated animate__fadeInLeft col-12 col-md-4 col-xl-3 m-0 profile_data show" : "col-12 col-md-4 col-xl-3 m-0 profile_data "}>
            <button className={showSlide === 0 ? "close_btn" : "close_btn hide"} onClick={() => setShowSlide(0)}><FontAwesomeIcon icon={faClose} /> </button>
            <div className="profile_info">
              <span>
                <img className="prof" src={ProfileImage} alt="profile" />
              </span>
              <span>
                <h4>Eniola Lucas</h4>
                <h4 className="rate_score">Worker</h4>
              </span>
            </div>
            <ul className="tabs">
              <li className={activeTab === 1 ? "active" : ""} onClick={() => setActiveTab(1)}>
                <span className="label">
                  <FontAwesomeIcon icon={faUserPen} />
                  <span>Edit Profile</span>
                </span>
                <FontAwesomeIcon icon={faChevronRight} />
              </li>
              <li className={activeTab === 2 ? "active" : ""} onClick={() => setActiveTab(2)}>
                <span className="label">
                  <FontAwesomeIcon icon={faWallet} />
                  <span>Wallet</span>
                </span>
                <FontAwesomeIcon icon={faChevronRight} />
              </li>
              <li className={activeTab === 3 ? "active" : ""} onClick={() => setActiveTab(3)}>
                <span className="label">
                  <FontAwesomeIcon icon={faBookmark} />
                  <span>Saved Jobs</span>
                </span>
                <FontAwesomeIcon icon={faChevronRight} />
              </li>
              <li className={activeTab === 4 ? "active" : ""} onClick={() => setActiveTab(4)}>
                <span className="label">
                  <FontAwesomeIcon icon={faBell} />
                  <span>Notifications</span>
                </span>
                <FontAwesomeIcon icon={faChevronRight} />
              </li>
              <li className={activeTab === 5 ? "active" : ""} onClick={() => setActiveTab(5)}>
                <span className="label">
                  {/* <img src={Stars} alt="" /> */}
                  <FontAwesomeIcon icon={faStar} />
                  <span>Ratings & Reviews</span>
                </span>
                <FontAwesomeIcon icon={faChevronRight} />
              </li>
              <li className={activeTab === 6 ? "active" : ""} onClick={() => setActiveTab(6)}>
                <span className="label">
                  <FontAwesomeIcon icon={faKey} />
                  <span>Login Settings</span>
                </span>
                <FontAwesomeIcon icon={faChevronRight} />
              </li>
              <li className={activeTab === 7 ? "active" : ""} onClick={() => setActiveTab(7)}>
                <span className="label">
                  <FontAwesomeIcon icon={faClipboard} />
                  <span>Feedback</span>
                </span>
                <FontAwesomeIcon icon={faChevronRight} />
              </li>
              <li className={activeTab === 8 ? "active" : ""} onClick={() => setActiveTab(8)}>
                <span className="label">
                  <img src={iconLogo} alt="Paeshift Logo" />
                  <span>About Paeshift</span>
                </span>
                <FontAwesomeIcon icon={faChevronRight} />
              </li>
            </ul>
          </div>
          <div className="col-12 col-md-8 col-xl-9 m-0 px-0 profile_form">
            <button className={showSlide === 0 ? "open_btn" : "open_btn hide"} onClick={() => setShowSlide(1)}><FontAwesomeIcon icon={faChevronRight} /> </button>
            {/* EDIT PROFILE  */}
            <div className={activeTab === 1 ? "tab-content display" : "tab-content"}>
              <h3>Edit Profile</h3>
              <h4>Profile Picture Upload</h4>
              <div className="profile_wrapper">
                <img className="prof" src={ProfileImage} alt="profile" />
              </div>
              <button className="change-image-btn" >
                <FontAwesomeIcon icon={faCamera} /> &nbsp;
                Change Image
              </button>

              <Formik
                initialValues={{
                  firstName: "",
                  lastName: "",
                  email: "",
                }}

                validationSchema={Schema}
                onSubmit={(values) => {
                  // same shape as initial values
                  /**
                   * Steps to create a new user
                   * get data
                   * sed to db in object format
                   */

                  let userdata = {
                    firstName: values.firstName,
                    lastName: values.lastName,
                    email: values.email
                  };

                  console.log(userdata);

                  // swal(<p className="mb-2">Registeration Successful!</p>, 'success', false, 1500)
                  // Endpoint needs to be updated
                  // let baseURL = "https://paeshift-backend.onrender.com/userApi/v1/user/register/";
                  try {
                    // let allUser = await Axios.get(`${baseURL}`);

                    // let isUnique = false;
                    // allUser.data.forEach((each) => {
                    //   if (each.email === values.email) {
                    //     isUnique = true;
                    //   }
                    // });

                    // use the typed email to check if the email already exist

                    // if (!isUnique) {
                    Axios({
                      method: 'post',
                      url: `${baseURL}`,
                      data: userdata,
                      headers: {
                        // 'Access-Control-Allow-Origin': '*',
                        // 'Content-Type': 'application/json',
                        "Access-Control-Allow-Headers": "Content-Type",
                        "Access-Control-Allow-Origin": "https://paeshift-backend.onrender.com",
                        'Content-Type': 'application/json',
                        "Access-Control-Allow-Methods": "OPTIONS,POST"
                      }
                    })
                      .then((response) => {

                        console.log(response);
                        swal("Registeration Successful!", " ", "success", { button: false, timer: 1500 });
                        redir("../signin");
                        // setTimeout(() => {
                        // redir("../signin");
                        // }, 1500);
                      })
                      .catch((error) => {
                        swal("Registeration Failed!", " ", "error", { button: false, timer: 1500 })
                        console.error(error);
                      });

                    // if unique email allow to signup else dont
                  } catch (error) {
                    console.error(error);
                  }
                }
                }
              >
                {({ errors, touched }) => (
                  <Form className="edit_profile_form">
                    <div className="row form_row">
                      <div className="col-12 col-md-6 mb-2">
                        <label htmlFor="firstName" className="form-label mb-0">First Name:</label>
                        <Field name="firstName" className="form-control" placeholder="Eniola" />
                        {/* If this field has been touched, and it contains an error, display it */}
                        {touched.firstName && errors.firstName && (<div className="errors">{errors.firstName}</div>)}
                      </div>
                      <div className="col-12 col-md-6 mb-2">
                        <label htmlFor="lastName" className="form-label mb-0">Last Name:</label>
                        <Field name="lastName" className="form-control" placeholder="Lucas" />
                        {touched.lastName && errors.lastName && (<div className="errors">{errors.lastName}</div>)}
                      </div>
                      <div className="col-12">
                        <label htmlFor="email" className="form-label mb-0">Email:</label>
                        <Field name="email" className="form-control email" placeholder="example@gmail.com" />
                        {touched.email && errors.email && (<div className="errors">{errors.email}</div>)}
                      </div>
                    </div>
                    <button type="submit" name='submit' className="btn save-btn w-100 mt-2">Save Changes</button>
                  </Form>
                )}
              </Formik>
            </div>


            {/* WALLET TAB CONTENT  */}
            <div className={activeTab === 2 ? "tab-content display" : "tab-content"} id="wallet_section">
              <h3>Wallet</h3>
              <div className="balance">
                <h4>Wallet Balance</h4>
                <h1>₦ 23,166.00</h1>
                <p>January 6, 2025 . 11:35 AM</p>
              </div>
              <div className="transactions">
                <div className="top_section">
                  <div><h3>All Transaction</h3></div>
                  <div className="btns-filter">
                    <button className="btn-filter active">All</button>
                    <button className="btn-filter">Today</button>
                    <button className="btn-filter">Yesterday</button>
                    <button className="btn-filter">This Week</button>
                    <button className="btn-filter">Last Week</button>
                    <button className="btn-filter">This Month</button>
                  </div>
                </div>
                <div className="bottom_section">
                  <div className="transaction">
                    <span className="profile_info">
                      <span className="profileWrapper">
                        <img className="prof" src={ProfileImage} alt="profile" />
                      </span>
                      <span>
                        <h4>Eniola Lucas</h4>
                        <p className="date">20 December 2024, 08:24 PM</p>
                      </span>
                    </span>
                    <h3 className="credit-amount">+ #23,400</h3>
                  </div>
                  <div className="transaction">
                    <span className="profile_info">
                      <span className="profileWrapper">
                        <img className="prof" src={iconLogo} alt="profile" />
                      </span>
                      <span>
                        <h4>Platform Fee</h4>
                        <p className="date">20 December 2024, 08:24 PM</p>
                      </span>
                    </span>
                    <h3 className="debit-amount">- #234</h3>
                  </div>
                  <div className="transaction">
                    <span className="profile_info">
                      <span className="profileWrapper">
                        <img className="prof" src={ProfileImage} alt="profile" />
                      </span>
                      <span>
                        <h4>Eniola Lucas</h4>
                        <p className="date">20 December 2024, 08:24 PM</p>
                      </span>
                    </span>
                    <h3 className="credit-amount">+ #23,400</h3>
                  </div>
                  <div className="transaction">
                    <span className="profile_info">
                      <span className="profileWrapper">
                        <img className="prof" src={iconLogo} alt="profile" />
                      </span>
                      <span>
                        <h4>Platform Fee</h4>
                        <p className="date">20 December 2024, 08:24 PM</p>
                      </span>
                    </span>
                    <h3 className="debit-amount">- #234</h3>
                  </div>
                </div>
              </div>
              <button type="button" className="btn withdraw-btn">Withdraw</button>
            </div>



            {/* SAVED JOBS TAB CONTENT  */}
            <div className={activeTab === 3 ? "tab-content display" : "tab-content"}>
              <h3>Saved Jobs</h3>
            <div className="row">
              <div className="cards">

                {JobsData && JobsData.map((item, key) => {

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
            </div>



            {/* NOTIFICATIONS TAB CONTENT  */}
            <div className={activeTab === 4 ? "tab-content display" : "tab-content"}>
              <h3>Notifications</h3>
            </div>




            {/* RATINGS AND REVIEWS TAB CONTENTS  */}
            <div className={activeTab === 5 ? "tab-content display" : "tab-content"}>
              <h3>Rating & Reviews</h3>
            </div>




            {/* LOGIN SETTINGS TAB CONTENTS  */}
            <div className={activeTab === 6 ? "tab-content display" : "tab-content"}>
              <h3>Login Settings</h3>
            </div>



            {/* FEEDBACK TAB CONTENTS  */}
            <div className={activeTab === 7 ? "tab-content display" : "tab-content"}>
              <h3>Feedback</h3>
            </div>






            {/* ABOUT PAESHIFT TAB CONTENT  */}
            <div className={activeTab === 8 ? "tab-content display" : "tab-content"}>
              <h3>About Paeshift</h3>
            </div>
          </div>
        </div>
        <Walletmodal />
      </section>
    </main >
  )
}

export default Main
