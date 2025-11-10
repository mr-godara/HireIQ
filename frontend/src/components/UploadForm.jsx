import React, { useState } from 'react'
import axios from 'axios'

export default function UploadForm(){
  const [selectedFile, setSelectedFile] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [message, setMessage] = useState(null)

  const handleFileChange = (e) => {
    const file = e.target.files[0]
    setSelectedFile(file)
    setMessage(null)
  }

  const handleUpload = async (e) => {
    e.preventDefault()
    
    if (!selectedFile) {
      setMessage({ type: 'error', text: 'Please select a file first' })
      return
    }

    setUploading(true)
    setMessage(null)

    try {
      const fd = new FormData()
      fd.append('resume', selectedFile)
      const res = await axios.post('http://127.0.0.1:5000/upload', fd)
      
      setMessage({ 
        type: 'success', 
        text: `✅ Resume uploaded successfully! Candidate ID: ${res.data.candidate_id}` 
      })
      setSelectedFile(null)
      e.target.reset()
    } catch (error) {
      console.error('Upload error:', error)
      setMessage({ 
        type: 'error', 
        text: '❌ Failed to upload resume. Please try again.' 
      })
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="card fade-in">
      <h3>📄 Upload Resume</h3>
      
      {message && (
        <div className={`alert alert-${message.type === 'success' ? 'success' : 'error'} mb-3`}>
          {message.text}
        </div>
      )}

      <form onSubmit={handleUpload}>
        <div className="mb-3">
          <label style={{ 
            display: 'block', 
            marginBottom: '8px', 
            fontWeight: '600',
            color: '#4a5568',
            fontSize: '14px'
          }}>
            Select Resume (PDF or DOCX)
          </label>
          <input 
            type="file" 
            name="resume" 
            accept=".pdf,.docx,.doc" 
            onChange={handleFileChange}
            disabled={uploading}
            style={{
              border: selectedFile ? '2px solid #48bb78' : '2px solid #e2e8f0'
            }}
          />
          {selectedFile && (
            <p style={{ 
              marginTop: '8px', 
              fontSize: '13px', 
              color: '#48bb78',
              display: 'flex',
              alignItems: 'center',
              gap: '6px'
            }}>
              ✓ {selectedFile.name} ({(selectedFile.size / 1024).toFixed(2)} KB)
            </p>
          )}
        </div>

        <button 
          type="submit" 
          className="btn-primary"
          disabled={uploading || !selectedFile}
          style={{ width: '100%' }}
        >
          {uploading ? (
            <>
              <span className="spinner" style={{ 
                width: '16px', 
                height: '16px', 
                borderWidth: '2px',
                margin: 0 
              }}></span>
              Uploading...
            </>
          ) : (
            <>
              📤 Upload Resume
            </>
          )}
        </button>
      </form>

      <div style={{ 
        marginTop: '16px', 
        padding: '12px', 
        background: '#f7fafc', 
        borderRadius: '8px',
        fontSize: '13px',
        color: '#4a5568'
      }}>
        <p style={{ marginBottom: '4px', fontWeight: '600' }}>💡 Tips:</p>
        <ul style={{ marginLeft: '20px', lineHeight: '1.6' }}>
          <li>Accepted formats: PDF, DOCX</li>
          <li>Max file size: 10 MB</li>
          <li>Ensure resume contains email address</li>
        </ul>
      </div>
    </div>
  )
}