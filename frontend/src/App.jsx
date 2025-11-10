import React, {useState} from 'react'
import UploadForm from './components/UploadForm'
import JobForm from './components/JobForm'
import MatchTable from './components/MatchTable'
import Dashboard from './components/Dashboard'
import axios from 'axios'
import { API_BASE_URL } from './config'

export default function App(){
  const [jobId, setJobId] = useState(null)
  const [matches, setMatches] = useState([])
  const [activeTab, setActiveTab] = useState('matches') // 'matches' or 'dashboard'
  const [loading, setLoading] = useState(false)

  const createJob = async (title, description) => {
    setLoading(true)
    try {
      const res = await axios.post(`${API_BASE_URL}/job`, {title, description})
      const newJobId = res.data.job_id
      setJobId(newJobId)
      return newJobId
    } catch (error) {
      console.error('Error creating job:', error)
      alert('Failed to create job. Please try again.')
      return null
    } finally {
      setLoading(false)
    }
  }

  const fetchMatches = async (id) => {
    if (!id) return
    setLoading(true)
    try {
      const res = await axios.get(`${API_BASE_URL}/match/${id}`)
      setMatches(res.data)
    } catch (error) {
      console.error('Error fetching matches:', error)
      alert('Failed to fetch matches. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleShortlist = async (candidateId, jobId, score) => {
    try {
      const sendEmail = window.confirm(
        '✉️ Send Email Notification?\n\n' +
        'Would you like to send a congratulatory email to the candidate?\n\n' +
        '(Note: Requires SMTP configuration in backend)'
      )
      
      setLoading(true)
      await axios.post(`${API_BASE_URL}/application/shortlist`, {
        candidate_id: candidateId,
        job_id: jobId,
        score: score,
        send_email: sendEmail
      })
      
      // Refresh matches to update status
      await fetchMatches(jobId)
      
      const message = sendEmail 
        ? '✅ Candidate shortlisted and email sent successfully!' 
        : '✅ Candidate shortlisted successfully!'
      
      // Show success message
      const alertDiv = document.createElement('div')
      alertDiv.className = 'alert alert-success fade-in'
      alertDiv.textContent = message
      alertDiv.style.position = 'fixed'
      alertDiv.style.top = '20px'
      alertDiv.style.right = '20px'
      alertDiv.style.zIndex = '9999'
      document.body.appendChild(alertDiv)
      setTimeout(() => alertDiv.remove(), 3000)
      
    } catch (error) {
      console.error('Error shortlisting candidate:', error)
      alert('❌ Failed to shortlist candidate. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleReject = async (candidateId, jobId, score) => {
    if (!window.confirm('⚠️ Reject Candidate?\n\nAre you sure you want to reject this candidate?')) {
      return
    }
    
    try {
      setLoading(true)
      await axios.post(`${API_BASE_URL}/application/reject`, {
        candidate_id: candidateId,
        job_id: jobId,
        score: score
      })
      
      // Refresh matches to update status
      await fetchMatches(jobId)
      
      // Show success message
      const alertDiv = document.createElement('div')
      alertDiv.className = 'alert alert-info fade-in'
      alertDiv.textContent = '✅ Candidate rejected'
      alertDiv.style.position = 'fixed'
      alertDiv.style.top = '20px'
      alertDiv.style.right = '20px'
      alertDiv.style.zIndex = '9999'
      document.body.appendChild(alertDiv)
      setTimeout(() => alertDiv.remove(), 3000)
      
    } catch (error) {
      console.error('Error rejecting candidate:', error)
      alert('❌ Failed to reject candidate. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>🎯 HireIQ</h1>
        <p>Smart Recruitment Platform - Match, Shortlist, Hire</p>
      </header>

      <div className="grid-layout">
        <div>
          <UploadForm />
        </div>
        
        <div>
          <JobForm 
            onCreateJob={async (t,d)=>{ 
              const newJobId = await createJob(t,d); 
              if (newJobId) {
                await fetchMatches(newJobId);
                setActiveTab('matches');
              }
            }} 
            loading={loading}
          />
          
          {/* Tab Navigation */}
          {jobId && (
            <div className="tab-container">
              <button
                className={`tab-button ${activeTab === 'matches' ? 'active' : ''}`}
                onClick={() => setActiveTab('matches')}
              >
                📋 All Matches
              </button>
              <button
                className={`tab-button ${activeTab === 'dashboard' ? 'active' : ''}`}
                onClick={() => setActiveTab('dashboard')}
              >
                📊 Dashboard
              </button>
            </div>
          )}

          {/* Content based on active tab */}
          {loading ? (
            <div className="card">
              <div className="spinner"></div>
              <p className="text-center">Loading...</p>
            </div>
          ) : activeTab === 'matches' ? (
            <MatchTable 
              matches={matches} 
              onShortlist={handleShortlist}
              onReject={handleReject}
              jobId={jobId}
            />
          ) : (
            <Dashboard jobId={jobId} />
          )}
        </div>
      </div>
    </div>
  )
}