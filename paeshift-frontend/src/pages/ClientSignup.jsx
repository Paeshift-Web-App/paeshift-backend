import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import brandLogo from "../assets/images/logo-sm.png";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faChevronLeft, faEye, faEyeSlash } from "@fortawesome/free-solid-svg-icons";

import { Formik, Form, Field } from "formik";
import * as Yup from "yup";

import swal from "sweetalert";
import axios from "axios";
import "animate.css";

// Yup validation schema
const SignupSchema = Yup.object().shape({
  firstName: Yup.string().required("Required").min(2, "Too short!"),
  lastName: Yup.string().required("Required").min(2, "Too short!"),
  email: Yup.string().email("Invalid email").required("Required"),
  password: Yup.string()
    .min(6, "Must contain at least 6 characters")
    .max(50, "Too Long!")
    .required("Required")
    .matches(/[a-z]/, "Must contain at least one lowercase character")
    .matches(/[A-Z]/, "Must contain at least one uppercase character")
    .matches(/[0-9]/, "Must contain at least one number")
    .matches(/[!@#$%^&*]/, "Must contain at least one special character"),
  confirmPassword: Yup.string()
    .min(6, "Too Short!")
    .max(50, "Too Long!")
    .required("Required")
    .oneOf([Yup.ref("password"), null], "Passwords must match"),
});

const Signup = () => {
  const navigate = useNavigate();
  const [show, setShow] = useState("password");
  const [show1, setShow1] = useState("password");

  const handleSignup = async (values) => {
    const userData = {
      firstName: values.firstName,
      lastName: values.lastName,
      email: values.email,
      password: values.password,
      confirmPassword: values.confirmPassword,
    };

    try {
      // POST to Django endpoint
      const response = await axios.post(
        "http://127.0.0.1:8000/jobs/signup",
        userData
      );

      if (response.status === 201 && response.data.message) {
        swal("Registration Successful!", "", "success");
        setTimeout(() => {
          navigate("/signin");
        }, 1500);
      } else if (response.data.error) {
        swal("Registration Failed!", response.data.error, "error");
      }
    } catch (error) {
      if (error.response?.data?.error) {
        swal("Registration Failed!", error.response.data.error, "error");
      } else {
        swal("Registration Failed!", "Something went wrong. Please try again.", "error");
      }
    }
  };

  return (
    <div className="row m-0 px-2 signup_wrapper animate__animated animate__fadeIn">
      <div className="col-12 col-md-4 main-card animate__animated animate__zoomIn">
        <div className="col-12 bg-card-2"></div>
        <div className="col-12 bg-card-3"></div>
        <div className="bg-card">
          <div className="row">
            <div className="col-3">
              <Link to="/welcome" className="text-dark">
                <FontAwesomeIcon icon={faChevronLeft} />
              </Link>
            </div>
            <div className="col-6 text-center">
              <img src={brandLogo} className="brand-logo ms-2" alt="Paeshift logo" />
            </div>
            <div className="col-3" />
          </div>

          <div className="row content">
            <div className="col-12">
              <div className="title">
                <h3>Sign Up</h3>
                <p>Kindly provide us with your details to create a new account</p>
              </div>

              <Formik
                initialValues={{
                  firstName: "",
                  lastName: "",
                  email: "",
                  password: "",
                  confirmPassword: "",
                }}
                validationSchema={SignupSchema}
                onSubmit={(values) => handleSignup(values)}
              >
                {({ errors, touched }) => (
                  <Form className="signup_form">
                    <div className="mb-2">
                      <label htmlFor="firstName" className="form-label mb-0">
                        First Name
                      </label>
                      <Field name="firstName" className="form-control" />
                      {touched.firstName && errors.firstName && (
                        <div className="errors">{errors.firstName}</div>
                      )}
                    </div>

                    <div className="mb-2">
                      <label htmlFor="lastName" className="form-label mb-0">
                        Last Name
                      </label>
                      <Field name="lastName" className="form-control" />
                      {touched.lastName && errors.lastName && (
                        <div className="errors">{errors.lastName}</div>
                      )}
                    </div>

                    <div className="mb-2">
                      <label htmlFor="email" className="form-label mb-0">
                        Email
                      </label>
                      <Field name="email" className="form-control" />
                      {touched.email && errors.email && (
                        <div className="errors">{errors.email}</div>
                      )}
                    </div>

                    <div className="mb-2">
                      <label htmlFor="password" className="form-label mb-0">
                        Create Password
                      </label>
                      <span className="visibility">
                        <Field
                          type={show}
                          name="password"
                          id="password"
                          className="form-control"
                        />
                        <FontAwesomeIcon
                          icon={show === "password" ? faEye : faEyeSlash}
                          onClick={() =>
                            setShow(show === "password" ? "text" : "password")
                          }
                          className="eye-icon"
                        />
                      </span>
                      {touched.password && errors.password && (
                        <div className="errors">{errors.password}</div>
                      )}
                    </div>

                    <div className="mb-2">
                      <label htmlFor="confirmPassword" className="form-label mb-0">
                        Confirm Password
                      </label>
                      <span className="visibility">
                        <Field
                          type={show1}
                          name="confirmPassword"
                          id="confirmPassword"
                          className="form-control"
                        />
                        <FontAwesomeIcon
                          icon={show1 === "password" ? faEye : faEyeSlash}
                          onClick={() =>
                            setShow1(show1 === "password" ? "text" : "password")
                          }
                          className="eye-icon"
                        />
                      </span>
                      {touched.confirmPassword && errors.confirmPassword && (
                        <div className="errors">{errors.confirmPassword}</div>
                      )}
                    </div>

                    <button
                      type="submit"
                      className="btn primary-btn w-100 mt-2"
                    >
                      Sign Up
                    </button>
                    <p className="mt-3">
                      Already have an account? <Link to="/signin">Login</Link>
                    </p>
                  </Form>
                )}
              </Formik>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Signup;
