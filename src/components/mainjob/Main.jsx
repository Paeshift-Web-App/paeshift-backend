import React, { useState, useEffect } from "react";
import "./Jobs.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faServer, faUser, faUserGroup, faSearch } from "@fortawesome/free-solid-svg-icons";
import { faBell, faBookmark } from "@fortawesome/free-regular-svg-icons";

import Stars from "../../assets/images/stars.png";
import iconWallet from "../../assets/images/wallet.png";
import iconLogo from "../../assets/images/icon-logo.png";
import Axios from "axios";
import { faBarsProgress } from "@fortawesome/free-solid-svg-icons";
import { faBars } from "@fortawesome/free-solid-svg-icons";
import ProfileImage from "../../assets/images/profile.png";
import Walletmodal from "../walletmodal/Walletmodal";


import { JobsData } from "./JobsData";
// import { defaults } from "chart.js/auto";
// import { Bar, Line } from "react-chartjs-2";
// import { ChartData } from "./Chartdata";
// import { userInfo } from "../../atoms/User.jsx";
// import { useRecoilValue } from "recoil";



// defaults.maintainAspectRatio = false;
// defaults.responsive = true;

// defaults.plugins.title.display = true;
// defaults.plugins.title.align = "start";
// defaults.plugins.title.font.size = 20;
// defaults.plugins.title.color = "black";

let id = 0;
export const filterButton = [
  {
    id: id++,
    title: 'All',
    value: ''
  },
  {
    id: id++,
    title: 'Upcoming',
    value: 'upcoming'
  },
  {
    id: id++,
    title: 'Ongoing',
    value: 'ongoing'
  },
  {
    id: id++,
    title: 'Completed',
    value: 'completed'
  },
  {
    id: id++,
    title: 'Canceled',
    value: 'cancel'
  },

]












const Main = () => {
  // let user = useRecoilValue(userInfo);

  // const [prods, setProduct] = useState();
  // const [admins, setAdmins] = useState();
  // const [users, setUsers] = useState();

  const [searchWork, setSearchWork] = useState("");

  const [filterState, setFilterState] = useState("");
  const [jobs, setJobs] = useState("")


  const filterFunction = (e) => {
    const buttons = document.getElementsByClassName('filter-btn');
    setFilterState(e.target.value);
    for (let index = 0; index < buttons.length; index++) {
      buttons[index].classList.remove('active');;
    }
    e.target.classList.add('active');
    // buttons;
  } 

  // useEffect(() => {

  //   Axios.get("http://localhost:8000/Products")
  //     .then((response) => {
  //       setProduct(response.data);
  //     })
  //     .catch((error) => console.error(error));



  //   Axios.get("http://localhost:8000/Admin")
  //     .then((response) => {
  //       setAdmins(response.data);
  //     })
  //     .catch((error) => console.error(error));

  //   Axios.get("http://localhost:8000/Users")
  //     .then((response) => {
  //       setUsers(response.data);
  //       })
  //       .catch((error) => console.error(error));
  // }, []);

  // console.log(user.data)

  // alert(filterState);




  return (
    <main className="col-12 col-md-12 col-lg-9 col-xl-10 ms-sm-auto  px-md-4">
      <div className="d-flex justify-content-between align-items-center flex-wrap flex-md-nowrap align-items-center pb-2 ">
        <div className="page_header">
          <h1 className="m-0 p-0">Jobs</h1>
          <div className="">
            <button className="navbar-toggler position-absolute d-lg-none collapsed" type="button"
              data-bs-toggle="collapse" data-bs-target="#sidebarMenu" aria-controls="sidebarMenu" aria-expanded="false" aria-label="Toggle navigation"
            >
              <FontAwesomeIcon className="icon-bars" icon={faBars} />
            </button>
          </div>
        </div>
        <div className="searchbar-section">
          <div className="serachbar-notify">
            <div className="me-2 searchbar">
              <input className="form-control searchbar-input" onChange={(e) => setSearchWork(e.target.value)} type="text" placeholder="Search" aria-label="Search" />
              <FontAwesomeIcon className="search-icon" icon={faSearch} />
            </div>
            <button type="button" className="notification-icon px-3">
              <FontAwesomeIcon className="" icon={faBell} />
            </button>
          </div>
          <button type="button" className="btn btn-wallet px-3" data-bs-toggle="modal" data-bs-target="#walletModal">
            <img src={iconWallet} alt="" srcSet="" /> ₦0.00
          </button>
        </div>
      </div>
      <section className="container container__data">
        <div className="row m-0 p-0">
          <div className="col-12 m-0 p-0">
            <div className="filter-section">
              {
                filterButton.map((item, key) => {
                  return (
                    <button type="button" key={key} value={item.value} onClick={filterFunction} className={item.title === "All" ? "filter-btn active" : "filter-btn"}>{item.title}</button>
                  )
                })
              }

            </div>
          </div>
        </div>
        <div className="row mt-3">
          <div className="cards jobs">


            {JobsData &&
              JobsData.filter((item) => {
                return searchWork.toLowerCase() === "" ? item.status.toLowerCase().includes(filterState.toLowerCase()) : item.title.toLowerCase().includes(searchWork.toLowerCase());
              }).map((item, key) => {
                return (
                  <div className="card" key={key}>
                    <div className="card_top">
                      <span className="profile_info">
                        <span>
                          <img className="prof" src={ProfileImage} alt="profile" />
                        </span>
                        <span>
                          <h4>{item.name}</h4>
                          <span className="rate_score">{item.role}</span>
                        </span>
                      </span>
                      <span className="top_cta">
                        <button className={"btn " + item.status}>{item.status.charAt(0).toUpperCase() + item.status.slice(1)}</button>
                      </span>
                    </div>
                    <div className="row">
                      <div className="col-12"><h2>{item.title}</h2></div>
                    </div>
                    <div className="row">
                      <div className="col-3 pe-0"><p>Location:</p></div>
                      <div className="col-9"><h4 className="text-truncate">{item.location}</h4></div>
                    </div>
                    <div className="row">
                      <div className="col-4 pe-0"><p>Date:</p></div>
                      <div className="col-8"><h4>{item.date}</h4></div>
                    </div>
                    <div className="row">
                      <div className="col-6 pe-0"><p>Time:</p></div>
                      <div className="col-6"><h4>{item.time}</h4></div>
                    </div>
                    <div className="row">
                      <div className="col-6 pe-0"><p>Contract Duration:</p></div>
                      <div className="col-6"><h4>{item.duration}</h4></div>
                    </div>
                    <div className="row">
                      <div className="col-6 pe-0"><p>Amount:</p></div>
                      <div className="col-6"><h4>₦{item.amount}.00</h4></div>
                    </div>
                    {
                      item.status === 'upcoming' ?
                        <div className="bottom">
                          <span>
                            <button className="cancel">Cancel</button>
                          </span>
                          <span>
                            <button className="track-btn">Track Location</button>
                          </span>
                        </div> :
                        ""
                    }
                    {
                      item.status === 'ongoing' ?
                        <div className="bottom">
                          <span>
                            <button className="cancel">01:59:48</button>
                          </span>
                          <span>
                            <button className="track-btn">Share Location</button>
                          </span>
                        </div> :
                        ""
                    }
                    {
                      item.status === 'completed' || item.status === 'canceled' ?
                        <div className="bottom">
                          <button className="track-btn w-100">Feedback Client</button>
                        </div>
                        :
                        ""
                    }
                  </div>
                );
              })
              // JobsData.filter((item) => {
              //   return filterState.toLowerCase() === "" ? item : item.status.includes(filterState.toLowerCase());
              // }).map((item, key) => {
              //   return (
              //       <div className={"col-6 col-md-3 state " + item.image} key={key}>
              //         <h4>{item.location}</h4>
              //         <p>{item.description}</p>
              //       </div>
              //   );
              // })
            }

          </div>
        </div>
        <Walletmodal />
      </section>
    </main >
  )
}

export default Main
