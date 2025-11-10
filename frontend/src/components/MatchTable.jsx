import React from 'react'

export default function MatchTable({matches, onShortlist, onReject, jobId}){
  const getStatusBadge = (status) => {
    const badgeClass = status === 'shortlisted' ? 'badge-success' 
                     : status === 'rejected' ? 'badge-danger' 
                     : 'badge-warning'
    return <span className={`badge ${badgeClass}`}>{status}</span>
  }

  const getScoreClass = (score) => {
    if (score >= 70) return 'score-high'
    if (score >= 50) return 'score-medium'
    return 'score-low'
  }

  if (!jobId) {
    return (
      <div className="card empty-state">
        <div className="empty-state-icon">📋</div>
        <h3>No Job Selected</h3>
        <p>Create a job posting to see candidate matches</p>
      </div>
    )
  }

  return (
    <div className="card fade-in">
      <div className="flex-between mb-3">
        <h3>👥 Candidate Matches</h3>
        <span style={{ 
          fontSize: '14px', 
          color: '#4a5568',
          background: '#f7fafc',
          padding: '6px 12px',
          borderRadius: '20px',
          fontWeight: '600'
        }}>
          {matches?.length || 0} Candidates
        </span>
      </div>

      {matches && matches.length > 0 ? (
        <div style={{ overflowX: 'auto' }}>
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Match Score</th>
                <th>Status</th>
                <th style={{ textAlign: 'center' }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {matches.map(m => (
                <tr key={m.candidate_id}>
                  <td style={{ fontWeight: '600', color: '#1a202c' }}>
                    {m.name || 'N/A'}
                  </td>
                  <td style={{ color: '#4a5568' }}>
                    {m.email || 'N/A'}
                  </td>
                  <td>
                    <span className={getScoreClass(m.score)} style={{ fontSize: '16px' }}>
                      {m.score}%
                    </span>
                  </td>
                  <td>{getStatusBadge(m.status)}</td>
                  <td>
                    <div className="flex-center gap-2">
                      <button 
                        onClick={() => onShortlist(m.candidate_id, jobId, m.score)}
                        disabled={m.status === 'shortlisted'}
                        className={m.status === 'shortlisted' ? 'btn-secondary' : 'btn-success'}
                        style={{ 
                          fontSize: '12px',
                          padding: '8px 16px'
                        }}
                      >
                        {m.status === 'shortlisted' ? '✓ Shortlisted' : '👍 Shortlist'}
                      </button>
                      <button 
                        onClick={() => onReject(m.candidate_id, jobId, m.score)}
                        disabled={m.status === 'rejected'}
                        className={m.status === 'rejected' ? 'btn-secondary' : 'btn-danger'}
                        style={{ 
                          fontSize: '12px',
                          padding: '8px 16px'
                        }}
                      >
                        {m.status === 'rejected' ? '✗ Rejected' : '👎 Reject'}
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="empty-state">
          <div className="empty-state-icon">🔍</div>
          <h3>No Matches Found</h3>
          <p>Upload resumes and create a job to see candidate matches</p>
        </div>
      )}

      {matches && matches.length > 0 && (
        <div style={{ 
          marginTop: '16px', 
          padding: '12px', 
          background: '#f7fafc', 
          borderRadius: '8px',
          fontSize: '13px',
          color: '#4a5568',
          display: 'flex',
          gap: '20px',
          justifyContent: 'space-around'
        }}>
          <div>
            <span className="score-high">●</span> High Match (≥70%)
          </div>
          <div>
            <span className="score-medium">●</span> Medium Match (50-69%)
          </div>
          <div>
            <span className="score-low">●</span> Low Match (&lt;50%)
          </div>
        </div>
      )}
    </div>
  )
}