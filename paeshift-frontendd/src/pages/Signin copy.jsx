import React, { useState } from 'react'
import { useNavigate } from "react-router-dom";
import brandLogo from "../assets/images/logo-sm.png";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCheck, faChevronLeft, faCircle, faEye, faEyeSlash } from "@fortawesome/free-solid-svg-icons";
import { ToastContainer, toast, Bounce } from 'react-toastify'
import Axios from "axios";




const Signin = () => {
    let redir = useNavigate();
    const [values, setValues] = useState({
        email: "",
        password: ""

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
            password: values.password,

        };


        if (userdata.email === "") {
            errorNotify("Email is Required");
        }
        else if (!email_pattern.test(userdata.email)) {
            errorNotify("Invalid email address");
        }
        else if (userdata.password === "") {
            errorNotify("Password is Required");
        }
        else {
            notify("Login successfull");
            console.log(userdata);
            redir("./dashboard");

            // Endpoint needs to be updated


            // const token = '..your token..';
            // const headers = {
            //     'Content-Type': 'application/json',
            //     "Access-Control-Allow-Origin": "*",
            //     'Authorization': 'JWT fefege...',
            //     'Authorization': `Basic ${token}`
            // }
            // let baseURL = "http://localhost:8000/Users";
            // try {
            //     let getUser = await Axios.get(`${baseURL}/${values.email}`, {
            //         headers: headers
            //     });

            //     if (getUser.data.password === values.password) {
            //         notify("account logged in successfully");
            //         //   setUser({ isLoggedIn: true, data: getUser.data });
            //         setTimeout(() => {
            //             redir("../dashboard");
            //         }, 1500)
            //     } else {
            //         errorNotify("Invalid login details");
            //     }
            // } catch (error) {
            //     console.error(error);
            //     if (error.response.status === 404) {
            //         errorNotify("User does not exist");
            //     }
            // }

        }




    }


    return (
        <div className="row m-0 px-2 signin_wrapper animate__animated animate__fadeIn">
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
                        <div className="col-12">
                            <div className="title">
                                <h3>Welcome Back</h3>
                                <p>Login with your Email and password</p>
                            </div>
                            <form className="signin_form" onSubmit={handleValidation}>
                                <div className="mb-2">
                                    <label htmlFor="email" className="form-label mb-0">Email</label>
                                    <input type="email" className="form-control" name="email" id="email" placeholder="Enter email address" onChange={handleInput} />
                                </div>
                                <div className="mb-2">
                                    <label htmlFor="password" className="form-label mb-0">Enter Password</label>
                                    <span className="visibility">
                                        <input type={show} className="form-control" name="password" id="password" placeholder="Enter your password" onChange={handleInput} />
                                        <FontAwesomeIcon icon={show === "password" ? faEye : faEyeSlash} onClick={() => setShow(show === "password" ? "text" : "password")} className='eye-icon' />
                                    </span>
                                </div>
                                <p className="mt-3"><a href="/forgotpassword" >Forgot Password?</a></p>

                                <button type="submit" name='submit' className="btn primary-btn w-100 mt-2">Login</button>
                            </form>

                            <p className="mt-5">Don't have an account? <a href="/signup" >Create Account</a></p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Signin