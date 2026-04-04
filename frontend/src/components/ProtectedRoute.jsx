import { Navigate, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { motion } from 'framer-motion'
import { Shield } from 'lucide-react'

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth()
  const location = useLocation()

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0a0a0f] flex flex-col items-center justify-center">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 1.5, repeat: Infinity, ease: 'linear' }}
          className="relative w-16 h-16"
        >
          <div className="absolute inset-0 border-4 border-cyan-500/30 border-t-cyan-500 rounded-full" />
          <Shield className="absolute inset-0 m-auto w-6 h-6 text-cyan-400" />
        </motion.div>
        <motion.p
          animate={{ opacity: [1, 0.5, 1] }}
          transition={{ duration: 1.5, repeat: Infinity }}
          className="mt-4 text-gray-400"
        >
          Checking authentication...
        </motion.p>
      </div>
    )
  }

  if (!isAuthenticated) {
    // Redirect to login, preserving the intended destination
    return <Navigate to="/login" state={{ from: location }} replace />
  }

  return children
}

export default ProtectedRoute
