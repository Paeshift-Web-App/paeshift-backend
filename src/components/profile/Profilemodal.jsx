import React, { useState, useEffect } from "react";
import Stars from "../../assets/images/stars.png";
import { Link, useNavigate } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBell, faBookmark } from "@fortawesome/free-regular-svg-icons";
import { faStar } from "@fortawesome/free-solid-svg-icons";
import Axios from "axios";
import ProfileImage from "../../assets/images/profile.png"
import "./Profilemodal.css";



import { JobsData } from "./JobsData";

const Profilemodal = () => {
  const [toggle, setToggle] = useState(1);


  function updateToggle(id) {
    setToggle(id);
  }



  return (
    <div className="modal fade come-from-modal right" id="profileModal" data-bs-backdrop="static" data-bs-keyboard="false" tabIndex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
      <div className="modal-dialog">
        <div className="modal-content">
          <div className="modal-header border-0">
            <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div className="modal-body py-0">
            <div className="profile_section">
              <div className="row">
                <div className="col-12 text-center">
                  <div className="profile_wrapper">
                    <img className="" src={ProfileImage} alt="profile" />
                  </div>
                  <span className="profile_details mt-1">
                    <h4>Eniola Lucas</h4>
                    <img src={Stars} alt="profile" /> <span className="rate_score">4.98</span>
                  </span>
                </div>
              </div>
            </div>
            <div className="row client_data p-0 m-0">
              <div className="col-4 p-0">
                <h4>24</h4>
                <p>Total Job Posted</p>
              </div>
              <div className="col-4 p-0">
                <h4>3</h4>
                <p>Rating & Reviews</p>
              </div>
              <div className="col-4 p-0">
                <h4>32</h4>
                <p>Applicants Worked With</p>
              </div>
            </div>
            <div className="row tabs m-0 p-0">
              <ul >
                <li className={toggle === 1 ? "profile-btn active" : "profile-btn"} onClick={() => updateToggle(1)}>Jobs Posted</li>
                <li className={toggle === 2 ? "profile-btn active" : "profile-btn"} onClick={() => updateToggle(2)}>Reviews</li>
              </ul>
            </div>
            <div className="row ">
              <div className={toggle === 1 ? "cards jobs active-content" : "cards jobs tab-content"}>
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
              <div className={toggle === 2 ? "reviews active-content" : "reviews tab-content"}>
                {
                  JobsData && JobsData.map((item, key) => {
                    return (
                      <div className="review" key={key}>
                        <div className="ratings">
                          <div className="worker_profile">
                            <span>
                              <img className="prof" src={ProfileImage} alt="profile" />
                            </span>
                            <span>
                              <h4>{item.name}</h4>
                              <p className="rate_score">Professional Grass Cutter</p>
                            </span>
                          </div>
                          <div className="star_ratings">
                            <FontAwesomeIcon icon={faStar} className="rate-icon " />
                            <FontAwesomeIcon icon={faStar} className="rate-icon " />
                            <FontAwesomeIcon icon={faStar} className="rate-icon " />
                            <FontAwesomeIcon icon={faStar} className="rate-icon unrated" />
                            <FontAwesomeIcon icon={faStar} className="rate-icon unrated" />
                          </div>
                        </div>
                        <div className="comment">
                          <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et </p>
                        </div>
                      </div>
                    )
                  })
                }

              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Profilemodal