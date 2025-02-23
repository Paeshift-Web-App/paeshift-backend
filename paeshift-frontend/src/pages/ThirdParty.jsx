import React, { useCallback, useState } from 'react';
import { Link, useNavigate } from "react-router-dom";
import brandLogo from "../assets/images/logo-sm.png";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faChevronLeft } from "@fortawesome/free-solid-svg-icons";
import { LoginSocialFacebook, LoginSocialApple } from 'reactjs-social-login';

import iemail from "../assets/images/icon-email.png";
import igoogle from "../assets/images/icon-google.png";
import ifacebook from "../assets/images/icon-facebook.png";
import iapple from "../assets/images/icon-apple.png";
import Axios from "axios";

const ThirdParty = () => {
    const navigate = useNavigate();
    const [profile, setProfile] = useState(null);

    const onLoginStart = useCallback(() => {
        console.log('Login process started...');
    }, []);

    // ✅ Redirect to Django's Google OAuth Sign-Up Flow
    const handleGoogleSignup = () => {
        window.location.href = "http://127.0.0.1:8000/accounts/google/login/";
    };

    // ✅ Redirect to Django's Facebook OAuth Sign-Up Flow
    const handleFacebookSignup = () => {
        window.location.href = "http://127.0.0.1:8000/accounts/facebook/login/";
    };

    return (
        <div className="row m-0 px-2 thirdparty_wrapper animate__animated animate__fadeIn">
            <div className="col-12 col-md-4 main-card animate__animated animate__zoomIn">
                <div className="col-12 bg-card-2"></div>
                <div className="col-12 bg-card-3"></div>
                <div className="bg-card">
                    <div className="row">
                        <div className="col-3">
                            <Link to="/select" className='text-dark'>
                                <FontAwesomeIcon icon={faChevronLeft} />
                            </Link>
                        </div>
                        <div className="col-6 text-center">
                            <img src={brandLogo} className="brand-logo ms-2" alt="Paeshift logo" />
                        </div>
                    </div>
                    <div className="row content">
                        <div className="col-12">
                            <div className="title">
                                <h3>Sign Up With</h3>
                                <p>Choose an option to create your account</p>
                            </div>
                            <div className="body">
                                {/* ✅ Sign Up with Email */}
                                <Link to="/signup" className="btn primary-btn-outline mb-2 btn-signup">
                                    <img src={iemail} alt="Email" className="me-2" /> Sign up with Email
                                </Link>

                                {/* ✅ Google OAuth Login */}
                                <button className="btn primary-btn-outline mb-2 btn-signup" onClick={handleGoogleSignup}>
                                    <img src={igoogle} alt="Google" className="me-2" /> Sign up with Google
                                </button>

                                {/* ✅ Facebook OAuth Login */}
                                <button className="btn primary-btn-outline mb-2 btn-signup" onClick={handleFacebookSignup}>
                                    <img src={ifacebook} alt="Facebook" className="me-2" /> Sign up with Facebook
                                </button>

                                {/* ✅ Apple OAuth Login */}
                                <LoginSocialApple
                                    client_id="YOUR_APPLE_CLIENT_ID"
                                    scope={'name email'}
                                    redirect_uri={window.location.href}
                                    onLoginStart={onLoginStart}
                                    onResolve={({ provider, data }) => {
                                        console.log("Apple Login:", data);
                                        setProfile(data);
                                        navigate("/dashboard");
                                    }}
                                    onReject={err => console.error("Apple Login Error:", err)}
                                >
                                    <button className="btn primary-btn-outline mb-2 btn-signup">
                                        <img src={iapple} alt="Apple" className="me-2" /> Sign up with Apple
                                    </button>
                                </LoginSocialApple>

                                <p className="mt-4">
                                    Already have an account? <Link to="/login">Sign In</Link>
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ThirdParty;
