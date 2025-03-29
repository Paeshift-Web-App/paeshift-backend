import React, { useState, useEffect } from "react";
import iconSuccess from "../../assets/images/success.png"
import "./AcceptJobmodal.css";











const AcceptJobmodal = () => {



    // let userdata = {

    //     title: values.jobtitle,
    //     location: values.jobLocation,
    //     industry: values.jobIndustry,
    //     subcategory: values.jobSubCategory,
    //     rate: values.jobRate,
    //     applicants_needed: values.noOfApplicants,
    //     job_type: values.jobType,
    //     shift_type: values.shiftType,
    //     date: values.jobDate,
    //     start_time: values.startTime,
    //     end_time: values.endTime,
    //     payment_status: "pending"
    // }

    // console.log(userdata);

    // try {

    //     await Axios.post("http://127.0.0.1:8000/jobs/create-job", userdata, {
    //         withCredentials: true,
    //         headers: {
    //             'Content-Type': 'application/json',
    //             // Include an Authorization header if using token auth
    //         }
    //     })
    //         .then(response => {
    //             // console.log(response.data);
    //             console.log(response);
    //             //     swal("Job Creation Successful!", " ", "success", { button: false, timer: 1500 });
    //             //     redir("../dashboard");
    //         })

    // } catch (error) {
    //     //     swal("Job Creation Failed!", " ", "error", { button: false, timer: 1500 })
    //     console.error(error);
    // }



    return (
        <div className="modal fade come-from-modal right text-center" id="acceptJobModal" data-bs-backdrop="static" data-bs-keyboard="false" tabIndex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
            <div className="modal-dialog">
                <div className="modal-content">
                    <div className="modal-header border-0">
                        <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div className="modal-body mb-0 pb-0">
                        <img src={iconSuccess} alt="Success Logo" />
                        <div className="title">
                            <h1>Successful!</h1>
                            <p>You’ve successfully accepted this applicant to take on this job. You can now follow up with the applicant complete the job.</p>
                        </div>

                        <div className="row m-0 p-0">
                            <div className="col-4 px-1">
                                <button type="button" name='submit' className="btn preview-btn ">View Job</button>
                            </div>
                            <div className="col-8">
                                <button type="submit" className="btn proceed-btn" data-bs-toggle="modal" data-bs-target="#paymentMethodModal" >Back to Home</button>

                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div >
    )
}

export default AcceptJobmodal