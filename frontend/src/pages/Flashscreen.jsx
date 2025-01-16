import React from "react";
import { Link, useNavigate } from "react-router-dom";
import  brandLogo  from "../assets/images/logo.png";
import 'animate.css';




const Flashscreen = () => {
    let redir = useNavigate();
  return (
    <div className="row m-0 p-0 flash_screen animate__animated animate__fadeIn">
      <div className="col-12 brand">
        <img src={brandLogo} className="logo animate__animated animate__zoomIn " alt="Paeshift logo" />
        {
          setInterval(()=>{
             redir("../select");
          }, 2500)
        }
      </div>
    </div>
  );
};

export default Flashscreen;
