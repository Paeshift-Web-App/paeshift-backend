import React, { useState } from 'react'
import { useNavigate } from "react-router-dom";
import brandLogo from "../assets/images/logo-sm.png";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCheck, faChevronLeft, faCircle, faEye, faEyeSlash } from "@fortawesome/free-solid-svg-icons";
import { ToastContainer, toast, Bounce } from 'react-toastify'
import Axios from "axios";




const VerificationScreen = () => {
    let redir = useNavigate();
    const [values, setValues] = useState({
        otp: "",

    });

    const [otp, setOtp] = useState(new Array(6).fill(""));


    // Dynamic notification
    const notify = (val) =>
        toast.success(val, {
            position: "top-right",
            autoClose: 2000,
            hideProgressBar: false,
            closeOnClick: true,
            pauseOnHover: true,
            draggable: true,
            progress: undefined,
            theme: "light",
            transition: Bounce,
        });

    // Dynamic notification
    const errorNotify = (val) =>
        toast.error(val, {
            position: "top-right",
            autoClose: 2000,
            hideProgressBar: false,
            closeOnClick: true,
            pauseOnHover: true,
            draggable: true,
            progress: undefined,
            theme: "light",
            transition: Bounce,
        });



    function handleInput(e, index) {

        if (isNaN(e.target.value)) return false
        setOtp([...otp.map((data, i) => (i === index ? e.target.value : data))]);
        if(e.target.value && e.target.nextSibling) {
            e.target.nextSibling.focus()
        }
        
    }

    async function handleValidation(e) {
        e.preventDefault();
        let userdata = otp.join("");


        if (userdata === "") {
            errorNotify("Otp is Required");
        }
        else {
            notify("Login successfull");
            console.log(userdata);

            // Endpoint needs to be updated
            // let baseURL = "http://localhost:8000/Users";
            // try {
            //     let getUser = await axios.get(`${baseURL}/${values.email}`);

            //     if (getUser.data.password === values.password) {
            //       notify("account logged in successfully");
            //       setUser({ isLoggedIn: true, data: getUser.data });
            //       setTimeout(()=> {
            //         redir("../dashboard");
            //       }, 1500)
            //     } else {
            //       Errnotify("Invalid login details");
            //     }
            //   } catch (error) {
            //     console.error(error);
            //     if (error.response.status === 404) {
            //       Errnotify("User does not exist");
            //     }
            //   }

        }




    }


    return (
        <div className="row m-0 px-2 otp_wrapper animate__animated animate__fadeIn">
            <div className="col-12 col-md-4 main-card animate__animated animate__zoomIn">
                <div className="col-12 bg-card-2"></div>
                <div className="col-12 bg-card-3"></div>
                <div className="bg-card">
                    <div>
                        <ToastContainer />
                    </div>
                    <div className="row">
                        <div className="col-3">
                            <a href="/signup" className='text-dark'>
                                <FontAwesomeIcon icon={faChevronLeft} />
                            </a>
                        </div>
                        <div className="col-6 text-center">
                            <img src={brandLogo} className="brand-logo ms-2" alt="Paeshift logo" />
                        </div>
                        <div className="col-3"></div>
                    </div>
                    <div className="row content">
                        <div className="col-12 px-0">
                            <div className="title">
                                <h3>OTP verification</h3>
                                <p>An OTP was sent to your email address (Eniolalucas@gmail.com)</p>
                            </div>
                            <form className="otp_form" onSubmit={handleValidation}>

                                <div className="mb-2 otp_area">
                                    {
                                        otp.map((data, i) => {
                                            return <input type="text" maxLength={1} className="form-control" name="otp" value={data} onChange={(e)=>handleInput(e, i)} key={i} />

                                        })
                                    }
                                </div>
                                <p className="mt-3">Didn’t get Code? <a href="#" > Resend OTP in 0:0</a></p>

                                <button type="submit" name='submit' className="btn primary-btn w-100 mt-2">Verify Code</button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default VerificationScreen