import React, { useCallback, useState } from 'react'
import { Link, useNavigate, useParams } from "react-router-dom";
import brandLogo from "../assets/images/logo-sm.png";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCheck, faChevronLeft, faCircle, faEye, faEyeSlash } from "@fortawesome/free-solid-svg-icons";
import {
    LoginSocialGoogle,
    LoginSocialFacebook,
    LoginSocialApple,
} from 'reactjs-social-login'


// CUSTOMIZE ANY UI BUTTON
import {
    FacebookLoginButton,
    GoogleLoginButton,
    AppleLoginButton,
} from 'react-social-login-buttons'


import iemail from "../assets/images/icon-email.png";
import igoogle from "../assets/images/icon-google.png";
import ifacebook from "../assets/images/icon-facebook.png";
import iapple from "../assets/images/icon-apple.png";
import { ToastContainer, toast, Bounce } from 'react-toastify'
import Axios from "axios";
// import { faChevronLeft, faEye, faEyeSlash } from "@fortawesome/free-regular-svg-icons";

// import { jwtDecode } from "jwt-decode";
import { useGoogleLogin } from '@react-oauth/google';


// REDIRECT URL must be same with URL where the (reactjs-social-login) components is locate
// MAKE SURE the (reactjs-social-login) components aren't unmounted or destroyed before the ask permission dialog closes
const REDIRECT_URI = window.location.href;


const ThirdParty = () => {
    const [provider, setProvider] = useState('')
    const [profile, setProfile] = useState(null)
    const roleValue = useParams();

    const onLoginStart = useCallback((response) => {
            // setProvider(provider)
            // setProfile(data)
            // console.log(data)
            console.log(response.data.userID);
            // alert('login start')
        }
    , [])

    const onLogoutSuccess = useCallback(() => {
        setProfile(null)
        setProvider('')
        alert('logout success')
    }, [])


    const login = useGoogleLogin({
        // onSuccess: tokenResponse => console.log(tokenResponse),
        onSuccess: async (tokenResponse) => {

            let URL = "https://www.googleapis.com/oauth2/v3/userinfo";
            try {
                const res = await Axios.get(
                    URL,
                    {
                        headers: {
                            Authorization: `Bearer ${tokenResponse.access_token}`,
                        },
                    }
                );
                console.log(res.data);
               let values = res.data;

                // same shape as initial values
                /**
                 * Steps to create a new user
                 * get data
                 * sed to db in object format
                 */

                let userdata = {
                    first_name: values.given_name,
                    last_name: values.family_name,
                    email: values.email,
                    role: roleValue.role,
                    password: values.sub,
                    confirm_password: values.sub,
                };

                console.log(userdata);

                // let baseURL = "http://127.0.0.1:8000/jobs/signup";
                let getUsersURL = "http://127.0.0.1:8000/jobs/all-users";
                try {
                    let allUser = await Axios.get(`${getUsersURL}`);
                    // console.log(allUser.data.users); 
                    allUser = allUser.data.users;


                    let isUnique = false;
                    allUser.forEach((each) => {
                        if (each.email === values.email) {
                            isUnique = true;
                        }
                    });

                    // use the typed email to check if the email already exist
                    if (!isUnique) {
                        let result = await Axios.post("http://127.0.0.1:8000/jobs/signup", userdata);
                        result = result.data.message;


                        if (result === "success") {
                            swal("Registeration Successful!", " ", "success", { button: false, timer: 1500 });
                            redir("../signin");
                        }
                        else {
                            swal("Registeration Failed!", " ", "error", { button: false, timer: 1500 })
                        }

                    } else {
                        swal("User already exit!", " ", "error", { button: false, timer: 1500 })
                        // swal("Registeration Failed!", " ", "error", { button: false, timer: 1500 })
                    }
                    // if unique email allow to signup else dont
                } catch (error) {
                    console.error(error);
                }


            } catch (err) {
                console.log(err);
            }
        }
    });



    return (

        <div className="row m-0 px-2 thirdparty_wrapper animate__animated animate__fadeIn">

            <div className="col-12 col-md-4 main-card animate__animated animate__zoomIn">
                <div className="col-12 bg-card-2"></div>
                <div className="col-12 bg-card-3"></div>
                <div className="bg-card">
                    <div className="row">
                        <div className="col-3">
                            <Link to="/welcomeclear
                            " className='text-dark'>
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
                                <h3>Sign Up With</h3>
                                <p>Kindly choose your sign up option to create new account</p>
                            </div>
                            <div className="body">
                                <Link to={`/asignup/${roleValue.role}`} className="btn primary-btn-outline mb-2 btn-signup"> <img src={iemail} alt="Email" className="me-2" /> Sign up with Email </Link>
                                <button className="btn primary-btn-outline mb-2 btn-signup" onClick={() => login()} > <img src={igoogle} alt="Google" className="me-2" /> Sign up with Google </button>
                                <LoginSocialFacebook
                                    isOnlyGetToken
                                    appId='607654518584001'
                                    // onLoginStart={onLoginStart}
                                    onResolve={onLoginStart}
                                    onReject={(err) => {
                                        console.log(err)
                                    }}
                                    scope="email,public_profile"
                                >
                                    {/* <FacebookLoginButton className="btn primary-btn-outline w-100 mb-2" /> */}
                                    <button className="btn primary-btn-outline mb-2 btn-signup"> <img src={ifacebook} alt="Facebook" className="me-2" /> Sign up with Facebook </button>

                                </LoginSocialFacebook>
                                <LoginSocialApple
                                    client_id="adffgfg"
                                    scope="email,public_profile"
                                    redirect_uri={REDIRECT_URI}
                                    // onLoginStart={onLoginStart}
                                    onResolve={({ provider, data }) => {
                                        setProvider(provider);
                                        setProfile(data);
                                    }}
                                    onReject={err => {
                                        console.log(err);
                                    }}
                                >
                                    <button className="btn primary-btn-outline mb-2 btn-signup"> <img src={iapple} alt="Apple" className="me-2" /> Sign up with Apple </button>
                                </LoginSocialApple>

                                <p className="mt-4">Already have an account? <Link href="#" >Sign In to my account</Link></p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default ThirdParty