import React, { useState, useEffect } from "react";
import Stars from "../../assets/images/stars.png";
import iconWallet from "../../assets/images/wallet.png";
import iconLogo from "../../assets/images/icon-logo.png";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBarsProgress, faCheckDouble, faChevronRight, faLocation, faLocationArrow, faLocationDot } from "@fortawesome/free-solid-svg-icons";
import { faBars } from "@fortawesome/free-solid-svg-icons";
import ProfileImage from "../../assets/images/profile.png"
import "./Notificationmodal.css";


import Axios from "axios";
import { userInfo } from "../../atoms/User.jsx";
import { useRecoilValue, useRecoilState } from "recoil";

import { Formik, Form, Field } from "formik";
import * as Yup from "yup";











const Notificationmodal = () => {












    return (
        <div className="modal fade come-from-modal right" id="notificationModal" data-bs-backdrop="static" data-bs-keyboard="false" tabIndex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
            <div className="modal-dialog">
                <div className="modal-content">
                    <div className="modal-header border-0">
                        <h1 className="modal-title fs-5" id="staticBackdropLabel">Notifications</h1>
                        <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>

                    </div>
                    <div className="modal-body mb-0 pb-0">
                        <div className="row">
                            <div className="col-12">
                                <button type="button" className="btn ">All</button>
                                <button type="button" className="btn ">Read</button>
                            </div>
                        </div>
                        <div className="title">
                            <h3>Today</h3>
                        </div>
                        <div className="row notify_details mb-3">
                            <div className="col-7 labels title">
                                <div className="profile_wrapper">
                                    <img src={iconLogo} alt="" />
                                </div>
                                <p className="m-0" >Job Request Confirmed</p>
                            </div>
                            <div className="col-5 values">
                                <p className="m-0" >Today 8:15 AM</p>
                            </div>
                            <div className="col-12 mt-2 labels message">
                                <p>
                                    Your “Professional Grass Cutter” Shift has been
                                    successfully posted. Ensure your notification
                                    is on so you can be informed
                                    when an applicant apples for the shift.
                                </p>
                            </div>
                            <div className="col-5 labels">
                                <button type="button"> <FontAwesomeIcon icon={faCheckDouble} className="notify_icon" />  Mark as Read</button>
                            </div>
                            <div className="col-7 values">
                                <a href="">View Applicant Details <FontAwesomeIcon icon={faChevronRight} className="notify_icon" /> </a>
                            </div>
                        </div>
                        <div className="row notify_details mb-3">
                            <div className="col-7 labels title">
                                <div className="profile_wrapper">
                                    <img src={ProfileImage} alt="" />
                                </div>
                                <p className="m-0" >Job Request Confirmed</p>
                            </div>
                            <div className="col-5 values">
                                <p className="m-0" >Today 8:15 AM</p>
                            </div>
                            <div className="col-12 mt-2 labels message">
                                <p>
                                    Your “Professional Grass Cutter” Shift has been
                                    successfully posted. Ensure your notification
                                    is on so you can be informed
                                    when an applicant apples for the shift.
                                </p>
                            </div>
                            <div className="col-5 labels">
                                <button type="button"> <FontAwesomeIcon icon={faCheckDouble} className="notify_icon" />  Mark as Read</button>
                            </div>
                            <div className="col-7 values">
                                <a href="">View Applicant Details <FontAwesomeIcon icon={faChevronRight} className="notify_icon" /> </a>
                            </div>
                        </div>


                    </div>
                    <div className="modal-footer border-0">
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Notificationmodal