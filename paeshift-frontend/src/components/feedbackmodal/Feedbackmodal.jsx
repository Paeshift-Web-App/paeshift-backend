import React, { useState, useEffect } from "react";
import feedBackImage from "../../assets/images/feedback.png";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import "./Feedbackmodal.css";


import Axios from "axios";
import { userInfo } from "../../atoms/User.jsx";
import { useRecoilValue, useRecoilState } from "recoil";

import { Formik, Form, Field } from "formik";
import * as Yup from "yup";
import FeedbackSuccessmodal from "../feedbacksuccessmodal/FeedbackSuccessmodal.jsx";




const Schema = Yup.object().shape({
    feedback: Yup.string().required("Required").min(2, "Too short!"),
    feedbacktype: Yup.string().required("Required"),
    rating: Yup.string().required("Required"),
});






const Feedbackmodal = () => {

const [feedback, setFeedback] = useState("");



// /jobs/feedback/

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


                        <Formik
                            initialValues={{
                                feedbacktype: "",
                                feedback: "",
                                rating: ""
                            }}

                            validationSchema={Schema}
                            onSubmit={(values) => {

                                let userdata = {
                                    userId: profile.id,
                                    user: profile.role,
                                    jobId: job_id,
                                    clientId: job_id,
                                    feedbacktype: values.feedbacktype,
                                    feedback: values.feedback,
                                    rating: values.ratings
                                };

                                redir("../jobs");
                                const modal = new bootstrap.Modal('#feedbackSuccessModal');
                                modal.show()
                                console.log(userdata);

                                try {
                                    useEffect(() => {
                                        Axios.post("http://localhost:8000/jobs/feedback", {userdata})
                                            .then((response) => {
                                                setFeedback(response.data.jobs);
                                                console.log(response.data.jobs);
                                            })
                                            .catch((error) => console.error(error));
                                    }, [])

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
                                            <label htmlFor="feedbacktype" className="form-label mb-0">Feedback Type</label>
                                            <Field as="select" name="feedbacktype" id="feedbacktype" className="form-control" >
                                                <option value="">Choose type of Feedback</option>
                                                <option value="dispute">Dispute</option>
                                                <option value="review">Review</option>
                                            </Field>
                                            {touched.feedbacktype && errors.feedbacktype && (<div className="errors">{errors.feedbacktype}</div>)}
                                        </div>
                                    </div>
                                    <div className="row rating mt-2">
                                        <div className="col-7">
                                            <h4>Worker Rating</h4>
                                            <span>Nice Experience</span>
                                        </div>
                                        <div className="col-5 star-ratings">
                                            <FontAwesomeIcon icon={faStar} className="rating-star" />
                                            <FontAwesomeIcon icon={faStar} className="rating-star" />
                                            <FontAwesomeIcon icon={faStar} className="rating-star" />
                                            <FontAwesomeIcon icon={faStar} className="rating-star" />
                                            <FontAwesomeIcon icon={faStar} className="rating-star" />
                                        </div>
                                    </div>
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
                    <FeedbackSuccessmodal />
                </div>
            </div>
        </div >
    )
}

export default Feedbackmodal