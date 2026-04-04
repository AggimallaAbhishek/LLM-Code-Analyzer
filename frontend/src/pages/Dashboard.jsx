import { useState } from 'react'
import { motion } from 'framer-motion'
import { Shield, Play, Trash2, FileCode, Download, Upload, Zap } from 'lucide-react'
import { Link } from 'react-router-dom'
import CodeEditor from '../components/CodeEditor'
import ResultsPanel from '../components/ResultsPanel'
import GlowButton from '../components/GlowButton'

const SAMPLE_CODE = `# Example vulnerable Python code
import os
import pickle
import sqlite3

def get_user(user_id):
    # SQL Injection vulnerability
    conn = sqlite3.connect('users.db')
    query = "SELECT * FROM users WHERE id = '" + user_id + "'"
    result = conn.execute(query)
    return result.fetchone()

def run_command(cmd):
    # Command injection vulnerability
    os.system("echo " + cmd)

def process_data(data):
    # Insecure deserialization
    obj = pickle.loads(data)
    return obj

# Hardcoded credentials
API_KEY = "sk-1234567890abcdef"
PASSWORD = "admin123"

def dangerous_eval(user_input):
    # Arbitrary code execution
    result = eval(user_input)
    return result
`

const Dashboard = () => {
  const [code, setCode] = useState('')
  const [language, setLanguage] = useState('python')
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)

  const analyzeCode = async () => {
    if (!code.trim()) {
      setError('Please enter some code to analyze')
      return
    }

    setIsAnalyzing(true)
    setError(null)
    setResults(null)

    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code, language })
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Analysis failed')
      }

      if (!data.success) {
        throw new Error(data.error || 'Analysis failed')
      }

      setResults(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setIsAnalyzing(false)
    }
  }

  const loadSample = () => {
    setCode(SAMPLE_CODE)
    setLanguage('python')
    setResults(null)
    setError(null)
  }

  const clearAll = () => {
    setCode('')
    setResults(null)
    setError(null)
  }

  const downloadReport = () => {
    if (!results) return
    const report = JSON.stringify(results, null, 2)
    const blob = new Blob([report], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'security-report.json'
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="min-h-screen bg-[#0a0a0f]">
      {/* Background Effects */}
      <div className="fixed inset-0 bg-grid opacity-30" />
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-cyan-500/5 rounded-full blur-3xl" />
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-purple-500/5 rounded-full blur-3xl" />
      </div>

      {/* Header */}
      <motion.header
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="relative z-10 glass border-b border-white/10"
      >
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <Link to="/" className="flex items-center gap-3">
              <div className="relative">
                <Shield className="w-8 h-8 text-cyan-400" />
                <Zap className="w-4 h-4 text-purple-400 absolute -bottom-1 -right-1" />
              </div>
              <span className="text-xl font-bold text-gradient">SecureCodeAI</span>
            </Link>

            <div className="flex items-center gap-4">
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-gray-300 focus:outline-none focus:border-cyan-500"
              >
                <option value="python">Python</option>
                <option value="javascript">JavaScript</option>
                <option value="java">Java</option>
                <option value="c">C/C++</option>
                <option value="php">PHP</option>
                <option value="auto">Auto-detect</option>
              </select>

              <Link
                to="/"
                className="text-gray-400 hover:text-white transition-colors"
              >
                Home
              </Link>
            </div>
          </div>
        </div>
      </motion.header>

      {/* Main Content */}
      <main className="relative z-10 max-w-7xl mx-auto px-6 py-8">
        <div className="grid lg:grid-cols-2 gap-8">
          {/* Left Panel - Code Editor */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.1 }}
            className="space-y-4"
          >
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold text-white flex items-center gap-2">
                <FileCode className="w-5 h-5 text-cyan-400" />
                Code Input
              </h2>
              <div className="flex items-center gap-2">
                <button
                  onClick={loadSample}
                  className="px-3 py-1.5 text-sm text-gray-400 hover:text-white hover:bg-white/10 rounded-lg transition-colors flex items-center gap-1"
                >
                  <Upload className="w-4 h-4" />
                  Load Sample
                </button>
                <button
                  onClick={clearAll}
                  className="px-3 py-1.5 text-sm text-gray-400 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-colors flex items-center gap-1"
                >
                  <Trash2 className="w-4 h-4" />
                  Clear
                </button>
              </div>
            </div>

            <CodeEditor
              value={code}
              onChange={setCode}
              language={language}
            />

            {/* Action Buttons */}
            <div className="flex items-center gap-4">
              <GlowButton
                onClick={analyzeCode}
                loading={isAnalyzing}
                disabled={!code.trim()}
                className="flex-1"
              >
                <Play className="w-5 h-5" />
                {isAnalyzing ? 'Analyzing...' : 'Analyze Code'}
              </GlowButton>

              {results && (
                <motion.button
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  onClick={downloadReport}
                  className="px-4 py-3 bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl transition-colors flex items-center gap-2 text-gray-300"
                >
                  <Download className="w-5 h-5" />
                  Export
                </motion.button>
              )}
            </div>

            {/* Error Display */}
            {error && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-red-500/10 border border-red-500/30 rounded-xl p-4"
              >
                <p className="text-red-400">⚠️ {error}</p>
              </motion.div>
            )}
          </motion.div>

          {/* Right Panel - Results */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
          >
            {!results && !isAnalyzing ? (
              <div className="glass rounded-xl p-12 text-center h-full flex flex-col items-center justify-center">
                <motion.div
                  animate={{ 
                    scale: [1, 1.1, 1],
                    rotate: [0, 5, -5, 0]
                  }}
                  transition={{ duration: 4, repeat: Infinity }}
                  className="w-24 h-24 mb-6 rounded-2xl bg-gradient-to-br from-cyan-500/20 to-purple-500/20 flex items-center justify-center"
                >
                  <Shield className="w-12 h-12 text-cyan-400" />
                </motion.div>
                <h3 className="text-xl font-semibold text-white mb-2">
                  Ready to Analyze
                </h3>
                <p className="text-gray-400 max-w-sm">
                  Paste your code in the editor and click "Analyze Code" to detect security vulnerabilities.
                </p>
                <div className="mt-6 flex flex-wrap gap-2 justify-center">
                  {['SQL Injection', 'XSS', 'Command Injection', 'Hardcoded Secrets'].map((tag) => (
                    <span key={tag} className="px-3 py-1 bg-white/5 text-gray-500 rounded-full text-sm">
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            ) : (
              <ResultsPanel results={results} isLoading={isAnalyzing} />
            )}
          </motion.div>
        </div>

        {/* Scanning Animation Overlay */}
        {isAnalyzing && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 pointer-events-none z-50"
          >
            <motion.div
              className="absolute left-0 right-0 h-0.5 bg-gradient-to-r from-transparent via-cyan-500 to-transparent"
              animate={{ top: ['0%', '100%'] }}
              transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
            />
          </motion.div>
        )}
      </main>

      {/* Footer */}
      <footer className="relative z-10 border-t border-white/10 mt-12 py-6 px-6">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4 text-sm text-gray-500">
          <p>SecureCodeAI — AI-Powered Code Security Analysis</p>
          <p>Hybrid Analysis: LLM + Static Rules</p>
        </div>
      </footer>
    </div>
  )
}

export default Dashboard
