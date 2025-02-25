import React, { useState, useEffect } from "react";
import Stars from "../../assets/images/stars.png";
import { Link, useNavigate } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBell, faBookmark } from "@fortawesome/free-regular-svg-icons";
import { faStar } from "@fortawesome/free-solid-svg-icons";
import Axios from "axios";
import ProfileImage from "../../assets/images/profile.png"
import "./Jobrequestmodal.css";



import { JobsData } from "./JobsData";

const Jobrequestmodal = () => {
  const [toggle, setToggle] = useState(1);


  function updateToggle(id) {
    setToggle(id);
  }


  return (
    <div className="modal fade come-from-modal right" id="jobrequestModal" data-bs-backdrop="static" data-bs-keyboard="false" tabIndex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
      <div className="modal-dialog">
        <div className="modal-content">
          <div className="modal-header border-0">
            <h1 className="modal-title fs-5" id="staticBackdropLabel">All Job Requests</h1>
            <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div className="modal-body py-0">
            <div className="row mb-2">
              <div className="col-12 p-2">
                <button type="button" className="btn btn-filter active">All</button>
                <button type="button" className="btn btn-filter">Completed</button>
              </div>
            </div>
            <div className="row ">
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
                          <button className="btn active">No application yet &nbsp; <FontAwesomeIcon icon={faBookmark} className="icon-saved" /> </button>
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
        </div>
      </div>
    </div>
  )
}

export default Jobrequestmodal