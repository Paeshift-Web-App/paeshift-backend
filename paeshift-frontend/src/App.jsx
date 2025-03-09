import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import JobDetail from "./components/jobdetail/JobDetail"; // The file below

function App() {
  return (
    <Router>
      <Routes>
        {/* ...other routes... */}
        <Route path="/jobs/:jobId" element={<JobDetail />} />
      </Routes>
    </Router>
  );
}

export default App;
