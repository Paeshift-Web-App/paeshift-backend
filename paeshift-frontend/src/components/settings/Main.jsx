import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./Settings.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEye, faEyeSlash, faServer, faUser, faUserGroup, faSearch, faBars, faKey, faBarsProgress, faChevronRight, faUserPen, faWallet, faClipboard, faStar, faCamera, faClose, faBookBible, faBook } from "@fortawesome/free-solid-svg-icons";
import { faBell, faBookmark, faCircleXmark } from "@fortawesome/free-regular-svg-icons";

import Stars from "../../assets/images/stars.png";
import iconWallet from "../../assets/images/wallet.png";
import iconStamp from "../../assets/images/paeshiftstamp.png";
import iconWema from "../../assets/images/wemaicon.png";
import iconLogo from "../../assets/images/icon-logo.png";

import ProfileImage from "../../assets/images/profile.png";
import Walletmodal from "../walletmodal/Walletmodal";

import Axios from "axios";
import { userInfo } from "../../atoms/User.jsx";
import { useRecoilValue, useRecoilState } from "recoil";

import { Formik, Form, Field } from "formik";
import * as Yup from "yup";

import { JobsData } from "./JobsData";
import { faFacebook, faInstagram, faTiktok } from "@fortawesome/free-brands-svg-icons";





let id = 0;
export const filterButton = [
  {
    id: id++,
    title: 'All',
    value: ''
  },
  {
    id: id++,
    title: 'Read',
    value: 'read'
  },


]




const Schema = Yup.object().shape({
  firstName: Yup.string().required("Required").min(2, "Too short!").required("Required"),
  feedback: Yup.string().required("Required").min(2, "Too short!").required("Required"),
  lastName: Yup.string().required("Required").min(2, "Too short!").required("Required"),
  email: Yup.string().email("Invalid email").required("Required"),
  newpassword: Yup.string().min(6, "Must Contain 8 Characters").max(50, "Too Long!").required("Required")
    .matches(/^(?=.*[a-z])/, "Must Contain One Lowercase Character")
    .matches(/^(?=.*[A-Z])/, "Must Contain One Uppercase Character")
    .matches(/^(?=.*[0-9])/, "Must Contain One Number Character")
    .matches(/^(?=.*[!@#\$%\^&\*])/, "Must Contain  One Special Case Character"),
  confirmPassword: Yup.string().min(6, "Too Short!").max(50, "Too Long!").required("Required")
    .oneOf([Yup.ref("password"), null], "Passwords must match"),
});

const Main = () => {
  let user = useRecoilValue(userInfo);
  let [profile, setProfile] = useState("");

  let [show, setShow] = useState('password');
  let [show1, setShow1] = useState('password');
  let [show2, setShow2] = useState('password');
  const [activeTab, setActiveTab] = useState(1);
  const [showSlide, setShowSlide] = useState("");


  function openTab(params) {
    setActiveTab(params);
    setShowSlide(0);
  }

  function closeTab() {
    setActiveTab(0);
    setShowSlide(1);
  }

  useEffect(() => {

    Axios.get("http://localhost:8000/jobs/whoami")
      .then((response) => {
        setProfile(response.data);
        console.log(response.data);
      })
      .catch((error) => console.error(error));
    },[])


  // Filter Feature 
  const filterFunction = (e) => {
    const buttons = document.getElementsByClassName('filter-btn');
    setFilterState(e.target.value);
    for (let index = 0; index < buttons.length; index++) {
      buttons[index].classList.remove('active');;
    }
    e.target.classList.add('active');
    // buttons;
  }


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
        <div className="row m-0 p-md-2 px-md-2">
          <div className="col-12 col-md-4 col-xl-3 m-0 py-3 profile_data">
            <div className="profile_info">
              <span>
                <img className="prof" src={ProfileImage} alt="profile" />
              </span>
              <span>
                <h4>{profile.first_name} {profile.last_name}</h4>
                <h4 className="rate_score">{profile.role}</h4>
              </span>
            </div>
            <ul className="tabs">
              {/* <li className={activeTab === 1 ? "active" : ""} onClick={() => {setActiveTab(1)}}> */}
              <li className={activeTab === 1 ? "active" : ""} onClick={() => openTab(1)}>
                <span className="label">
                  <FontAwesomeIcon icon={faUserPen} />
                  <span>Edit Profile</span>
                </span>
                <FontAwesomeIcon icon={faChevronRight} />
              </li>
              {
                user.data.role === "applicant" &&
                <li className={activeTab === 2 ? "active" : ""} onClick={() => openTab(2)}>
                  <span className="label">
                    <FontAwesomeIcon icon={faWallet} />
                    <span>Wallet</span>
                  </span>
                  <FontAwesomeIcon icon={faChevronRight} />
                </li>
              }
              {
                user.data.role === "client" &&
                <li className={activeTab === 9 ? "active" : ""} onClick={() => openTab(9)}>
                  <span className="label">
                    <FontAwesomeIcon icon={faBook} />
                    <span>Invoice</span>
                  </span>
                  <FontAwesomeIcon icon={faChevronRight} />
                </li>
              }
              <li className={activeTab === 3 ? "active" : ""} onClick={() => openTab(3)}>
                <span className="label">
                  <FontAwesomeIcon icon={faBookmark} />
                  <span>Saved Jobs</span>
                </span>
                <FontAwesomeIcon icon={faChevronRight} />
              </li>
              <li className={activeTab === 4 ? "active" : ""} onClick={() => openTab(4)}>
                <span className="label">
                  <FontAwesomeIcon icon={faBell} />
                  <span>Notifications</span>
                </span>
                <FontAwesomeIcon icon={faChevronRight} />
              </li>
              <li className={activeTab === 5 ? "active" : ""} onClick={() => openTab(5)}>
                <span className="label">
                  {/* <img src={Stars} alt="" /> */}
                  <FontAwesomeIcon icon={faStar} />
                  <span>Ratings & Reviews</span>
                </span>
                <FontAwesomeIcon icon={faChevronRight} />
              </li>
              <li className={activeTab === 6 ? "active" : ""} onClick={() => openTab(6)}>
                <span className="label">
                  <FontAwesomeIcon icon={faKey} />
                  <span>Login Settings</span>
                </span>
                <FontAwesomeIcon icon={faChevronRight} />
              </li>
              <li className={activeTab === 7 ? "active" : ""} onClick={() => openTab(7)}>
                <span className="label">
                  <FontAwesomeIcon icon={faClipboard} />
                  <span>Feedback</span>
                </span>
                <FontAwesomeIcon icon={faChevronRight} />
              </li>
              <li className={activeTab === 8 ? "active" : ""} onClick={() => openTab(8)}>
                <span className="label">
                  <img src={iconLogo} alt="Paeshift Logo" />
                  <span>About Paeshift</span>
                </span>
                <FontAwesomeIcon icon={faChevronRight} />
              </li>
            </ul>
          </div>
          <div className={showSlide === 0 ? "animate__animated animate__fadeIn col-12 col-md-8 col-xl-9 m-0  p-2 py-3 profile_form" : "col-12 col-md-8 col-xl-9 m-0 px-0 profile_form hide"}>
            {/* <div className={"col-12 col-md-8 col-xl-9 m-0 px-0 profile_form"}> */}
            <button className="close_btn" onClick={closeTab}><FontAwesomeIcon icon={faCircleXmark} className="close_icon" /> </button>


            {/* EDIT PROFILE  */}
            <div className={activeTab === 1 ? "animate__animated animate__fadeInRight tab-content display" : "tab-content"} id="profile">
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
                        "Access-Control-Allow-Origin": "*",
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
            <div className={activeTab === 2 ? "animate__animated animate__fadeInRight tab-content display" : "tab-content"} id="wallet_section">
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
                    <button className="btn-filter">This_Week</button>
                    <button className="btn-filter">Last_Week</button>
                    <button className="btn-filter">This_Month</button>
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


            {/* Invoice TAB CONTENT  */}
            <div className={activeTab === 9 ? "animate__animated animate__fadeInRight tab-content display" : "tab-content"} id="invoice_section">
              <h3>Invoice</h3>

              <div className="transactions">
                <div className="top_section">
                  <div className="btns-filter">
                    <button className="btn-filter active">All</button>
                    <button className="btn-filter">Today</button>
                    <button className="btn-filter">Yesterday</button>
                    <button className="btn-filter">This_Week</button>
                    <button className="btn-filter">Last_Week</button>
                    <button className="btn-filter">This_Month</button>
                  </div>
                </div>
                <div className="bottom_section">
                  <div className="transaction">
                    <span className="profile_info">
                      <span className="profileWrapper">
                        <img className="prof" src={iconWema} alt="profile" />
                      </span>
                      <span>
                        <h4>Eniola Lucas</h4>
                        <p className="date">20 December 2024, 08:24 PM</p>
                      </span>
                    </span>
                    <h3 className="credit-amount">#23,400</h3>
                  </div>
                  <div className="transaction">
                    <span className="profile_info">
                      <span className="profileWrapper">
                        <img className="prof" src={iconWema} alt="profile" />
                      </span>
                      <span>
                        <h4>Eniola Lucas</h4>
                        <p className="date">20 December 2024, 08:24 PM</p>
                      </span>
                    </span>
                    <h3 className="credit-amount">#23,400</h3>
                  </div>
                  <div className="transaction">
                    <span className="profile_info">
                      <span className="profileWrapper">
                        <img className="prof" src={iconWema} alt="profile" />
                      </span>
                      <span>
                        <h4>Eniola Lucas</h4>
                        <p className="date">20 December 2024, 08:24 PM</p>
                      </span>
                    </span>
                    <h3 className="credit-amount">#23,400</h3>
                  </div>
                  <div className="transaction">
                    <span className="profile_info">
                      <span className="profileWrapper">
                        <img className="prof" src={iconWema} alt="profile" />
                      </span>
                      <span>
                        <h4>Eniola Lucas</h4>
                        <p className="date">20 December 2024, 08:24 PM</p>
                      </span>
                    </span>
                    <h3 className="credit-amount">#23,400</h3>
                  </div>
                  <div className="transaction">
                    <span className="profile_info">
                      <span className="profileWrapper">
                        <img className="prof" src={iconWema} alt="profile" />
                      </span>
                      <span>
                        <h4>Eniola Lucas</h4>
                        <p className="date">20 December 2024, 08:24 PM</p>
                      </span>
                    </span>
                    <h3 className="credit-amount">#23,400</h3>
                  </div>
                </div>
              </div>
              {/* <button type="button" className="btn withdraw-btn">Save Changes</button> */}
            </div>


            {/* SAVED JOBS TAB CONTENT  */}
            <div className={activeTab === 3 ? "animate__animated animate__fadeInRight tab-content display" : "tab-content"} id="saved_jobs">
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
                            <button className="btn active">Remove &nbsp; <FontAwesomeIcon icon={faCircleXmark} className="icon-saved" /> </button>
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
            <div className={activeTab === 4 ? "animate__animated animate__fadeInRight tab-content display" : "tab-content"} id="notification">
              <h3>Notifications</h3>
              <h4>Set your push notification preferences</h4>
              <form action="" className="notification_form">
                <div className="row notifications">
                  <div className="col-12 notification">
                    <span>
                      <h4>New Job alert</h4>
                      <label className="form-check-label" htmlFor="notify-switch">Receive push notification for all new job alert</label>
                    </span>
                    <div className="form-check form-switch">
                      <input className="form-check-input" type="checkbox" role="switch" id="notify-switch" defaultChecked />
                    </div>
                  </div>
                  <div className="col-12 notification">
                    <span>
                      <h4>Job Reminder</h4>
                      <label className="form-check-label" htmlFor="notify-switch1">Receive push notification for all new job reminder</label>
                    </span>
                    <div className="form-check form-switch">
                      <input className="form-check-input" type="checkbox" role="switch" id="notify-switch1" />
                    </div>
                  </div>
                  <div className="col-12 notification">
                    <span>
                      <h4>Job Request Acceptance</h4>
                      <label className="form-check-label" htmlFor="notify-switch2">Receive push notification for all accepted job requests</label>
                    </span>
                    <div className="form-check form-switch">
                      <input className="form-check-input" type="checkbox" role="switch" id="notify-switch2" />
                    </div>
                  </div>
                  <div className="col-12 notification">
                    <span>
                      <h4>Settings</h4>
                      <label className="form-check-label" htmlFor="notify-switch3">Receive push notification for all settings changes</label>
                    </span>
                    <div className="form-check form-switch">
                      <input className="form-check-input" type="checkbox" role="switch" id="notify-switch3" defaultChecked />
                    </div>
                  </div>
                </div>
                <h4>Set your email notification preferences</h4>
                <div className="row notifications">
                  <div className="col-12 notification">
                    <span>
                      <h4>New Job alert</h4>
                      <label className="form-check-label" htmlFor="notify-switch4">Receive email notification for all  new job alert</label>
                    </span>
                    <div className="form-check form-switch">
                      <input className="form-check-input" type="checkbox" role="switch" id="notify-switch4" />
                    </div>
                  </div>
                  <div className="col-12 notification">
                    <span>
                      <h4>Job Reminder</h4>
                      <label className="form-check-label" htmlFor="notify-switch5">Receive email notification for all new job reminder</label>
                    </span>
                    <div className="form-check form-switch">
                      <input className="form-check-input" type="checkbox" role="switch" id="notify-switch5" defaultChecked />
                    </div>
                  </div>
                  <div className="col-12 notification">
                    <span>
                      <h4>Job Request Acceptance</h4>
                      <label className="form-check-label" htmlFor="notify-switch6">Receive email notification for all accepted job requests</label>
                    </span>
                    <div className="form-check form-switch">
                      <input className="form-check-input" type="checkbox" role="switch" id="notify-switch6" />
                    </div>
                  </div>
                  <div className="col-12 notification">
                    <span>
                      <h4>Settings</h4>
                      <label className="form-check-label" htmlFor="notify-switch7">Receive email notification for all settings changes</label>
                    </span>
                    <div className="form-check form-switch">
                      <input className="form-check-input" type="checkbox" role="switch" id="notify-switch7" defaultChecked />
                    </div>
                  </div>
                </div>
                <button type="submit" name='submit' className="btn btn-save w-100 mt-2">Save Changes</button>
              </form>
            </div>


            {/* RATINGS AND REVIEWS TAB CONTENTS  */}
            <div className={activeTab === 5 ? "animate__animated animate__fadeInRight tab-content display" : "tab-content"} id="reviews">
              <h3>Rating & Reviews</h3>
              <div className="row m-0 p-0">
                <div className="col-12 m-0 p-0">
                  <div className="filter-section">
                    {
                      filterButton.map((item, key) => {
                        return (
                          <button type="button" key={key} value={item.value} onClick={filterFunction} className={item.title === "All" ? "filter-btn active" : "filter-btn"}>{item.title}</button>
                        )
                      })
                    }

                  </div>
                </div>
              </div>
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
                              <span className="rate_score">Professional Grass Cutter</span>
                            </span>
                          </span>
                          <span className="top_cta">
                            <FontAwesomeIcon icon={faStar} className="icon-saved" />
                            <FontAwesomeIcon icon={faStar} className="icon-saved" />
                            <FontAwesomeIcon icon={faStar} className="icon-saved" />
                            <FontAwesomeIcon icon={faStar} className="icon-saved light" />
                            <FontAwesomeIcon icon={faStar} className="icon-saved light" />
                          </span>
                        </div>
                        <span className="review">{item.review}</span>
                        <div className="button">
                          <Link to="../jobdetails" className="btn w-100">Mark as Read</Link>
                        </div>
                      </div>
                    )
                  })

                  }

                </div>
              </div>
            </div>


            {/* LOGIN SETTINGS TAB CONTENTS  */}
            <div className={activeTab === 6 ? "animate__animated animate__fadeInRight tab-content display" : "tab-content"} id="login_settings">
              <h3>Login Settings</h3>
              <div className="row">
                <div className="col-12">
                  <div className="accordion" id="accordionExample">
                    <div className="accordion-item">
                      <h2 className="accordion-header">
                        <button className="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOn" aria-expanded="true" aria-controls="collapseOn">
                          <h4>Change Password</h4>
                        </button>
                      </h2>
                      <div id="collapseOn" className="accordion-collapse collapse show" data-bs-parent="#accordionExample">
                        <div className="accordion-body p-2">
                          <Formik
                            initialValues={{
                              oldpassword: "",
                              newpassword: "",
                              confirmPassword: "",
                            }}

                            validationSchema={Schema}
                            onSubmit={async (values) => {
                              // same shape as initial values
                              /**
                               * Steps to create a new user
                               * get data
                               * sed to db in object format
                               */

                              let userdata = {
                                oldpassword: values.email,
                                password: values.password,
                                password2: values.confirmPassword,
                              };

                              // console.log(userdata);

                              // swal(<p className="mb-2">Registeration Successful!</p>, 'success', false, 1500)
                              // Endpoint needs to be updated
                              // let baseURL = "https://paeshift-backend.onrender.com/userApi/v1/user/register/";
                              // try {
                              //   // let allUser = await Axios.get(`${baseURL}`);

                              //   // let isUnique = false;
                              //   // allUser.data.forEach((each) => {
                              //   //   if (each.email === values.email) {
                              //   //     isUnique = true;
                              //   //   }
                              //   // });


                              //   // setInterval(() => {
                              //   //   AppSwal.showLoading()
                              //   // }, 1000);

                              //   // use the typed email to check if the email already exist
                              //   // if (!isUnique) {
                              //   await Axios({
                              //     method: 'post',
                              //     url: `${baseURL}`,
                              //     // url: "https://paeshift-backend.onrender.com/userApi/v1/user/register/",
                              //     data: userdata
                              //   })
                              //     .then((response) => {
                              //       console.log(response);
                              //       swal("Password Changed Successful!", " ", "success", { button: false, timer: 1500 });
                              //       redir("../signin");
                              //       // setTimeout(() => {
                              //       // redir("../signin");
                              //       // }, 1500);
                              //     })
                              //     .catch((error) => {
                              //       swal("Action Failed!", " ", "error", { button: false, timer: 1500 })
                              //       console.error(error.message);
                              //     });

                              //   // if unique email allow to signup else dont
                              // } catch (error) {
                              //   console.error(error);
                              // }
                            }
                            }
                          >
                            {({ errors, touched }) => (
                              <Form className="form_settings">
                                <div className="mb-2">
                                  <span className="visibility">
                                    <Field type={show} name="oldpassword" id="oldpassword" className="form-control" placeholder="Old Password" />
                                    <FontAwesomeIcon icon={show === "password" ? faEye : faEyeSlash} onClick={() => setShow(show === "password" ? "text" : "password")} className='eye-icon' />
                                  </span>
                                  {touched.oldpassword && errors.oldpassword && (<div className="errors">{errors.oldpassword}</div>)}
                                </div>
                                <div className="mb-2">
                                  <span className="visibility">
                                    <Field type={show1} name="newpassword" id="password" className="form-control" placeholder="New Password" />
                                    <FontAwesomeIcon icon={show1 === "password" ? faEye : faEyeSlash} onClick={() => setShow1(show1 === "password" ? "text" : "password")} className='eye-icon' />
                                  </span>
                                  {touched.newpassword && errors.newpassword && (<div className="errors">{errors.newpassword}</div>)}
                                </div>
                                <div className="mb-2" >
                                  <span className="visibility">
                                    <Field type={show2} name="confirmPassword" id="confirmPassword" className="form-control" placeholder="Confirm Password" />
                                    <FontAwesomeIcon icon={show2 === "password" ? faEye : faEyeSlash} onClick={() => setShow2(show2 === "password" ? "text" : "password")} className='eye-icon' />
                                  </span>
                                  {touched.confirmPassword && errors.confirmPassword && (<div className="errors">{errors.confirmPassword}</div>)}
                                </div>
                                <button type="submit" name='submit' className="btn btn-lg primary-btn w-100 mt-2">Save Changes</button>

                              </Form>
                            )}
                          </Formik>
                        </div>
                      </div>
                    </div>
                  
                  </div>

                </div>
              </div>
            </div>



            {/* FEEDBACK TAB CONTENTS  */}
            <div className={activeTab === 7 ? "animate__animated animate__fadeInRight tab-content display" : "tab-content"} id="feedback">
              <h3>Feedback</h3>
              <div className="row">
                <div className="col-12">
                  <img src={iconStamp} alt="Paeshift Feedback Icon" className="brand_stamp" />
                </div>
                <div className="col-12">
                  <h2>Paeshift wants your feedback</h2>
                  <Formik
                    initialValues={{
                      firstName: "",
                      lastName: "",
                      email: "",
                      password: "",
                      confirmPassword: "",
                    }}

                    validationSchema={Schema}
                    onSubmit={async (values) => {
                      // same shape as initial values
                      /**
                       * Steps to create a new user
                       * get data
                       * sed to db in object format
                       */

                      let userdata = {
                        firstName: values.firstName,
                        lastName: values.lastName,
                        email: values.email,
                        password: values.password,
                        password2: values.confirmPassword,
                      };

                      // console.log(userdata);

                      // swal(<p className="mb-2">Registeration Successful!</p>, 'success', false, 1500)
                      // Endpoint needs to be updated
                      // let baseURL = "https://paeshift-backend.onrender.com/userApi/v1/user/register/";
                      // try {
                      //   // let allUser = await Axios.get(`${baseURL}`);

                      //   // let isUnique = false;
                      //   // allUser.data.forEach((each) => {
                      //   //   if (each.email === values.email) {
                      //   //     isUnique = true;
                      //   //   }
                      //   // });


                      //   // setInterval(() => {
                      //   //   AppSwal.showLoading()
                      //   // }, 1000);

                      //   // use the typed email to check if the email already exist
                      //   // if (!isUnique) {
                      //   await Axios({
                      //     method: 'post',
                      //     url: `${baseURL}`,
                      //     // url: "https://paeshift-backend.onrender.com/userApi/v1/user/register/",
                      //     data: userdata
                      //   })
                      //     .then((response) => {
                      //       console.log(response);
                      //       swal("Registeration Successful!", " ", "success", { button: false, timer: 1500 });
                      //       redir("../signin");
                      //       // setTimeout(() => {
                      //       // redir("../signin");
                      //       // }, 1500);
                      //     })
                      //     .catch((error) => {
                      //       swal("Registeration Failed!", " ", "error", { button: false, timer: 1500 })
                      //       console.error(error.message);
                      //     });

                      //   // if unique email allow to signup else dont
                      // } catch (error) {
                      //   console.error(error);
                      // }
                    }
                    }
                  >
                    {({ errors, touched }) => (
                      <Form className="form_settings" >
                        <div className="my-2">
                          <Field name="feedback" className="form-control" as="textarea" placeholder="We'd love to hear from you" />
                          {/* If this field has been touched, and it contains an error, display it */}
                          {touched.feedback && errors.feedback && (<div className="errors">{errors.feedback}</div>)}
                        </div>
                        <button type="submit" name='submit' className="btn btn-lg primary-btn w-100 mt-2">Submit</button>
                      </Form>
                    )}
                  </Formik>
                </div>
              </div>
            </div>


            {/* ABOUT PAESHIFT TAB CONTENT  */}
            <div className={activeTab === 8 ? "animate__animated animate__fadeInRight tab-content display" : "tab-content"} id="about_paeshift">
              <h3>About Paeshift</h3>
              <div className="row">
                <div className="col-12">
                  <div className="accordion" id="accordionExample2">
                    <div className="accordion-item">
                      <h2 className="accordion-header">
                        <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne" aria-expanded="false" aria-controls="collapseOne">
                          <h4>Privacy Policy</h4>
                        </button>
                      </h2>
                      <div id="collapseOne" className="accordion-collapse collapse" data-bs-parent="#accordionExample2">
                        <div className="accordion-body">
                          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                        </div>
                      </div>
                    </div>
                    <div className="accordion-item">
                      <h2 className="accordion-header">
                        <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
                          <h4>Terms & Condition</h4>
                        </button>
                      </h2>
                      <div id="collapseTwo" className="accordion-collapse collapse" data-bs-parent="#accordionExample2">
                        <div className="accordion-body">
                          Terms dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                        </div>
                      </div>
                    </div>
                    <div className="accordion-item">
                      <h2 className="accordion-header">
                        <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseThree" aria-expanded="false" aria-controls="collapseThree">
                          <h4>Social Media</h4>
                        </button>
                      </h2>
                      <div id="collapseThree" className="accordion-collapse collapse" data-bs-parent="#accordionExample2">
                        <div className="accordion-body">
                          <a href="#"> <FontAwesomeIcon icon={faInstagram}/> <span className="text-dark">Instagram</span> <FontAwesomeIcon className="socialmedia-icon" icon={faChevronRight} /></a>
                          <br />
                          <a href="#"> <FontAwesomeIcon icon={faFacebook}/> <span className="text-dark">Facebook</span>  <FontAwesomeIcon className="socialmedia-icon" icon={faChevronRight} /></a>
                          <br />
                          <a href="#"> <FontAwesomeIcon icon={faTiktok}/> <span className="text-dark">Tiktok</span>  <FontAwesomeIcon className="socialmedia-icon" icon={faChevronRight} /></a>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <Walletmodal />
      </section>
    </main >
  )
}

export default Main
