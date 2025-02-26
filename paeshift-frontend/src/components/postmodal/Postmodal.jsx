import React, { useState, useEffect } from "react";
import Stars from "../../assets/images/stars.png";
import iconWallet from "../../assets/images/wallet.png";
import iconLogo from "../../assets/images/icon-logo.png";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBarsProgress, faLocation, faLocationArrow, faLocationDot } from "@fortawesome/free-solid-svg-icons";
import { faBars } from "@fortawesome/free-solid-svg-icons";
import ProfileImage from "../../assets/images/profile.png"
import "./Postmodal.css";


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






const Postmodal = () => {












    return (
        <div className="modal fade come-from-modal right" id="postModal" data-bs-backdrop="static" data-bs-keyboard="false" tabIndex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
            <div className="modal-dialog">
                <div className="modal-content">
                    <div className="modal-header border-0">
                        <h1 className="modal-title fs-5" id="staticBackdropLabel">Create Job Request</h1>
                        <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div className="modal-body mb-0 pb-0">
                        <div className="title">
                            <span>1/2</span>
                            <h3>Let’s start with a main details</h3>
                            <p>This will help your job posts stand out to the right applicants</p>
                        </div>


                        <Formik
                            initialValues={{
                                jobtitle: "",
                                jobLocation: "",
                                jobIndustry: "",
                                jobSubCategory: "",
                                jobRate: "",
                                noOfApplicants: "",
                                jobType: "",
                                shiftType: "",
                                jobDate: "",
                                startTime: "",
                                endTime: "",
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
                                    jobtitle: values.jobtitle,
                                    location: values.jobLocation,
                                    industry: values.jobIndustry,
                                    sub_category: values.jobSubCategory,
                                    rate: values.jobRate,
                                    no_of_applicants: values.noOfApplicants,
                                    job_type: values.jobType,
                                    shift_type: values.shiftType,
                                    job_date: values.jobDate,
                                    end_time: values.startTime,
                                    endTime: values.endTime,
                                };

                                console.log(userdata);
                                // try {
                                 
            
                                //     // use the typed email to check if the email already exist
                                //     let result = await Axios.post("http://127.0.0.1:8000/create-job", userdata);
                                //     result = result.data.message;
            
            
                                //     if (result === "success") {
                                //         swal("Job Created Successful!", " ", "success", { button: false, timer: 1500 });
                                //         redir("../signin");
                                //     }
                                //     else {
                                //         swal("Job Creation Failed!", " ", "error", { button: false, timer: 1500 })
                                //     }
            
                                 
                                //   // if unique email allow to signup else dont
                                // } catch (error) {
                                //   console.error(error);
                                // }
                                // swal(<p className="mb-2">Registeration Successful!</p>, 'success', false, 1500)
                                // Endpoint needs to be updated
                                // let baseURL = "https://paeshift-backend.onrender.com/userApi/v1/user/register/";
                                // try {
                                //     // let allUser = await Axios.get(`${baseURL}`);

                                //     // let isUnique = false;
                                //     // allUser.data.forEach((each) => {
                                //     //   if (each.email === values.email) {
                                //     //     isUnique = true;
                                //     //   }
                                //     // });

                                //     // use the typed email to check if the email already exist

                                //     // if (!isUnique) {
                                //     Axios({
                                //         method: 'post',
                                //         url: `${baseURL}`,
                                //         data: userdata,
                                //         headers: {
                                //             // 'Access-Control-Allow-Origin': '*',
                                //             // 'Content-Type': 'application/json',
                                //             "Access-Control-Allow-Headers": "Content-Type",
                                //             "Access-Control-Allow-Origin": "https://paeshift-backend.onrender.com",
                                //             'Content-Type': 'application/json',
                                //             "Access-Control-Allow-Methods": "OPTIONS,POST"
                                //         }
                                //     })
                                //         .then((response) => {

                                //             console.log(response);
                                //             swal("Registeration Successful!", " ", "success", { button: false, timer: 1500 });
                                //             redir("../signin");
                                //             // setTimeout(() => {
                                //             // redir("../signin");
                                //             // }, 1500);
                                //         })
                                //         .catch((error) => {


                                //             console.error(error);
                                //         });

                                //     // if unique email allow to signup else dont
                                // } catch (error) {
                                //     console.error(error);
                                // }
                            }
                            }
                        >
                            {({ errors, touched }) => (
                                <Form className="post_form" id="post_form">
                                    <div className="row form_row">
                                        <div className="col-12 col-md-6 mb-2">
                                            <label htmlFor="jobtitle" className="form-label mb-0">Write a title for your Job</label>
                                            <Field name="jobtitle" className="form-control" placeholder="30 letters Max" />
                                            {/* If this field has been touched, and it contains an error, display it */}
                                            {touched.jobtitle && errors.jobtitle && (<div className="errors">{errors.jobtitle}</div>)}
                                        </div>
                                        <div className="col-12 col-md-6 mb-2">
                                            <label htmlFor="jobLocation" className="form-label mb-0">Where the job take place?</label>
                                            <span className="location">
                                                <Field name="jobLocation" id="jobLocation" className="form-control" placeholder="Location" />
                                                <FontAwesomeIcon icon={faLocationDot} className='location-icon' />
                                            </span>
                                            {touched.jobLocation && errors.jobLocation && (<div className="errors">{errors.jobLocation}</div>)}
                                        </div>
                                        <div className="col-12 mb-2">
                                            <label htmlFor="jobIndustry" className="form-label mb-0">Job Industry</label>
                                            <button> </button>
                                            <Field as="select" name="jobIndustry" id="jobIndustry" className="form-control" placeholder="">
                                                <option value="">Select Job industry</option>
                                                <option value="General Handyman">General Handyman</option>
                                                <option value="Hospitality">Hospitality</option>
                                                <option value="Tv & Accessories">Tv & Accessories</option>
                                                <option value="Electrical">Electrical</option>
                                            </Field>
                                            {touched.jobIndustry && errors.jobIndustry && (<div className="errors">{errors.jobIndustry}</div>)}
                                        </div>
                                        <div className="col-12 mb-2">
                                            <label htmlFor="jobSubCategory" className="form-label mb-0">Sub Category (select at most 6)</label>
                                            <Field as="select" name="jobSubCategory" id="jobSubCategory" className="form-control" placeholder="" >
                                                <option value="">Select the sub category of the job industry</option>
                                                <option value="Air Conditioner Installation">Air Conditioner Installation</option>
                                                <option value="Furniture Assembly">Furniture Assembly</option>
                                                <option value="Home Repair Services">Home Repair Services</option>
                                                <option value="Locks Installation">Locks Installation</option>
                                            </Field>
                                            {touched.jobSubCategory && errors.jobSubCategory && (<div className="errors">{errors.jobSubCategory}</div>)}
                                        </div>
                                        <div className="row m-0 mb-2 p-0">
                                            <div className="col-6 form-group">
                                                <label htmlFor="jobRate" className="form-label mb-0">Job rate per hour</label>
                                                <Field type="number" id="jobRate" name="jobRate" className="form-control" placeholder="" />
                                                {touched.jobRate && errors.jobRate && (<div className="errors">{errors.jobRate}</div>)}
                                            </div>
                                            <div className="col-6">
                                                <label htmlFor="noOfApplicants" className="form-label mb-0">Applicant Needed</label>
                                                <Field type="number" id="noOfApplicants" name="noOfApplicants" className="form-control" placeholder="" />
                                                {touched.noOfApplicants && errors.noOfApplicants && (<div className="errors">{errors.noOfApplicants}</div>)}
                                            </div>
                                        </div>

                                        <div className="title">
                                            <span>2/2</span>
                                            <h3>Estimate the Timeline/Scope of your job</h3>
                                            <p>This information helps us recommend to the right applicant for what job you need.</p>
                                        </div>

                                        <div className="row m-0 mb-2 p-0">
                                            <div className="col-6">
                                                <label htmlFor="jobType" className="form-label mb-0">Type of Job</label>
                                                <Field as="select" name="jobType" id="jobType" className="form-control" placeholder="" >
                                                    <option value="">Select job type</option>
                                                    <option value="1">A day job</option>
                                                    <option value="2">Multiple</option>
                                                </Field>
                                                {touched.jobType && errors.jobType && (<div className="errors">{errors.jobType}</div>)}
                                            </div>
                                            <div className="col-6">
                                                <label htmlFor="shiftType" className="form-label mb-0">Type of Shift</label>
                                                <Field as="select" name="shiftType" id="shiftType" className="form-control" placeholder="" >
                                                    <option value="">Select shift type</option>
                                                    <option value="day">Day Shift</option>
                                                    <option value="night">Night Shift</option>
                                                </Field>
                                                {touched.shiftType && errors.shiftType && (<div className="errors">{errors.shiftType}</div>)}
                                            </div>
                                        </div>
                                        <div className="col-12 mb-2">
                                            <label htmlFor="jobDate" className="form-label mb-0">Job Date</label>
                                            <Field type="date" name="jobDate" id="jobDate" className="form-control" placeholder="" />
                                            {touched.jobDate && errors.jobDate && (<div className="errors">{errors.jobDate}</div>)}
                                        </div>
                                        <div className="row m-0 mb-2 p-0">
                                            <div className="col-6">
                                                <label htmlFor="startTime" className="form-label mb-0">Start Time:</label>
                                                <Field type="time" name="startTime" id="startTime" className="form-control" placeholder="Choose Start Time" />
                                                {touched.startTime && errors.startTime && (<div className="errors">{errors.startTime}</div>)}
                                            </div>
                                            <div className="col-6">
                                                <label htmlFor="endTime" className="form-label mb-0">End Time:</label>
                                                <Field type="time" name="endTime" id="endTime" className="form-control" placeholder="Choose End Time" />
                                                {touched.endTime && errors.endTime && (<div className="errors">{errors.endTime}</div>)}
                                            </div>
                                        </div>
                                        <p>Job Duration: 2hrs</p>
                                    </div>
                                    <div className="row m-0 p-0">
                                        <div className="col-4 px-1">
                                            <button type="button" name='preview-btn' className="btn preview-btn ">Preview</button>
                                        </div>
                                        <div className="col-8">
                                            <button type="submit" name='submit' className="btn proceed-btn">Proceed to Payment</button>
                                        </div>
                                    </div>
                                </Form>
                            )}
                        </Formik>

                    </div>
                    <div className="modal-footer border-0">
                    </div>
                </div>
            </div>
        </div >
    )
}

export default Postmodal