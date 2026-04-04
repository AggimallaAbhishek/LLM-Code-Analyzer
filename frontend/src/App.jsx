import { Routes, Route } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import ProtectedRoute from './components/ProtectedRoute'
import LandingPage from './pages/LandingPage'
import Dashboard from './pages/Dashboard'
import LoginPage from './pages/LoginPage'

function App() {
  return (
    <AuthProvider>
      <div className="min-h-screen bg-[#0a0a0f] text-white">
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route 
            path="/" 
            element={
              <ProtectedRoute>
                <LandingPage />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/dashboard" 
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } 
          />
        </Routes>
      </div>
    </AuthProvider>
  )
}

export default App
