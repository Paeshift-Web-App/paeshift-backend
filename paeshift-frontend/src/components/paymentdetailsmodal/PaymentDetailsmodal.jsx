import React, { useState, useEffect } from "react";
import Stars from "../../assets/images/stars.png";
import iconWallet from "../../assets/images/wallet.png";
import iconLogo from "../../assets/images/icon-logo.png";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBarsProgress, faLocation, faLocationArrow, faLocationDot } from "@fortawesome/free-solid-svg-icons";
import { faBars } from "@fortawesome/free-solid-svg-icons";
import ProfileImage from "../../assets/images/profile.png"
import "./PaymentDetailsmodal.css";


import Axios from "axios";
import { userInfo } from "../../atoms/User.jsx";
import { useRecoilValue, useRecoilState } from "recoil";

import { Formik, Form, Field } from "formik";
import * as Yup from "yup";


const PaymentDetailsmodal = () => {












    return (
        <div className="modal fade come-from-modal right" id="paymentDetailsModal" data-bs-backdrop="static" data-bs-keyboard="false" tabIndex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
            <div className="modal-dialog">
                <div className="modal-content">
                    <div className="modal-header border-0">
                        <h1 className="modal-title fs-5" id="staticBackdropLabel">Payment Detail <span className="success">Successful</span></h1>
                        <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div className="modal-body mb-0 pb-0">
                        <div className="row">

                        </div>
                        {/* <div className="title">
                            <h3>Let’s start with a main details</h3>
                        </div> */}
                        <div className="title">
                            <h3>Transaction Details</h3>
                        </div>
                        <div className="row px-3 trans_details mb-3">
                            <div className="col-6 labels">
                                <p>Transaction ID:</p> 
                            </div>
                            <div className="col-6 values">
                                <p>JR4257-09-011</p> 
                            </div>
                            <div className="col-3 labels">
                               <p>Date:</p> 
                            </div>
                            <div className="col-9 values">
                               <p>Saturday 2nd March, 2024.</p> 
                            </div>
                            <div className="col-6 labels">
                               <p>Time:</p> 
                            </div>
                            <div className="col-6 values">
                               <p>09:00 AM.</p>
                            </div>
                            <div className="col-7 labels">
                                <p>Service Charged:</p> 
                            </div>
                            <div className="col-5 values">
                                <p>₦4,000.00</p>
                            </div>
                            <div className="col-7 labels">
                                <p>Platform Fee:</p>
                            </div>
                            <div className="col-5 values">
                                <p>₦200.00</p>
                            </div>
                            <div className="col-7 labels">
                                <p>Total:</p>
                            </div>
                            <div className="col-5 values">
                                <p className="text-success" >₦4,200.00</p>
                            </div>
                        </div>
                        <div className="title">
                            <h3>Job Details</h3>
                        </div>
                        <div className="row px-3 trans_details mb-3">
                            <div className="col-3 labels">
                                <p>Title:</p>
                            </div>
                            <div className="col-9 values">
                                <p>Professional Grass Cutter</p>
                            </div>
                            <div className="col-3 labels">
                                <p>Date:</p>
                            </div>
                            <div className="col-9 values">
                                <p>Monday 2nd March, 2024.</p>
                            </div>
                            <div className="col-6 labels">
                                <p>Start Time:</p>
                            </div>
                            <div className="col-6 values">
                                <p>09:00 AM.</p>
                            </div>
                            <div className="col-6 labels">
                                <p>End Time:</p>
                            </div>
                            <div className="col-6 values">
                                <p>11:00 AM.</p>
                            </div>
                            <div className="col-8 labels">
                                <p>Contract Duration:</p>
                            </div>
                            <div className="col-4 values">
                                <p>2hrs</p>
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

export default PaymentDetailsmodal