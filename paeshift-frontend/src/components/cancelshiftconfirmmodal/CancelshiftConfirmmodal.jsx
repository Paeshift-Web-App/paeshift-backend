import React, { useState, useEffect } from "react";
import iconWarning from "../../assets/images/warning.png"
import "./CancelshiftConfirmmodal.css"; 

const CancelshiftConfirmmodal = () => {



    return (
        <div className="modal fade come-from-modal right text-center" id="cancelshiftConfirmModal" data-bs-backdrop="static" data-bs-keyboard="false" tabIndex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
            <div className="modal-dialog">
                <div className="modal-content">
                    <div className="modal-header border-0">
                        <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div className="modal-body mb-0 pb-0">
                        <img src={iconWarning} alt="Success Logo" />
                        <div className="title">
                            <h1>Cancel Shift?</h1>
                            <p>
                                Are you sure you want to cancel this shift? Doing this you ascertain that you are not interested to continue this job anymore.  
                            </p>
                        </div>
                        <div className="row m-0 p-0">
                            <div className="col-4 px-1">
                                <button type="button" name='submit' className="btn preview-btn ">Go Back</button>
                            </div>
                            <div className="col-8">
                                <button type="submit" className="btn proceed-btn" data-bs-toggle="modal" data-bs-target="#paymentMethodModal" >Cancel Shift</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div >
    )
}

export default CancelshiftConfirmmodal