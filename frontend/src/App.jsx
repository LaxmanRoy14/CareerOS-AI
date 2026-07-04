import { Routes, Route } from "react-router-dom";

import Landing from "./pages/Landing";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import ResumeAnalysis from "./pages/ResumeAnalysis";
import MockInterview from "./pages/MockInterview";
import InterviewHistory from "./pages/InterviewHistory";
import Profile from "./pages/Profile";
import NotFound from "./pages/Notfound";

import ProtectedRoute from "./components/ProtectedRoute";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        }
      />

      <Route path="/resume-analysis" element={<ResumeAnalysis />} />
      <Route path="/mock-interview" element={<MockInterview />} />
      <Route path="/interview-history" element={<InterviewHistory />} />
      <Route path="/profile" element={<Profile />} />

      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}

export default App;