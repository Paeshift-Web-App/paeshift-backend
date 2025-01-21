import React from 'react'
import { createRoot } from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import 'bootstrap/dist/css/bootstrap.min.css';
import './assets/css/style.css';

import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'

const MySwal = withReactContent(Swal);


import Flashscreen from './pages/Flashscreen.jsx';
import Usertypescreen from './pages/Usertypescreen.jsx';
import Signup from './pages/Signup.jsx';
import Signin from './pages/Signin.jsx';
import ForgotPassword from './pages/ForgotPassword.jsx';
import CreatePassword from './pages/CreatePassword.jsx';
import VerificationScreen from './pages/VerificationScreen.jsx';
import ThirdParty from './pages/ThirdParty.jsx';
import Dashboard from './pages/Dashboard.jsx';

import { GoogleOAuthProvider } from '@react-oauth/google';
import Jobs from './pages/Jobs.jsx';
import JobDetails from './pages/JobDetails.jsx';
import Settings from './pages/Settings.jsx';
// import { RecoilRoot } from "recoil";


const router = createBrowserRouter([
  {
    // id:id++,
      path: "/jobdetails",
      // element:  <RecoilRoot><Dashboard /></RecoilRoot>,
      element:  <JobDetails />
    },
  {
    // id:id++,
      path: "/jobs",
      // element:  <RecoilRoot><Dashboard /></RecoilRoot>,
      element:  <Jobs />
    },
  {
    // id:id++,
      path: "/dashboard",
      // element:  <RecoilRoot><Dashboard /></RecoilRoot>,
      element:  <Dashboard />
    },
  {
    path: "/settings",
    element: <Settings />

  },
  {
    path: "/signupwith",
    element: <ThirdParty />

  },
  {
    path: "/verify",
    element: <VerificationScreen />

  },
  {
    path: "/createpassword",
    element: <CreatePassword />

  },
  {
    path: "/forgotpassword",
    element: <ForgotPassword />

  },
  {
    path: "/signin",
    element: <Signin />

  },
  {
    path: "/signup",
    element: <Signup />

  },
  {
    path: "/select",
    element: <Usertypescreen />

  },
  {
    path: "/",
    element: <Flashscreen />

  },
]);


createRoot(document.getElementById('root')).render(
  <GoogleOAuthProvider clientId="796224650682-uuudhogl202q8lgh0d01kul7i86j2f25.apps.googleusercontent.com">
    <RouterProvider router={router} />
  </GoogleOAuthProvider>
)
