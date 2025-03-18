import React, { useEffect } from "react";
import Sidebar from "../components/sidebar/SideBar";
import Main from "../components/main/Main";
import { useNavigate } from "react-router-dom";
import "./Home.css";
import { useRecoilValue } from "recoil";
import { userInfo } from "../atoms/User";

const Home = () => {
  // let user = useRecoilValue(userInfo);
  let redir = useNavigate();

 

  // useEffect(()=> {
  //   if (!user.isLoggedIn) {
  //     redir("../");
  //   }
  // }, [user.isLoggedIn, redir])

  return (
    <div className="container-fluid dashboard_container">
      <div className="row p-0">
        <Sidebar />
        <Main />
      </div>
    </div>
  );
};

export default Home;
