import React, { useState } from 'react'
import {Link, useNavigate } from "react-router-dom";
import brandLogo from "../assets/images/logo-sm.png";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCheck, faChevronLeft, faCircle, faEye, faEyeSlash } from "@fortawesome/free-solid-svg-icons";

import { ToastContainer, toast, Bounce } from 'react-toastify'
import Axios from "axios";
// import { faChevronLeft, faEye, faEyeSlash } from "@fortawesome/free-regular-svg-icons";


const CreatePassword = () => {
    let redir = useNavigate();
    const [values, setValues] = useState({
        password: "",
        confirmPassword: ""

    });

    let [show, setShow] = useState('password');
    let [show1, setShow1] = useState('password');
    let [password, setPassword] = useState('');
    let [confirm, setConfirm] = useState('');
    const email_pattern = /^[^\s@]+@[^\s@]+\.[^\s@]{2,6}$/;
    const password_pattern = /^[\w@-]{8,}$/;

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
            id: values.email,
            password: values.password,
            confirmPassword: values.confirmPassword,
        };


       if (userdata.password === "") {
            console.log(userdata.password);
            errorNotify("Password is Required");
        }
        else if (!password_pattern.test(userdata.password)) {
            errorNotify("Invalid password");
        } else if (userdata.password !== userdata.confirmPassword) {
            errorNotify("Password did not match");
        }
        else {
            notify("Password changed successfull");
            console.log(userdata);

            // Endpoint needs to be updated
            // let baseURL = "http://localhost:8000/Users";
            // try {
            //   let allUser = await Axios.get(`${baseURL}`);

            // // use the typed email to check if the email already exist
            //   Axios.post(`${baseURL}`, userdata)
            //     .then((response) => {
            //       //   setUser({isLoggedIn: true, data: response.data});
            //       notify("Password changed successfully");
            //       setTimeout(() => {
            //         // redir("../login");
            //       }, 1500);
            //     })
            //     .catch((error) => {
            //       console.error(error);
            //     });
           
            // // if unique email allow to signup else dont
            // } catch (error) {
            //   console.error(error);
            // }

        }


    }


    return (
        <div className="row m-0 px-2 createpass_wrapper animate__animated animate__fadeIn">
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
                                <h3>Create New Password</h3>
                                <p>Create a secure password to access your account</p>
                            </div>
                            <form className="createpass_form" onSubmit={handleValidation}>
                                <div className="mb-2">
                                    <label htmlFor="password" className="form-label mb-0">Create New Password</label>
                                    <span className="visibility">
                                        <input type={show} className="form-control" name="password" id="password" placeholder="Enter your new password" onChange={handleInput} />
                                        <FontAwesomeIcon icon={show === "password" ? faEye : faEyeSlash} onClick={() => setShow(show === "password" ? "text" : "password")} className='eye-icon' />
                                    </span>
                                    <p>Password must be alphanumeric, specialchars and min - 8 characters</p>
                                </div>
                                <div className="mb-2 mt-4">
                                    <label htmlFor="confirmPassword" className="form-label mb-0">Confirm New Password</label>
                                    <span className="visibility">
                                        <input type={show1} name="confirmPassword" className={password != "" && password === confirm ? "form-control matched" : "form-control"} id="confirmPassword" placeholder="Confirm your new password" onChange={handleInput} />
                                        <FontAwesomeIcon icon={show1 === "password" ? faEye : faEyeSlash} onClick={() => setShow1(show1 === "password" ? "text" : "password")} className='eye-icon' />
                                    </span>
                                </div>
                                <button type="submit" name='submit' className="btn primary-btn w-100 mt-2">Save Changes</button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default CreatePassword