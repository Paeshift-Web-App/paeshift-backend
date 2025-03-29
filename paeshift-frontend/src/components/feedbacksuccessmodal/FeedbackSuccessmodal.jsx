import React, { useState, useEffect } from "react";
import iconSuccess from "../../assets/images/success.png"
import "./FeedbackSuccessmodal.css";




const FeedbackSuccessmodal = () => {

    return (
        <div className="modal fade come-from-modal right text-center" id="feedbackSuccessModal" data-bs-backdrop="static" data-bs-keyboard="false" tabIndex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
            <div className="modal-dialog">
                <div className="modal-content">
                    <div className="modal-header border-0">
                        <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div className="modal-body mb-0 pb-0">
                        <img src={iconSuccess} alt="Success Logo" />
                        <div className="title">
                            <h1>Successful!</h1>
                            <p>
                                You’ve successfully sent feedback to this worker. You can proceed to create another job post once needed.
                            </p>
                        </div>
                        <div className="row m-0 p-0">
                            <div className="col-4 px-1">
                                <a href="../jobs" className="btn preview-btn">View Jobs</a>
                            </div>
                            <div className="col-8">
                                <button type="submit" className="btn proceed-btn" data-bs-toggle="modal" data-bs-target="#" >Back to Home</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div >
    )
}

export default FeedbackSuccessmodal