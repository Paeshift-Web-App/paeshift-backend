import React, { useState } from 'react'
import { useNavigate } from "react-router-dom";
import brandLogo from "../assets/images/logo-sm.png";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCheck, faChevronLeft, faCircle, faEye, faEyeSlash } from "@fortawesome/free-solid-svg-icons";

import { ToastContainer, toast, Bounce } from 'react-toastify';
import Axios from "axios";
// import { faChevronLeft, faEye, faEyeSlash } from "@fortawesome/free-regular-svg-icons";




const Signup = () => {



  let redir = useNavigate();
  const [values, setValues] = useState({

    firstname: "",
    lastname: "",
    email: "",
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
      // id: values.email,
      firstName: values.firstname,
      lastName: values.lastname,
      email: values.email,
      password: values.password,
      confirmPassword: values.confirmPassword,
    };


    console.log(userdata.password);
    if (userdata.firstName === "") {
      errorNotify("First name is Required");
    }
    else if (userdata.lastName === "") {
      errorNotify("Last name is Required");
    }
    else if (userdata.email === "") {
      errorNotify("Email is Required");
    }
    else if (!email_pattern.test(userdata.email)) {
      errorNotify("Invalid email address");
    }
    else if (userdata.password === "") {
      console.log(userdata.password);
      errorNotify("Password is Required");
    }
    else if (!password_pattern.test(userdata.password)) {
      errorNotify("Invalid password");
    } else if (userdata.password !== userdata.confirmPassword) {
      errorNotify("Password did not match");
    }
    else {
      notify("Registeration successfull");
      console.log(userdata);
      redir("../signin");





      // swal({
      //   title: 'Registeration Successful!',
      //   icon: 'success',
      //   button: false,
      //   timer: 1500
      // })
      // Endpoint needs to be updated
      // let baseURL = "http://localhost:8000/Users";
      // try {
      // let allUser = await Axios.get(`${baseURL}`);

      // let isUnique = false;
      // allUser.data.forEach((each) => {
      //   if (each.email === values.email) {
      //     isUnique = true;
      //   }
      // });

      // use the typed email to check if the email already exist
      // const token = '..your token..';
      // const headers = {
      //   'Content-Type': 'application/json',
      //   "Access-Control-Allow-Origin": "*",
      //   'Authorization': 'JWT fefege...',
      //   'Authorization': `Basic ${token}`
      // } 
      // if (!isUnique) {
      //   Axios.post(`${baseURL}`, userdata, {
      //     headers: headers
      //   })
      //     .then((response) => {
      //       //   setUser({isLoggedIn: true, data: response.data});
      //       notify("Signed up successfully");
      //       setTimeout(() => {
      //         // redir("../signin");
      //       }, 1500);
      //     })
      //     .catch((error) => {
      //       console.error(error);
      //     });
      // } else {
      //   errorNotify("User already exit");
      // }
      // if unique email allow to signup else dont
      // } catch (error) {
      //   console.error(error);
      // }


      // Axios({
      //   url: `${baseURL}`,
      //   method: 'POST',
      //   data: userdata,
      //   headers: {
      //     "Access-Control-Allow-Origin": "*",
      //     'Content-Type': 'application/json',
      // headers: {
      // 'Access-Control-Allow-Origin': '*',
      // 'Content-Type': 'application/json',
      // "Access-Control-Allow-Headers": "Content-Type",
      // "Access-Control-Allow-Origin": "https://paeshift-backend.onrender.com",
      // 'Content-Type': 'application/json',
      // "Access-Control-Allow-Methods": "OPTIONS,POST"
      // }
      //   }

      // })


    }

    // try {
    //   // let allUser = await Axios.get(`${baseURL}`);

    //   // let isUnique = false;
    //   // allUser.data.forEach((each) => {
    //   //   if (each.email === values.email) {
    //   //     isUnique = true;
    //   //   }
    //   // });

    //   // use the typed email to check if the email already exist

    //   // if (!isUnique) {
    //   let result = fetch("https://paeshift-backend.onrender.com/userApi/v1/user/register/",

    //     {
    //       method: 'POST',
    //       body: JSON.stringify(userdata),
    //       headers: {
    //         'Access-Control-Allow-Origin': '*',
    //         'Content-Type': 'application/json',
    //         "Accept": 'application/json'

    //       }
    //     })
    //     .then((res) => {
    //       console.log(res.json());
    //       swal("Registeration Successful!", " ", "success", { button: false, timer: 1500 });
    //       redir("../signin");
    //     })
    //     .then((data) => {
    //       console.log(data);
    //     })

    //   // if unique email allow to signup else dont
    // } catch (error) {
    //   swal("Registeration Failed!", " ", "error", { button: false, timer: 1500 })
    //   console.error(error);
    // }


  }


  return (
    <div className="row m-0 px-2 signup_wrapper animate__animated animate__fadeIn">
      <div className="col-12 col-md-4 main-card animate__animated animate__zoomIn">
        <div className="col-12 bg-card-2"></div>
        <div className="col-12 bg-card-3"></div>
        <div className="bg-card">
          <div>
            <ToastContainer />
          </div>
          <div className="row">
            <div className="col-3">
              <a href="/select" className='text-dark'>
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
                <h3>Sign Up</h3>
                <p>Kindly provide us with your details to create new account</p>
              </div>
              <form className="signup_form" onSubmit={handleValidation}>
                <div className="mb-2">
                  <label htmlFor="firstname" className="form-label mb-0">First Name</label>
                  <input type="text" className="form-control" name="firstname" id="firstname" placeholder="Enter your first name" onChange={handleInput} />
                </div>
                <div className="mb-2">
                  <label htmlFor="lastname" className="form-label mb-0">Last Name</label>
                  <input type="text" className="form-control" name="lastname" id="lastname" placeholder="Enter your last name" onChange={handleInput} />
                </div>
                <div className="mb-2">
                  <label htmlFor="email" className="form-label mb-0">Email</label>
                  <input type="email" className="form-control" name="email" id="email" placeholder="Enter email address" onChange={handleInput} />
                </div>
                <div className="mb-2">
                  <label htmlFor="password" className="form-label mb-0">Create Password</label>
                  <span className="visibility">
                    <input type={show} className="form-control" name="password" id="password" placeholder="Enter your password" onChange={handleInput} />
                    <FontAwesomeIcon icon={show === "password" ? faEye : faEyeSlash} onClick={() => setShow(show === "password" ? "text" : "password")} className='eye-icon' />
                  </span>
                  <p>Password must be alphanumeric, specialchars and min - 8 characters</p>
                </div>
                <div className="mb-2">
                  <label htmlFor="confirmPassword" className="form-label mb-0">Confirm Password</label>
                  <span className="visibility">
                    <input type={show1} name="confirmPassword" className={password != "" && password === confirm ? "form-control matched" : "form-control"} id="confirmPassword" placeholder="Confirm your password" onChange={handleInput} />
                    <FontAwesomeIcon icon={show1 === "password" ? faEye : faEyeSlash} onClick={() => setShow1(show1 === "password" ? "text" : "password")} className='eye-icon' />
                  </span>
                  {/* <p>{password === confirm ? "Password matched!" : " Password not matched!"}</p> */}
                </div>
                <button type="submit" name='submit' className="btn primary-btn w-100 mt-2">Sign Up</button>
              </form>
              <p className="mt-3">Already have an account? <a href="/signin" >Login</a></p>
            </div>
          </div>
        </div>
      </div>

    </div>
  )
}

export default Signup