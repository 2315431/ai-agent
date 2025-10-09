import { useState, useRef } from 'react'
import { Upload as UploadIcon, File, X, CheckCircle } from 'lucide-react'
import { contentAPI } from '../services/api'
import toast from 'react-hot-toast'

const Upload = () => {
  const [dragActive, setDragActive] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [uploadedFiles, setUploadedFiles] = useState([])
  const fileInputRef = useRef(null)

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFiles(e.dataTransfer.files)
    }
  }

  const handleChange = (e) => {
    e.preventDefault()
    if (e.target.files && e.target.files[0]) {
      handleFiles(e.target.files)
    }
  }

  const handleFiles = async (files) => {
    const fileArray = Array.from(files)
    
    for (const file of fileArray) {
      if (file.size > 10 * 1024 * 1024) { // 10MB limit
        toast.error(`File ${file.name} is too large. Maximum size is 10MB.`)
        continue
      }

      const allowedTypes = ['text/plain', 'text/markdown', 'application/pdf', 'video/mp4', 'audio/mp3', 'audio/wav']
      if (!allowedTypes.includes(file.type)) {
        toast.error(`File ${file.name} has unsupported format.`)
        continue
      }

      setUploading(true)
      
      try {
        const formData = new FormData()
        formData.append('file', file)
        
        const response = await contentAPI.upload(formData)
        
        setUploadedFiles(prev => [...prev, {
          ...response.data,
          file: file
        }])
        
        toast.success(`${file.name} uploaded successfully!`)
      } catch (error) {
        toast.error(`Failed to upload ${file.name}`)
      } finally {
        setUploading(false)
      }
    }
  }

  const removeFile = (id) => {
    setUploadedFiles(prev => prev.filter(file => file.id !== id))
  }

  const triggerFileInput = () => {
    fileInputRef.current?.click()
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Upload Content</h1>
        <p className="text-gray-600 mt-2">Upload your content to generate AI-powered social media posts</p>
      </div>

      {/* Upload Area */}
      <div className="card">
        <div
          className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors duration-200 ${
            dragActive
              ? 'border-primary-500 bg-primary-50'
              : 'border-gray-300 hover:border-gray-400'
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <input
            ref={fileInputRef}
            type="file"
            multiple
            accept=".txt,.md,.pdf,.mp4,.mp3,.wav"
            onChange={handleChange}
            className="hidden"
          />
          
          <UploadIcon className="mx-auto h-12 w-12 text-gray-400 mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Upload your content
          </h3>
          <p className="text-gray-600 mb-4">
            Drag and drop files here, or click to browse
          </p>
          
          <button
            type="button"
            onClick={triggerFileInput}
            className="btn-primary"
            disabled={uploading}
          >
            {uploading ? 'Uploading...' : 'Choose Files'}
          </button>
          
          <p className="text-sm text-gray-500 mt-4">
            Supported formats: TXT, MD, PDF, MP4, MP3, WAV (Max 10MB)
          </p>
        </div>
      </div>

      {/* Uploaded Files */}
      {uploadedFiles.length > 0 && (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Uploaded Files</h3>
          <div className="space-y-3">
            {uploadedFiles.map((fileData) => (
              <div key={fileData.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center">
                  <div className="p-2 bg-green-100 rounded-lg mr-3">
                    <CheckCircle className="h-5 w-5 text-green-600" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-900">{fileData.title}</p>
                    <p className="text-xs text-gray-500">
                      {fileData.source_type} • {fileData.file_size} bytes
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => removeFile(fileData.id)}
                  className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg"
                >
                  <X className="h-4 w-4" />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Next Steps */}
      {uploadedFiles.length > 0 && (
        <div className="card bg-primary-50 border-primary-200">
          <div className="flex items-start">
            <div className="p-2 bg-primary-100 rounded-lg mr-3">
              <File className="h-5 w-5 text-primary-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-primary-900 mb-2">
                Ready for AI Generation!
              </h3>
              <p className="text-primary-700 mb-4">
                Your content has been uploaded successfully. Now you can generate AI-powered social media posts from your content.
              </p>
              <a
                href="/generate"
                className="btn-primary"
              >
                Generate Content
              </a>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default Upload
