import React, { useState, useEffect } from "react";
import Stars from "../../assets/images/stars.png";
import iconWallet from "../../assets/images/wallet.png";
import iconLogo from "../../assets/images/icon-logo.png";
import feedBackImage from "../../assets/images/feedback.png";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBarsProgress, faLocation, faLocationArrow, faLocationDot, faStar } from "@fortawesome/free-solid-svg-icons";
import { faBars } from "@fortawesome/free-solid-svg-icons";
import ProfileImage from "../../assets/images/profile.png"
import "./Feedbackmodal.css";


import Axios from "axios";
import { userInfo } from "../../atoms/User.jsx";
import { useRecoilValue, useRecoilState } from "recoil";

import { Formik, Form, Field } from "formik";
import * as Yup from "yup";




const Schema = Yup.object().shape({
    feedback: Yup.string().required("Required").min(2, "Too short!").required("Required"),
});






const Feedbackmodal = () => {












    return (
        <div className="modal fade come-from-modal right" id="feedbackModal" data-bs-backdrop="static" data-bs-keyboard="false" tabIndex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
            <div className="modal-dialog">
                <div className="modal-content">
                    <div className="modal-header border-0">
                        <h1 className="modal-title fs-5" id="staticBackdropLabel">Feedback Worker</h1>
                        <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div className="modal-body mb-0 pb-0">
                        <div className="row">
                            <div className="col-12 text-center feedbackContent">
                                <img src={feedBackImage} alt="feed back image" />
                                <p>
                                    This employee needs your rating and feedback
                                    about the job to stand out among other applicants. Thank you!
                                </p>
                            </div>
                        </div>
                        <div className="row rating mt-2">
                            <div className="col-7">
                                <h4>Worker Rating</h4>
                                <span>Nice Experience</span>
                            </div>
                            <div className="col-5 star-ratings">
                                <FontAwesomeIcon icon={faStar} className="rating-star"/>
                                <FontAwesomeIcon icon={faStar} className="rating-star"/>
                                <FontAwesomeIcon icon={faStar} className="rating-star"/>
                                <FontAwesomeIcon icon={faStar} className="rating-star"/>
                                <FontAwesomeIcon icon={faStar} className="rating-star"/>
                            </div>
                        </div>


                        <Formik
                            initialValues={{
                                feedback: ""
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
                                    feedback: values.feedback
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
                                <Form >
                                    <div className="row">
                                        <div className="col-12 mb-3">
                                            <Field as="textarea" name="feedback" id="feedback" className="form-control" placeholder="We’d love to hear from you..." row="" >
                                            </Field>
                                            <span className="text-count" >0/2000</span>
                                            {touched.feedback && errors.feedback && (<div className="errors">{errors.feedback}</div>)}
                                        </div>

                                    </div>
                                    <div className="row m-0 p-0">
                                        <div className="col-5 px-1">
                                            <button type="button" name='cancel' className="btn back-btn" data-bs-dismiss="modal">Go Back</button>
                                        </div>
                                        <div className="col-7 px-1">
                                            <button type="submit" name='submit' className="btn submit-btn">Send Feedback</button>
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

export default Feedbackmodal