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
const Schema = Yup.object().shape({
  email: Yup.string().email("Invalid email").required("Required"),
  password: Yup.string().required("Required"),
});

const Signin = () => {
  const navigate = useNavigate();
  const [show, setShow] = useState("password");

  // Called when the form is submitted
  const handleLogin = async (values) => {
    const userData = {
      email: values.email,
      password: values.password,
    };

    try {
      // POST to your Django Ninja login route on port 8000
      // e.g., http://127.0.0.1:8000/jobs/login
      const response = await axios.post("http://127.0.0.1:8000/jobs/login", userData);

      // If success
      if (response.status === 200 && response.data.message) {
        swal("Login Successful!", "", "success");
        // e.g. redirect to dashboard or something else
        setTimeout(() => {
          navigate("/dashboard");
        }, 1500);
      }
      // If Django returns {error: "..."}
      else if (response.data.error) {
        swal("Login Failed!", response.data.error, "error");
      }
    } catch (error) {
      // If server or network error
      if (error.response?.data?.error) {
        swal("Login Failed!", error.response.data.error, "error");
      } else {
        swal("Login Failed!", "Something went wrong. Please try again.", "error");
      }
    }
  };

  return (
    <div className="row m-0 px-2 signin_wrapper animate__animated animate__fadeIn">
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
            <div className="col-3"></div>
          </div>
          <div className="row content">
            <div className="col-12">
              <div className="title">
                <h3>Welcome Back</h3>
                <p>Login with your Email and password</p>
              </div>

              <Formik
                initialValues={{ email: "", password: "" }}
                validationSchema={Schema}
                onSubmit={(values) => handleLogin(values)}
              >
                {({ errors, touched }) => (
                  <Form className="signin_form">
                    <div className="mb-2">
                      <label htmlFor="email" className="form-label mb-0">
                        Email:
                      </label>
                      <Field name="email" className="form-control" />
                      {touched.email && errors.email && (
                        <div className="errors">{errors.email}</div>
                      )}
                    </div>

                    <div className="mb-2">
                      <label htmlFor="password" className="form-label mb-0">
                        Enter Password:
                      </label>
                      <span className="visibility">
                        <Field
                          type={show}
                          name="password"
                          id="password"
                          className="form-control"
                          placeholder="Enter your password"
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

                    <p className="mt-3">
                      <Link to="/forgotpassword">Forgot Password?</Link>
                    </p>

                    <button type="submit" className="btn primary-btn w-100 mt-2">
                      Login
                    </button>
                    <p className="mt-3">
                      Don't have an account? <Link to="/welcome">Create Account</Link>
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

export default Signin;
