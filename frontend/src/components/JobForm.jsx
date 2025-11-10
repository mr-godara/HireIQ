import React, {useState} from 'react'

export default function JobForm({onCreateJob, loading}){
  const [title, setTitle] = useState('')
  const [desc, setDesc] = useState('')

  const handleSubmit = () => {
    if (!title.trim()) {
      alert('⚠️ Please enter a job title')
      return
    }
    if (!desc.trim()) {
      alert('⚠️ Please enter a job description')
      return
    }
    onCreateJob(title, desc)
  }

  return (
    <div className="card fade-in">
      <h3>💼 Create Job Posting</h3>
      
      <div className="mb-3">
        <label style={{ 
          display: 'block', 
          marginBottom: '8px', 
          fontWeight: '600',
          color: '#4a5568',
          fontSize: '14px'
        }}>
          Job Title *
        </label>
        <input 
          type="text"
          placeholder="e.g., Senior Software Engineer" 
          value={title} 
          onChange={(e)=>setTitle(e.target.value)}
          disabled={loading}
        />
      </div>

      <div className="mb-3">
        <label style={{ 
          display: 'block', 
          marginBottom: '8px', 
          fontWeight: '600',
          color: '#4a5568',
          fontSize: '14px'
        }}>
          Job Description *
        </label>
        <textarea 
          placeholder="Enter detailed job requirements, required skills, experience level, etc.&#10;&#10;Example:&#10;- 5+ years of Python experience&#10;- React and JavaScript expertise&#10;- Team leadership skills&#10;- Bachelor's degree in Computer Science" 
          value={desc} 
          onChange={(e)=>setDesc(e.target.value)}
          disabled={loading}
          style={{ minHeight: '150px' }}
        />
      </div>

      <button 
        onClick={handleSubmit}
        className="btn-primary"
        disabled={loading}
        style={{ width: '100%' }}
      >
        {loading ? (
          <>
            <span className="spinner" style={{ 
              width: '16px', 
              height: '16px', 
              borderWidth: '2px',
              margin: 0 
            }}></span>
            Processing...
          </>
        ) : (
          <>
            🎯 Create Job & Find Matches
          </>
        )}
      </button>

      {!title && !desc && (
        <div style={{ 
          marginTop: '16px', 
          padding: '12px', 
          background: '#f7fafc', 
          borderRadius: '8px',
          fontSize: '13px',
          color: '#4a5568'
        }}>
          <p style={{ marginBottom: '4px', fontWeight: '600' }}>💡 Pro Tip:</p>
          <p style={{ lineHeight: '1.6' }}>
            Be specific with requirements to get better matches. Include key skills, 
            technologies, experience levels, and qualifications.
          </p>
        </div>
      )}
    </div>
  )
}