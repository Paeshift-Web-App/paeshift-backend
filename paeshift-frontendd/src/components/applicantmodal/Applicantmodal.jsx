import React, { useState, useEffect } from "react";
import Stars from "../../assets/images/stars.png";
import iconWallet from "../../assets/images/wallet.png";
import iconLogo from "../../assets/images/icon-logo.png";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBarsProgress, faLocation, faLocationArrow, faLocationDot } from "@fortawesome/free-solid-svg-icons";
import { faBars } from "@fortawesome/free-solid-svg-icons";
import ProfileImage from "../../assets/images/profile.png"
import "./Applicantmodal.css";


import Axios from "axios";
import { userInfo } from "../../atoms/User.jsx";
import { useRecoilValue, useRecoilState } from "recoil";

import { Formik, Form, Field } from "formik";
import * as Yup from "yup";




const Schema = Yup.object().shape({
    jobtitle: Yup.string().required("Required").min(2, "Too short!").required("Required"),
    jobLocation: Yup.string().required("Required").min(2, "Too short!").required("Required"),
    jobIndustry: Yup.string().required("Required").min(2, "Too short!").required("Required"),
    jobSubCategory: Yup.string().required("Required").min(2, "Too short!").required("Required"),
    jobRate: Yup.string().required("Required").required("Required"),
    noOfApplicants: Yup.string().required("Required").required("Required"),
    jobType: Yup.string().required("Required").required("Required"),
    shiftType: Yup.string().required("Required").required("Required"),
    jobDate: Yup.string().required("Required").required("Required"),
    startTime: Yup.string().required("Required").required("Required"),
    endTime: Yup.string().required("Required").required("Required"),
});






const Applicantmodal = () => {












    return (
        <div className="modal fade come-from-modal right" id="applicantModal" data-bs-backdrop="static" data-bs-keyboard="false" tabIndex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
            <div className="modal-dialog">
                <div className="modal-content">
                    <div className="modal-header border-0">
                        <h1 className="modal-title fs-5" id="staticBackdropLabel">All Applicants</h1>
                        <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div className="modal-body mb-0 pb-0">
                        <div className="title">
                            <h3>Today</h3>
                        </div>
                        <div className="row mt-3 px-3">
                            <div className="col-12 applicants">
                                <div className="card_top">
                                    <span className="profile_info">
                                        <span>
                                            <img className="prof" src={ProfileImage} alt="profile" />
                                        </span>
                                        <span>
                                            <h4>Eniola Lucas</h4>
                                            <img src={Stars} alt="profile" /> <span className="rate_score">4.98</span>
                                        </span>
                                    </span>
                                    <span className="top_cta">
                                        <button className="btn" data-bs-toggle="modal" data-bs-target="#profileModal">View Profile</button>
                                    </span>
                                </div>
                            </div>
                        </div>
                        <div className="title mt-4">
                            <h3>Tomorrow</h3>
                        </div>
                        <div className="row mt-3 px-3">
                            <div className="col-12 applicants">
                                <div className="card_top">
                                    <span className="profile_info">
                                        <span>
                                            <img className="prof" src={ProfileImage} alt="profile" />
                                        </span>
                                        <span>
                                            <h4>Eniola Lucas</h4>
                                            <img src={Stars} alt="profile" /> <span className="rate_score">4.98</span>
                                        </span>
                                    </span>
                                    <span className="top_cta">
                                        <button className="btn" data-bs-toggle="modal" data-bs-target="#profileModal">View Profile</button>
                                    </span>
                                </div>
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

export default Applicantmodal