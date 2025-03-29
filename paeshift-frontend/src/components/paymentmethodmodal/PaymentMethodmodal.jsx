import React, { useState, useEffect } from "react";
import Stars from "../../assets/images/stars.png";
import iconWallet from "../../assets/images/wallet.png";
import iconLogo from "../../assets/images/icon-logo.png";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBarsProgress, faLocation, faLocationArrow, faLocationDot } from "@fortawesome/free-solid-svg-icons";
import { faBars } from "@fortawesome/free-solid-svg-icons";
import flutterLogo from "../../assets/images/flutterwave.png"
import paystackLogo from "../../assets/images/paystack.png"
import "./PaymentMethodmodal.css";


import Axios from "axios";
import { userInfo } from "../../atoms/User.jsx";
import { useRecoilValue, useRecoilState } from "recoil";

import { Formik, Form, Field } from "formik";
import * as Yup from "yup";
import PostJobSuccessmodal from "../postjobsuccessmodal/PostJobSuccessmodal.jsx";




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






const PaymentMethodmodal = () => {




    const initiatePayment = () => {

        useEffect(() => {
            Axios.post(`http://localhost:8000/api/payments/initiate-payment/`)
                .then((response) => {
                    console.log(response.data.jobs);
                })
                .catch((error) => console.error(error));
        }, [])


    }



    const initFlutterWave = () => {
        alert("We are using Flutter Wave");
    }

    const initPayStack = () => {
        alert("We are using Paystack");
        useEffect(() => {
            Axios.post(`http://localhost:8000/api/payments/initiate-payment/`)
                .then((response) => {
                    console.log(response.data.jobs);
                })
                .catch((error) => console.error(error));
        }, [])
    }






    return (
        <div className="modal fade come-from-modal right" id="paymentMethodModal" data-bs-backdrop="static" data-bs-keyboard="false" tabIndex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
            <div className="modal-dialog">
                <div className="modal-content">
                    <div className="modal-header border-0">
                        <h1 className="modal-title fs-5" id="staticBackdropLabel">Choose Payment Method</h1>
                        <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div className="modal-body mb-0 pb-0">
                        <div className="title">
                            <h3> Total Cost: ₦4,200</h3>
                        </div>
                        <div className="row mt-3 px-3">
                            <button type="button" className="payment_btn">
                                <div className="col-12 applicants">
                                    <div className="card_top">
                                        <span>
                                            <img className="prof" src={flutterLogo} alt="profile" />
                                        </span>
                                        <span>
                                            <h3>Flutter Wave</h3>
                                        </span>
                                    </div>
                                </div>
                            </button>
                        </div>
                        <div className="row mt-3 px-3">
                            <button type="button" className="payment_btn" onClick={() => initPayStack()} >
                                <div className="col-12 applicants">
                                    <div className="card_top">
                                        <span>
                                            <img className="prof" src={paystackLogo} alt="profile" />
                                        </span>
                                        <span>
                                            <h3>Pay Stack</h3>
                                        </span>
                                    </div>
                                </div>
                            </button>
                        </div>
                    </div>
                    <div className="modal-footer border-0">
                    </div>
                </div>
            </div>
           
        </div>
    )
}

export default PaymentMethodmodal