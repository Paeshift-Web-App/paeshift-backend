import React, { useState } from 'react'
import {Link, useNavigate } from "react-router-dom";
import brandLogo from "../assets/images/logo-sm.png";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCheck, faChevronLeft, faCircle, faEye, faEyeSlash } from "@fortawesome/free-solid-svg-icons";
import { ToastContainer, toast, Bounce } from 'react-toastify'
import Axios from "axios";


const ForgotPassword = () => {
    let redir = useNavigate();
    const [values, setValues] = useState({
        email: "",

    });

    let [show, setShow] = useState('password');
    let [password, setPassword] = useState('');
    const email_pattern = /^[^\s@]+@[^\s@]+\.[^\s@]{2,6}$/;

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



    function handleInput(e) {
        const newData = { ...values, [e.target.name]: e.target.value }
        // const newData = [ ...values,  e.target.value ]
        setValues(newData);
    }

    async function handleValidation(e) {
        e.preventDefault();
        let userdata = {
            email: values.email,
        };


        if (userdata.email === "") {
            errorNotify("Email is Required");
        }
        else if (!email_pattern.test(userdata.email)) {
            errorNotify("Invalid email address");
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
        <div className="row m-0 px-2 forgot_wrapper animate__animated animate__fadeIn">
            <div className="col-12 col-md-4 main-card animate__animated animate__zoomIn">
                <div className="col-12 bg-card-2"></div>
                <div className="col-12 bg-card-3"></div>
                <div className="bg-card">
                    <div>
                        <ToastContainer />
                    </div>
                    <div className="row">
                        <div className="col-3">
                            <Link to="/signin" className='text-dark'>
                                <FontAwesomeIcon icon={faChevronLeft} />
                            </Link>
                        </div>
                        <div className="col-6 text-center">
                            <img src={brandLogo} className="brand-logo ms-2" alt="Paeshift logo" />
                        </div>
                        <div className="col-3"></div>
                    </div>
                    <div className="row content">
                        <div className="col-12">
                            <div className="title">
                                <h3>Forgot Password</h3>
                                <p>To reset your password, Please enter your registered email address</p>
                            </div>
                            <form className="forgot_form" onSubmit={handleValidation}>
                                <div className="mb-2">
                                    <label htmlFor="email" className="form-label mb-0">Email</label>
                                    <input type="email" className="form-control" name="email" id="email" placeholder="Enter your email address" onChange={handleInput} />
                                </div>
                                <button type="submit" name='submit' className="btn primary-btn w-100 mt-2">Continue</button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default ForgotPassword