import React, { useState } from 'react'
import { Link, useNavigate } from "react-router-dom";
import brandLogo from "../assets/images/logo-sm.png";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCheck, faChevronLeft, faCircle, faEye, faEyeSlash } from "@fortawesome/free-solid-svg-icons";

import { Formik, Form, Field } from "formik";
import * as Yup from "yup";

import { ToastContainer, toast, Bounce } from 'react-toastify';
import Axios from "axios";
// import { faChevronLeft, faEye, faEyeSlash } from "@fortawesome/free-regular-svg-icons";
import swal from 'sweetalert';

import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'



// import { userInfo } from '../atoms/User';
// import { useRecoilState } from 'recoil';

const AppSwal = withReactContent(Swal);

const Schema = Yup.object().shape({
  firstName: Yup.string().required("Required").min(2, "Too short!").required("Required"),
  lastName: Yup.string().required("Required").min(2, "Too short!").required("Required"),
  email: Yup.string().email("Invalid email").required("Required"),
  password: Yup.string().min(6, "Must Contain 8 Characters").max(50, "Too Long!").required("Required")
    .matches(/^(?=.*[a-z])/, "Must Contain One Lowercase Character")
    .matches(/^(?=.*[A-Z])/, "Must Contain One Uppercase Character")
    .matches(/^(?=.*[0-9])/, "Must Contain One Number Character")
    .matches(/^(?=.*[!@#\$%\^&\*])/, "Must Contain  One Special Case Character"),
  confirmPassword: Yup.string().min(6, "Too Short!").max(50, "Too Long!").required("Required")
    .oneOf([Yup.ref("password"), null], "Passwords must match"),
});


const Signup = () => {
  let redir = useNavigate();


  let [show, setShow] = useState('password');
  let [show1, setShow1] = useState('password');






  return (
    <div className="row m-0 px-2 signup_wrapper animate__animated animate__fadeIn">
      <div className="col-12 col-md-4 main-card animate__animated animate__zoomIn">
        <div className="col-12 bg-card-2"></div>
        <div className="col-12 bg-card-3"></div>
        <div className="bg-card">
          <div>
            {/* <ToastContainer /> */}

          </div>
          <div className="row">
            <div className="col-3">
              <Link to="/welcome" className='text-dark'>
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
                <h3>Sign Up</h3>
                <p>Kindly provide us with your details to create new account</p>
                <Formik
                  initialValues={{
                    firstName: "",
                    lastName: "",
                    email: "",
                    password: "",
                    confirmPassword: "",
                  }}

                  validationSchema={Schema}
                  onSubmit={async (values) => {
                    // same shape as initial values
                    /**
                     * Steps to create a new user
                     * get data
                     * sed to db in object format
                     */

                    let userdata = {
                      firstName: values.firstName,
                      lastName: values.lastName,
                      email: values.email,
                      role: "applicant",
                      password: values.confirmPassword,
                    };

                    console.log(userdata);


                    let baseURL = "http://localhost:8000/Users";
                    try {
                      let allUser = await Axios.get(`${baseURL}`);

                      let isUnique = false;
                      allUser.data.forEach((each) => {
                        if (each.email === values.email) {
                          isUnique = true;
                        }
                      });

                      // use the typed email to check if the email already exist
                      if (!isUnique) {
                        Axios.post(`${baseURL}`, userdata)
                          .then((response) => {
                            //   setUser({isLoggedIn: true, data: response.data});
                            swal("Registeration Successful!", " ", "success", { button: false, timer: 1500 });
                            setTimeout(() => {
                              redir("../signin");

                            }, 1500);
                          })
                          .catch((error) => {
                            console.error(error);
                          });
                      } else {
                        swal("User already exit!", " ", "error", { button: false, timer: 1500 })
                        // swal("Registeration Failed!", " ", "error", { button: false, timer: 1500 })
                      }
                      // if unique email allow to signup else dont
                    } catch (error) {
                      console.error(error);
                    }

                    // swal(<p className="mb-2">Registeration Successful!</p>, 'success', false, 1500)
                    // Endpoint needs to be updated
                    // let baseURL = "https://paeshift-backend.onrender.com/userApi/v1/user/register/";
                    // try {
                    //   // let allUser = await Axios.get(`${baseURL}`);

                    //   // let isUnique = false;
                    //   // allUser.data.forEach((each) => {
                    //   //   if (each.email === values.email) {
                    //   //     isUnique = true;
                    //   //   }
                    //   // });


                    //   // setInterval(() => {
                    //   //   AppSwal.showLoading()
                    //   // }, 1000);

                    //   // use the typed email to check if the email already exist
                    //   // if (!isUnique) {
                    //   await Axios({
                    //     method: 'post',
                    //     url: `${baseURL}`,
                    //     // url: "https://paeshift-backend.onrender.com/userApi/v1/user/register/",
                    //     data: userdata
                    //   })
                    //     .then((response) => {
                    //       console.log(response);
                    //       swal("Registeration Successful!", " ", "success", { button: false, timer: 1500 });
                    //       redir("../signin");
                    //       // setTimeout(() => {
                    //       // redir("../signin");
                    //       // }, 1500);
                    //     })
                    //     .catch((error) => {
                    //       swal("Registeration Failed!", " ", "error", { button: false, timer: 1500 })
                    //       console.error(error.message);
                    //     });

                    //   // if unique email allow to signup else dont
                    // } catch (error) {
                    //   console.error(error);
                    // }
                  }
                  }
                >
                  {({ errors, touched }) => (
                    <Form className="signup_form">
                      <div>
                        <label htmlFor="firstName" className="form-label mb-0">First Name:</label>
                        <Field name="firstName" className="form-control" />
                        {/* If this field has been touched, and it contains an error, display it */}
                        {touched.firstName && errors.firstName && (<div className="errors">{errors.firstName}</div>)}
                      </div>
                      <div>
                        <label htmlFor="lastName" className="form-label mb-0">Last Name:</label>
                        <Field name="lastName" className="form-control" />
                        {touched.lastName && errors.lastName && (<div className="errors">{errors.lastName}</div>)}
                      </div>
                      <div>
                        <label htmlFor="email" className="form-label mb-0">Email:</label>
                        <Field name="email" className="form-control" />
                        {touched.email && errors.email && (<div className="errors">{errors.email}</div>)}
                      </div>
                      <div>
                        <label htmlFor="password" className="form-label mb-0">Create Password:</label>
                        <span className="visibility">
                          <Field type={show} name="password" id="password" className="form-control" />
                          <FontAwesomeIcon icon={show === "password" ? faEye : faEyeSlash} onClick={() => setShow(show === "password" ? "text" : "password")} className='eye-icon' />
                        </span>
                        {touched.password && errors.password && (<div className="errors">{errors.password}</div>)}
                      </div>
                      <div >
                        <label htmlFor="confrimPassword" className="form-label mb-0">Confirm Password:</label>
                        <span className="visibility">
                          <Field type={show1} name="confirmPassword" id="confirmPassword" className="form-control" />
                          <FontAwesomeIcon icon={show1 === "password" ? faEye : faEyeSlash} onClick={() => setShow1(show1 === "password" ? "text" : "password")} className='eye-icon' />
                        </span>
                        {touched.confirmPassword && errors.confirmPassword && (<div className="errors">{errors.confirmPassword}</div>)}
                      </div>
                      <button type="submit" name='submit' className="btn primary-btn w-100 mt-2">Sign Up</button>
                      <p className="mt-3">Already have an account? <Link to="/signin">Login</Link></p>
                    </Form>
                  )}
                </Formik>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Signup