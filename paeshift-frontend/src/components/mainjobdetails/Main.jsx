import React, { useState, useEffect } from "react";
import "./Jobdetails.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faChevronLeft } from "@fortawesome/free-solid-svg-icons";
import { faBookmark } from "@fortawesome/free-regular-svg-icons";

import GoogleMapReact from "google-map-react";


import Stars from "../../assets/images/stars.png";
import Axios from "axios";
import { faBars } from "@fortawesome/free-solid-svg-icons";
import ProfileImage from "../../assets/images/profile.png";
import MapImage from "../../assets/images/map.png";
import Walletmodal from "../walletmodal/Walletmodal";
import Profilemodal from "../profile/Profilemodal";
import Applicantmodal from "../applicantmodal/Applicantmodal";
import PaymentDetailsmodal from "../paymentdetailsmodal/PaymentDetailsmodal";



// import { userInfo } from "../../atoms/User.jsx";
// import { useRecoilValue } from "recoil";

const AnyReactComponent = ({ text }) => <div>{text}</div>;

const Main = () => {
  // let user = useRecoilValue(userInfo);

  const [prods, setProduct] = useState();
  const [admins, setAdmins] = useState();
  const [users, setUsers] = useState();

  const defaultProps = {
    center: {
      lat: 11.3970071,
      lng: 5.4847741,
    },
    zoom: 8,
  };

  function applyJob() {
    // swal("Application Successful!", "Your application has been successfully submitted. The client will review your details and get back to you shortly.", "success", { button: true, timer: 1500 })

    MySwal.fire({
      title: <p>Hello World</p>,
      didOpen: () => {
        // `MySwal` is a subclass of `Swal` with all the same instance & static methods
        MySwal.showLoading()
      },
    }).then(() => {
      return MySwal.fire(<p>Shorthand works too</p>)
    })
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


  return (
    <main className="col-12 col-md-12 col-lg-9 col-xl-10 ms-sm-auto main__job-details px-md-4">
      <div className="row page_title">
        <div className="col-1 pt-lg-2">
          <a href="/jobs" className='text-dark'>
            <FontAwesomeIcon icon={faChevronLeft} />
          </a>
        </div>
        <div className="col-10 payment-btn">
          <h1 className="mb-0">Job Details</h1>
          <button type="button" className="mb-0 me-1" data-bs-toggle="modal" data-bs-target="#paymentDetailsModal">View Payment Detail</button>
        </div>
        <div className="col-1 p-0">
          <button className="navbar-toggler position-absolute d-lg-none collapsed mt-1" type="button"
            data-bs-toggle="collapse" data-bs-target="#sidebarMenu" aria-controls="sidebarMenu" aria-expanded="false" aria-label="Toggle navigation"
          >
            <FontAwesomeIcon className="icon-bars" icon={faBars} />
          </button>
        </div>
      </div>
      <section className="container container__data">
        <div className="row m-0 p-0 map_wrapper">
          {/* <div className="col-12 m-0 p-0" style={{ height: '100vh', width: '100%' }}> */}
          <div className="col-12 m-0 p-0 img" >
            <img src={MapImage} alt="MapImage" />
            {/* <GoogleMapReact
              bootstrapURLKeys={{ key: "AIzaSyAMDoXjU2XFWN1vKFPxAVimw_teBjVBpQA" }}
              defaultCenter={defaultProps.center}
              defaultZoom={defaultProps.zoom}
            >
              <AnyReactComponent lat={11.3970071} lng={5.4847741} text="Google Map" />
            </GoogleMapReact> */}
          </div>
        </div>
        <div className="row mt-3 px-3">
          <div className="col-12 job_details">
            <h4 className="">Employer</h4>
            <div className="card_top">
              <span className="profile_info">
                <span>
                  <img className="prof" src={ProfileImage} alt="profile" />
                </span>
                <span>
                  <h4>Eniola Lucas</h4>
                  <img src={Stars} alt="profile" /> <span className="rate_score">4.98</span>
                </span>
              </span>
              <span className="top_cta">
                <button className="btn" data-bs-toggle="modal" data-bs-target="#profileModal">View Profile</button>
              </span>
            </div>
          </div>
        </div>
        <div className="row mt-3 px-3">
          <div className="col-12 job_details">
            <h4 className="">Worker(s)</h4>
            <div className="card_top">
              <span className="profile_info">
                <span>
                  <img className="prof" src={ProfileImage} alt="profile" />
                </span>
                <span>
                  <h4>Eniola Lucas</h4>
                  <img src={Stars} alt="profile" /> <span className="rate_score">4.98</span>
                </span>
              </span>
              <span className="top_cta">
                <button className="btn" data-bs-toggle="modal" data-bs-target="#profileModal">Feedback Worker</button>
              </span>
            </div>
          </div>
        </div>
        <section className="container_bottom">
          <div className="row mb-2">
            <div className="col-12 col-md-6">
              <p>Job Title:</p>
              <h2>Professional Grass Cutter</h2>
            </div>
            <div className="col-6 col-md-3">
              <p>Applicant Needed:</p>
              <h2>1</h2>
            </div>
            <div className="col-6 col-md-3">
              <p>Duration:</p>
              <h2>2hrs Contract</h2>
            </div>
          </div>
          <div className="row">
            <div className="col-12 col-md-6">
              <p>Start Date:</p>
              <h2>Monday 2nd March, 2024.</h2>
            </div>
            <div className="col-6 col-md-3">
              <p>Start Time:</p>
              <h2>09:00 AM.</h2>
            </div>
            <div className="col-6 col-md-3">
              <p>Job Pay:</p>
              <h2>₦4,000</h2>
            </div>
          </div>
        </section>
        <section className="container_bottom">
          <div className="row">
            <div className="col-12 applicant_details">
              <h4>2 Applicant(s) Applied</h4>
              <button className="btn view-btn" data-bs-toggle="modal" data-bs-target="#applicantModal">View Applicants</button>
            </div>
          </div>
        </section>
        <section className="buttons">
          <button className="btn saved">Saved &nbsp; <FontAwesomeIcon icon={faBookmark} className="icon-saved" /> </button>
          <button className="btn apply-btn" onClick={() => applyJob()}>Apply Now</button>
        </section>
      </section>
      <div className="row">
        <Profilemodal />
        <Applicantmodal />
        <PaymentDetailsmodal />
      </div>
    </main >
  )
}

export default Main





// import React, { useState, useEffect } from "react";
// import "./Jobdetails.css";
// import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
// import { faChevronLeft, faBars } from "@fortawesome/free-solid-svg-icons";
// import { faBookmark } from "@fortawesome/free-regular-svg-icons";
// import GoogleMapReact from "google-map-react";
// import Axios from "axios";
// import Stars from "../../assets/images/stars.png";
// import ProfileImage from "../../assets/images/profile.png";
// import Walletmodal from "../walletmodal/Walletmodal";
// import Profilemodal from "../profile/Profilemodal";
// import Applicantmodal from "../applicantmodal/Applicantmodal";
// import PaymentDetailsmodal from "../paymentdetailsmodal/PaymentDetailsmodal";

// // Custom Marker Component
// const Marker = ({ text }) => (
//   <div style={{ color: "red", fontWeight: "bold" }}>{text}</div>
// );

// const Main = () => {
//   const [jobLocation, setJobLocation] = useState({
//     lat: 11.3970071,
//     lng: 5.4847741,
//   });

//   const [zoom, setZoom] = useState(10);

//   // Fetch job details (including location)
//   useEffect(() => {
//     Axios.get("http://localhost:8000/job/1") // Replace with actual API
//       .then((response) => {
//         if (response.data.location) {
//           setJobLocation({
//             lat: response.data.location.lat,
//             lng: response.data.location.lng,
//           });
//         }
//       })
//       .catch((error) => console.error(error));
//   }, []);

//   return (
//     <main className="col-12 col-md-12 col-lg-9 col-xl-10 ms-sm-auto main__job-details px-md-4">
//       <div className="row page_title">
//         <div className="col-1 pt-lg-2">
//           <a href="/jobs" className="text-dark">
//             <FontAwesomeIcon icon={faChevronLeft} />
//           </a>
//         </div>
//         <div className="col-10 payment-btn">
//           <h1 className="mb-0">Job Details</h1>
//           <button
//             type="button"
//             className="mb-0 me-1"
//             data-bs-toggle="modal"
//             data-bs-target="#paymentDetailsModal"
//           >
//             View Payment Detail
//           </button>
//         </div>
//         <div className="col-1 p-0">
//           <button
//             className="navbar-toggler position-absolute d-lg-none collapsed mt-1"
//             type="button"
//             data-bs-toggle="collapse"
//             data-bs-target="#sidebarMenu"
//             aria-controls="sidebarMenu"
//             aria-expanded="false"
//             aria-label="Toggle navigation"
//           >
//             <FontAwesomeIcon className="icon-bars" icon={faBars} />
//           </button>
//         </div>
//       </div>

//       {/* Dynamic Google Map */}
//       <section className="container container__data">
//         <div className="row m-0 p-0 map_wrapper">
//           <div className="col-12 m-0 p-0" style={{ height: "400px", width: "100%" }}>
//             <GoogleMapReact
//               bootstrapURLKeys={{ key: process.env.REACT_APP_GOOGLE_MAPS_API_KEY }} // Use an environment variable
//               defaultCenter={jobLocation}
//               defaultZoom={zoom}
//             >
//               <Marker lat={jobLocation.lat} lng={jobLocation.lng} text="Job Location" />
//             </GoogleMapReact>
//           </div>
//         </div>

//         {/* Job Details */}
//         <div className="row mt-3 px-3">
//           <div className="col-12 job_details">
//             <h4>Employer</h4>
//             <div className="card_top">
//               <span className="profile_info">
//                 <span>
//                   <img className="prof" src={ProfileImage} alt="profile" />
//                 </span>
//                 <span>
//                   <h4>Eniola Lucas</h4>
//                   <img src={Stars} alt="stars" /> <span className="rate_score">4.98</span>
//                 </span>
//               </span>
//               <span className="top_cta">
//                 <button className="btn" data-bs-toggle="modal" data-bs-target="#profileModal">
//                   View Profile
//                 </button>
//               </span>
//             </div>
//           </div>
//         </div>

//         <section className="container_bottom">
//           <div className="row">
//             <div className="col-12 applicant_details">
//               <h4>2 Applicant(s) Applied</h4>
//               <button className="btn view-btn" data-bs-toggle="modal" data-bs-target="#applicantModal">
//                 View Applicants
//               </button>
//             </div>
//           </div>
//         </section>

//         <section className="buttons">
//           <button className="btn saved">
//             Saved &nbsp; <FontAwesomeIcon icon={faBookmark} className="icon-saved" />
//           </button>
//           <button className="btn apply-btn">Apply Now</button>
//         </section>
//       </section>

//       <div className="row">
//         <Profilemodal />
//         <Applicantmodal />
//         <PaymentDetailsmodal />
//       </div>
//     </main>
//   );
// };

// export default Main;


