import React, { useState, useEffect } from "react";
import "./Walletmodal.css";
import Stars from "../../assets/images/stars.png";
import iconWallet from "../../assets/images/wallet.png";
import iconLogo from "../../assets/images/icon-logo.png";
import Axios from "axios";
import { faBarsProgress } from "@fortawesome/free-solid-svg-icons";
import { faBars } from "@fortawesome/free-solid-svg-icons";
import ProfileImage from "../../assets/images/profile.png"

const Walletmodal = () => {

 let [profile, setProfile] = useState("");


const handleWithdraw = () => {
    alert("Withdrawal in progress");
}



    // GET CURRENT USER PROFILE 
  useEffect(() => {
    Axios.get("http://localhost:8000/jobs/whoami")
      .then((response) => {
        setProfile(response.data);
        console.log(response.data);
      })
      .catch((error) => console.error(error));

  }, [])

    // GET CURRENT USER WALLET BALANCE 
  useEffect(() => {
    Axios.get("http://localhost:8000/jobs/wallet/balance/")
      .then((response) => {
        setProfile(response.data);
        console.log(response.data);
      })
      .catch((error) => console.error(error));

  }, [])

    return (
        <div className="modal fade come-from-modal right" id="walletModal" data-bs-backdrop="static" data-bs-keyboard="false" tabIndex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
            <div className="modal-dialog">
                <div className="modal-content">
                    <div className="modal-header border-0">
                        <h1 className="modal-title fs-5" id="staticBackdropLabel">Wallet</h1>
                        <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div className="modal-body mb-0 pb-0">
                        <div className="balance">
                            <h4>Wallet Balance</h4>
                            <h1>₦ 23,166.00 {profile.wallet_balance}</h1>
                            <p>January 6, 2025 . 11:35 AM</p>
                        </div>
                        <div className="transactions">
                            <div className="top_section">
                                <div><h3>Wallet Transaction</h3></div>
                                <div><a href="#">See More</a></div>
                            </div>
                            <div className="bottom_section">
                                <div className="transaction">
                                    <span className="profile_info">
                                        <span className="profileWrapper">
                                            <img className="prof" src={ProfileImage} alt="profile" />
                                        </span>
                                        <span>
                                            <h4>Eniola Lucas</h4>
                                            <p className="date">20 December 2024, 08:24 PM</p>
                                        </span>
                                    </span>
                                    <h3 className="credit-amount">+ #23,400</h3>
                                </div>
                                <div className="transaction">
                                    <span className="profile_info">
                                        <span className="profileWrapper">
                                            <img className="prof" src={iconLogo} alt="profile" />
                                        </span>
                                        <span>
                                            <h4>Platform Fee</h4>
                                            <p className="date">20 December 2024, 08:24 PM</p>
                                        </span>
                                    </span>
                                    <h3 className="debit-amount">- #234</h3>
                                </div>
                                <div className="transaction">
                                    <span className="profile_info">
                                        <span className="profileWrapper">
                                            <img className="prof" src={ProfileImage} alt="profile" />
                                        </span>
                                        <span>
                                            <h4>Eniola Lucas</h4>
                                            <p className="date">20 December 2024, 08:24 PM</p>
                                        </span>
                                    </span>
                                    <h3 className="credit-amount">+ #23,400</h3>
                                </div>
                                <div className="transaction">
                                    <span className="profile_info">
                                        <span className="profileWrapper">
                                            <img className="prof" src={iconLogo} alt="profile" />
                                        </span>
                                        <span>
                                            <h4>Platform Fee</h4>
                                            <p className="date">20 December 2024, 08:24 PM</p>
                                        </span>
                                    </span>
                                    <h3 className="debit-amount">- #234</h3>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="modal-footer border-0">

                        <button type="button" className="btn withdraw-btn" onClick={()=>handleWithdraw()}>Withdraw</button>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Walletmodal