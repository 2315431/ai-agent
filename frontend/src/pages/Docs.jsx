import { useState } from 'react'
import { ExternalLink, Code, FileText, Zap } from 'lucide-react'

const Docs = () => {
  const [activeSection, setActiveSection] = useState('overview')

  const sections = [
    { id: 'overview', label: 'Overview', icon: FileText },
    { id: 'authentication', label: 'Authentication', icon: Code },
    { id: 'endpoints', label: 'API Endpoints', icon: Zap },
    { id: 'examples', label: 'Examples', icon: Code }
  ]

  const endpoints = [
    {
      method: 'POST',
      path: '/auth/login',
      description: 'Authenticate user and get JWT token',
      params: 'username, password'
    },
    {
      method: 'POST',
      path: '/content/upload',
      description: 'Upload content files',
      params: 'file (multipart/form-data)'
    },
    {
      method: 'GET',
      path: '/content/sources',
      description: 'List all uploaded content sources',
      params: 'Authorization header'
    },
    {
      method: 'POST',
      path: '/ai/generate',
      description: 'Generate AI-powered content',
      params: 'text, type, audience, tone'
    },
    {
      method: 'POST',
      path: '/demo/generate',
      description: 'Generate demo content (no AI)',
      params: 'text, type, audience, tone'
    },
    {
      method: 'GET',
      path: '/health',
      description: 'Check API health status',
      params: 'None'
    }
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">API Documentation</h1>
        <p className="text-gray-600 mt-2">Complete guide to using the Content Repurposing Agent API</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Navigation */}
        <div className="lg:col-span-1">
          <div className="card">
            <nav className="space-y-2">
              {sections.map((section) => {
                const Icon = section.icon
                return (
                  <button
                    key={section.id}
                    onClick={() => setActiveSection(section.id)}
                    className={`w-full flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors duration-200 ${
                      activeSection === section.id
                        ? 'bg-primary-50 text-primary-700'
                        : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                    }`}
                  >
                    <Icon className="mr-3 h-5 w-5" />
                    {section.label}
                  </button>
                )
              })}
            </nav>
          </div>
        </div>

        {/* Content */}
        <div className="lg:col-span-3">
          <div className="card">
            {/* Overview */}
            {activeSection === 'overview' && (
              <div className="space-y-6">
                <h3 className="text-lg font-semibold text-gray-900">API Overview</h3>
                
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <h4 className="font-medium text-blue-900 mb-2">Base URL</h4>
                  <code className="text-sm text-blue-700">https://ai-agent-ikc8.onrender.com</code>
                </div>

                <div>
                  <h4 className="font-medium text-gray-900 mb-3">Features</h4>
                  <ul className="space-y-2 text-sm text-gray-700">
                    <li className="flex items-center">
                      <span className="w-2 h-2 bg-green-500 rounded-full mr-3"></span>
                      Content upload and management
                    </li>
                    <li className="flex items-center">
                      <span className="w-2 h-2 bg-green-500 rounded-full mr-3"></span>
                      AI-powered content generation
                    </li>
                    <li className="flex items-center">
                      <span className="w-2 h-2 bg-green-500 rounded-full mr-3"></span>
                      Multiple content formats (LinkedIn, Twitter, Instagram, Newsletter)
                    </li>
                    <li className="flex items-center">
                      <span className="w-2 h-2 bg-green-500 rounded-full mr-3"></span>
                      JWT authentication
                    </li>
                    <li className="flex items-center">
                      <span className="w-2 h-2 bg-green-500 rounded-full mr-3"></span>
                      RESTful API design
                    </li>
                  </ul>
                </div>

                <div>
                  <h4 className="font-medium text-gray-900 mb-3">Content Types Supported</h4>
                  <div className="grid grid-cols-2 gap-3 text-sm">
                    <div className="bg-gray-50 p-3 rounded-lg">
                      <strong>Input:</strong> TXT, MD, PDF, MP4, MP3, WAV
                    </div>
                    <div className="bg-gray-50 p-3 rounded-lg">
                      <strong>Output:</strong> LinkedIn, Twitter, Instagram, Newsletter
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Authentication */}
            {activeSection === 'authentication' && (
              <div className="space-y-6">
                <h3 className="text-lg font-semibold text-gray-900">Authentication</h3>
                
                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                  <h4 className="font-medium text-yellow-900 mb-2">JWT Token Authentication</h4>
                  <p className="text-yellow-700 text-sm mb-3">
                    All API endpoints (except login and health) require a valid JWT token in the Authorization header.
                  </p>
                </div>

                <div>
                  <h4 className="font-medium text-gray-900 mb-3">Getting a Token</h4>
                  <div className="bg-gray-900 text-green-400 p-4 rounded-lg text-sm overflow-x-auto">
                    <pre>{`POST /auth/login?username=admin&password=darshan@2003

Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}`}</pre>
                  </div>
                </div>

                <div>
                  <h4 className="font-medium text-gray-900 mb-3">Using the Token</h4>
                  <div className="bg-gray-900 text-green-400 p-4 rounded-lg text-sm overflow-x-auto">
                    <pre>{`Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

Example:
curl -H "Authorization: Bearer YOUR_TOKEN" \\
     https://ai-agent-ikc8.onrender.com/content/sources`}</pre>
                  </div>
                </div>
              </div>
            )}

            {/* Endpoints */}
            {activeSection === 'endpoints' && (
              <div className="space-y-6">
                <h3 className="text-lg font-semibold text-gray-900">API Endpoints</h3>
                
                <div className="space-y-4">
                  {endpoints.map((endpoint, index) => (
                    <div key={index} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center space-x-3">
                          <span className={`px-2 py-1 text-xs font-medium rounded ${
                            endpoint.method === 'GET' 
                              ? 'bg-green-100 text-green-800'
                              : 'bg-blue-100 text-blue-800'
                          }`}>
                            {endpoint.method}
                          </span>
                          <code className="text-sm font-mono text-gray-800">{endpoint.path}</code>
                        </div>
                        <a
                          href={`https://ai-agent-ikc8.onrender.com${endpoint.path}`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-gray-400 hover:text-gray-600"
                        >
                          <ExternalLink className="h-4 w-4" />
                        </a>
                      </div>
                      <p className="text-sm text-gray-600 mb-2">{endpoint.description}</p>
                      <p className="text-xs text-gray-500">
                        <strong>Parameters:</strong> {endpoint.params}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Examples */}
            {activeSection === 'examples' && (
              <div className="space-y-6">
                <h3 className="text-lg font-semibold text-gray-900">Usage Examples</h3>
                
                <div>
                  <h4 className="font-medium text-gray-900 mb-3">1. Upload Content</h4>
                  <div className="bg-gray-900 text-green-400 p-4 rounded-lg text-sm overflow-x-auto">
                    <pre>{`curl -X POST \\
  -H "Authorization: Bearer YOUR_TOKEN" \\
  -F "file=@your-content.txt" \\
  https://ai-agent-ikc8.onrender.com/content/upload`}</pre>
                  </div>
                </div>

                <div>
                  <h4 className="font-medium text-gray-900 mb-3">2. Generate AI Content</h4>
                  <div className="bg-gray-900 text-green-400 p-4 rounded-lg text-sm overflow-x-auto">
                    <pre>{`curl -X POST \\
  -H "Authorization: Bearer YOUR_TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{
    "text": "Your content here...",
    "type": "linkedin_post",
    "audience": "professionals",
    "tone": "professional"
  }' \\
  https://ai-agent-ikc8.onrender.com/ai/generate`}</pre>
                  </div>
                </div>

                <div>
                  <h4 className="font-medium text-gray-900 mb-3">3. List Content Sources</h4>
                  <div className="bg-gray-900 text-green-400 p-4 rounded-lg text-sm overflow-x-auto">
                    <pre>{`curl -H "Authorization: Bearer YOUR_TOKEN" \\
     https://ai-agent-ikc8.onrender.com/content/sources`}</pre>
                  </div>
                </div>

                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <h4 className="font-medium text-blue-900 mb-2">Interactive API Testing</h4>
                  <p className="text-blue-700 text-sm mb-3">
                    You can test all endpoints interactively using the Swagger UI:
                  </p>
                  <a
                    href="https://ai-agent-ikc8.onrender.com/docs"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="btn-primary text-sm inline-flex items-center"
                  >
                    <ExternalLink className="h-4 w-4 mr-2" />
                    Open Swagger UI
                  </a>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Docs
