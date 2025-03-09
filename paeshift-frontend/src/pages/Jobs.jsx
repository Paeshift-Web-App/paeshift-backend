import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

import Sidebar from "../components/sidebar/SideBar";
import Main from "../components/mainjob/Main";

const Jobs = () => {
  const navigate = useNavigate();
  const [jobs, setJobs] = useState([]);

  useEffect(() => {
    // Fetch jobs from Django
    axios
      .get("http://127.0.0.1:8000/jobs/list") // Adjust if your endpoint differs
      .then((response) => {
        setJobs(response.data); // response.data should be an array of jobs
      })
      .catch((error) => {
        console.error("Error fetching jobs:", error);
        // Optionally redirect or show an error message
      });
  }, []);

  return (
    <div className="container-fluid dashboard_container">
      <div className="row p-0">
        <Sidebar />
        {/* Pass the jobs array to <Main /> as a prop */}
        <Main jobs={jobs} />
      </div>
    </div>
  );
};

export default Jobs;
