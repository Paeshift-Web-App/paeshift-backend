import React from 'react'
import Sidebar from "../components/sidebar/SideBar";
import Main from "../components/mainjob/Main";
import { useNavigate } from "react-router-dom";



const Jobs = () => {
  return (
    <div className="container-fluid dashboard_container">
      <div className="row p-0">
        <Sidebar />
        <Main />
      </div>
    </div>
  )
}

export default Jobs