import React, { useState, useEffect } from 'react'
import axios from 'axios'

export default function Dashboard({ jobId }) {
  const [topMatches, setTopMatches] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (jobId) {
      fetchDashboardData()
    }
  }, [jobId])

  const fetchDashboardData = async () => {
    if (!jobId) return
    
    setLoading(true)
    try {
      const [matchesRes, statsRes] = await Promise.all([
        axios.get(`http://127.0.0.1:5000/dashboard/top-matches/${jobId}?limit=10`),
        axios.get(`http://127.0.0.1:5000/dashboard/stats/${jobId}`)
      ])
      
      setTopMatches(matchesRes.data.top_matches || [])
      setStats(statsRes.data)
    } catch (error) {
      console.error('Error fetching dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  const getScoreClass = (score) => {
    if (score >= 70) return 'score-high'
    if (score >= 50) return 'score-medium'
    return 'score-low'
  }

  if (!jobId) {
    return (
      <div className="card empty-state">
        <div className="empty-state-icon">📊</div>
        <h3>Dashboard Not Available</h3>
        <p>Create a job posting to view the recruitment dashboard</p>
      </div>
    )
  }

  return (
    <div className="fade-in">
      <div className="card">
        <div className="flex-between mb-4">
          <div>
            <h3 style={{ marginBottom: '4px' }}>📊 Recruitment Dashboard</h3>
            <p style={{ fontSize: '14px', color: '#4a5568', margin: 0 }}>
              {stats?.job_title || 'Loading...'}
            </p>
          </div>
          <button 
            onClick={fetchDashboardData} 
            className="btn-outline"
            disabled={loading}
          >
            {loading ? '⟳ Refreshing...' : '🔄 Refresh'}
          </button>
        </div>

        {loading && !stats ? (
          <div className="text-center">
            <div className="spinner"></div>
            <p>Loading dashboard data...</p>
          </div>
        ) : (
          <>
            {/* Statistics Cards */}
            {stats && (
              <div className="stats-grid">
                <div className="stat-card blue">
                  <div className="stat-number" style={{ color: '#667eea' }}>
                    {stats.total_applications}
                  </div>
                  <div className="stat-label">Total Applications</div>
                </div>
                <div className="stat-card green">
                  <div className="stat-number" style={{ color: '#48bb78' }}>
                    {stats.shortlisted}
                  </div>
                  <div className="stat-label">Shortlisted</div>
                </div>
                <div className="stat-card yellow">
                  <div className="stat-number" style={{ color: '#ed8936' }}>
                    {stats.pending}
                  </div>
                  <div className="stat-label">Pending Review</div>
                </div>
                <div className="stat-card red">
                  <div className="stat-number" style={{ color: '#f56565' }}>
                    {stats.rejected}
                  </div>
                  <div className="stat-label">Rejected</div>
                </div>
              </div>
            )}

            {/* Top Matches Table */}
            <div style={{ marginTop: '30px' }}>
              <h4 style={{ 
                fontSize: '18px', 
                fontWeight: '600', 
                marginBottom: '16px',
                color: '#1a202c'
              }}>
                🏆 Top 10 Candidates
              </h4>
              
              {topMatches.length > 0 ? (
                <div style={{ overflowX: 'auto' }}>
                  <table>
                    <thead>
                      <tr>
                        <th style={{ width: '60px' }}>Rank</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Score</th>
                        <th>Status</th>
                      </tr>
                    </thead>
                    <tbody>
                      {topMatches.map((match, index) => (
                        <tr key={match.candidate_id}>
                          <td>
                            <div style={{
                              display: 'inline-flex',
                              alignItems: 'center',
                              justifyContent: 'center',
                              width: '32px',
                              height: '32px',
                              borderRadius: '50%',
                              background: index < 3 
                                ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                                : '#e2e8f0',
                              color: index < 3 ? 'white' : '#4a5568',
                              fontWeight: '700',
                              fontSize: '14px'
                            }}>
                              {index + 1}
                            </div>
                          </td>
                          <td style={{ fontWeight: '600', color: '#1a202c' }}>
                            {match.name || 'N/A'}
                          </td>
                          <td style={{ color: '#4a5568' }}>
                            {match.email || 'N/A'}
                          </td>
                          <td>
                            <span className={getScoreClass(match.score)} style={{ fontSize: '16px' }}>
                              {match.score}%
                            </span>
                          </td>
                          <td>
                            <span className={`badge ${
                              match.status === 'shortlisted' ? 'badge-success' :
                              match.status === 'rejected' ? 'badge-danger' : 'badge-warning'
                            }`}>
                              {match.status}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <div className="empty-state">
                  <div className="empty-state-icon">🔍</div>
                  <h3>No Candidates Found</h3>
                  <p>Upload resumes to see top matching candidates</p>
                </div>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  )
}
