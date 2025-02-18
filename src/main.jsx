import React from 'react'
import { createRoot } from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import 'bootstrap/dist/css/bootstrap.min.css';
import './assets/css/style.css';

import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'

const MySwal = withReactContent(Swal);


import Flashscreen from './pages/Flashscreen.jsx';
import Welcome from './pages/Welcome.jsx';
import AppSignup from './pages/AppSignup.jsx';
import ClientSignup from './pages/ClientSignup.jsx';
import Signin from './pages/Signin.jsx';
import ForgotPassword from './pages/ForgotPassword.jsx';
import CreatePassword from './pages/CreatePassword.jsx';
import VerificationScreen from './pages/VerificationScreen.jsx';
import ThirdParty from './pages/ThirdParty.jsx';
import Dashboard from './pages/Dashboard.jsx';
import Home from './pages/Home.jsx';

import { GoogleOAuthProvider } from '@react-oauth/google';
import Jobs from './pages/Jobs.jsx';
import JobDetails from './pages/JobDetails.jsx';
import Settings from './pages/Settings.jsx';
import { RecoilRoot } from "recoil";


const router = createBrowserRouter([
  {
    // id:id++,
      path: "/jobdetails",
      element:  <RecoilRoot><JobDetails /></RecoilRoot>
    },
  {
    // id:id++,
      path: "/jobs",
      element:  <RecoilRoot><Jobs /></RecoilRoot>
    },
  {
    // id:id++,
      path: "/dashboard",
      element:  <RecoilRoot><Dashboard /></RecoilRoot>,
     
    },
  {
    // id:id++,
      path: "/home",
      element:  <RecoilRoot><Home /> </RecoilRoot>,
     
    },
  {
    path: "/settings",
    element: <RecoilRoot><Settings /></RecoilRoot>

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
    element:  <RecoilRoot><Signin /></RecoilRoot>

  },
  {
    path: "/csignup",
    element: <ClientSignup />

  },
  {
    path: "/asignup",
    element: <AppSignup />

  },
  {
    path: "/welcome",
    element: <Welcome />

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
