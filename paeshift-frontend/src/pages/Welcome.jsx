import React from "react";
import brandLogo from "../assets/images/logo-sm.png";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faChevronLeft } from "@fortawesome/free-solid-svg-icons";
import arrowdivder from '../assets/images/arrow-divider.svg';

import "animate.css";

const Usertypescreen = () => {
  return (
    <div className="row m-0 px-2 user_type_wrapper animate__animated animate__fadeIn">
      <div className="col-12 col-md-4 main-card animate__animated animate__zoomIn">
         <div className="col-12 bg-card-2"></div>
         <div className="col-12 bg-card-3"></div>
        <div className="bg-card">
          <div className="row">
            <div className="col-3">
            </div>
            <div className="col-6">
              <img src={brandLogo} className="brand-logo" alt="Paeshift logo" />
            </div>
            <div className="col-3"></div>
          </div>
          <div className="row content">
            <div className="col-12">
              <div className="title mb-3">
                <h3>Welcome</h3>
                <p>Please select the type of user you want to register as</p>
              </div>
              <div className="body">
                  <a href="./signupwith/applicant" className="btn primary-btn"> Job Seeker/Applicant </a>
                  <img src={arrowdivder} alt="Divider" className="my-3" />
                  <a href="./signupwith/client" className="btn primary-btn"> Job Poster/Client </a>
                  <p className="mt-4">Already have an account? <a href="./signin" >Sign In to my account</a></p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Usertypescreen;
