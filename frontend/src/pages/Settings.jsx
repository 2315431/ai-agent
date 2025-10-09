import { useState } from 'react'
import { User, Key, Globe, Bell, Save } from 'lucide-react'
import toast from 'react-hot-toast'

const Settings = () => {
  const [activeTab, setActiveTab] = useState('profile')
  const [settings, setSettings] = useState({
    username: 'admin',
    email: 'admin@example.com',
    notifications: {
      email: true,
      browser: false,
      contentReady: true,
      errors: true
    },
    preferences: {
      defaultContentType: 'linkedin_post',
      defaultAudience: 'general',
      defaultTone: 'professional',
      autoGenerate: false
    }
  })

  const tabs = [
    { id: 'profile', label: 'Profile', icon: User },
    { id: 'preferences', label: 'Preferences', icon: Globe },
    { id: 'notifications', label: 'Notifications', icon: Bell },
    { id: 'api', label: 'API Keys', icon: Key }
  ]

  const handleSave = () => {
    // In a real app, this would save to backend
    localStorage.setItem('userSettings', JSON.stringify(settings))
    toast.success('Settings saved successfully!')
  }

  const updateSetting = (section, key, value) => {
    setSettings(prev => ({
      ...prev,
      [section]: {
        ...prev[section],
        [key]: value
      }
    }))
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
        <p className="text-gray-600 mt-2">Manage your account and preferences</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Settings Navigation */}
        <div className="lg:col-span-1">
          <div className="card">
            <nav className="space-y-2">
              {tabs.map((tab) => {
                const Icon = tab.icon
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`w-full flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors duration-200 ${
                      activeTab === tab.id
                        ? 'bg-primary-50 text-primary-700'
                        : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                    }`}
                  >
                    <Icon className="mr-3 h-5 w-5" />
                    {tab.label}
                  </button>
                )
              })}
            </nav>
          </div>
        </div>

        {/* Settings Content */}
        <div className="lg:col-span-3">
          <div className="card">
            {/* Profile Tab */}
            {activeTab === 'profile' && (
              <div className="space-y-6">
                <h3 className="text-lg font-semibold text-gray-900">Profile Information</h3>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Username
                    </label>
                    <input
                      type="text"
                      value={settings.username}
                      onChange={(e) => setSettings(prev => ({ ...prev, username: e.target.value }))}
                      className="input-field"
                      disabled
                    />
                    <p className="text-xs text-gray-500 mt-1">Username cannot be changed</p>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Email
                    </label>
                    <input
                      type="email"
                      value={settings.email}
                      onChange={(e) => setSettings(prev => ({ ...prev, email: e.target.value }))}
                      className="input-field"
                    />
                  </div>
                </div>

                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <h4 className="font-medium text-blue-900 mb-2">Account Security</h4>
                  <p className="text-blue-700 text-sm mb-3">
                    Your account is secured with JWT authentication. Password changes require admin access.
                  </p>
                  <button className="text-blue-600 hover:text-blue-700 text-sm font-medium">
                    Contact Administrator
                  </button>
                </div>
              </div>
            )}

            {/* Preferences Tab */}
            {activeTab === 'preferences' && (
              <div className="space-y-6">
                <h3 className="text-lg font-semibold text-gray-900">Content Generation Preferences</h3>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Default Content Type
                    </label>
                    <select
                      value={settings.preferences.defaultContentType}
                      onChange={(e) => updateSetting('preferences', 'defaultContentType', e.target.value)}
                      className="input-field"
                    >
                      <option value="linkedin_post">LinkedIn Post</option>
                      <option value="twitter_thread">Twitter Thread</option>
                      <option value="instagram_carousel">Instagram Carousel</option>
                      <option value="newsletter_section">Newsletter Section</option>
                    </select>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Default Audience
                    </label>
                    <select
                      value={settings.preferences.defaultAudience}
                      onChange={(e) => updateSetting('preferences', 'defaultAudience', e.target.value)}
                      className="input-field"
                    >
                      <option value="general">General Audience</option>
                      <option value="professionals">Professionals</option>
                      <option value="business_owners">Business Owners</option>
                      <option value="entrepreneurs">Entrepreneurs</option>
                      <option value="students">Students</option>
                    </select>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Default Tone
                    </label>
                    <select
                      value={settings.preferences.defaultTone}
                      onChange={(e) => updateSetting('preferences', 'defaultTone', e.target.value)}
                      className="input-field"
                    >
                      <option value="professional">Professional</option>
                      <option value="casual">Casual</option>
                      <option value="friendly">Friendly</option>
                      <option value="authoritative">Authoritative</option>
                      <option value="inspirational">Inspirational</option>
                    </select>
                  </div>
                  
                  <div className="flex items-center">
                    <input
                      type="checkbox"
                      id="autoGenerate"
                      checked={settings.preferences.autoGenerate}
                      onChange={(e) => updateSetting('preferences', 'autoGenerate', e.target.checked)}
                      className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                    />
                    <label htmlFor="autoGenerate" className="ml-2 text-sm text-gray-700">
                      Auto-generate multiple formats
                    </label>
                  </div>
                </div>
              </div>
            )}

            {/* Notifications Tab */}
            {activeTab === 'notifications' && (
              <div className="space-y-6">
                <h3 className="text-lg font-semibold text-gray-900">Notification Preferences</h3>
                
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-gray-700">Email Notifications</p>
                      <p className="text-xs text-gray-500">Receive notifications via email</p>
                    </div>
                    <input
                      type="checkbox"
                      checked={settings.notifications.email}
                      onChange={(e) => updateSetting('notifications', 'email', e.target.checked)}
                      className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                    />
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-gray-700">Browser Notifications</p>
                      <p className="text-xs text-gray-500">Show notifications in browser</p>
                    </div>
                    <input
                      type="checkbox"
                      checked={settings.notifications.browser}
                      onChange={(e) => updateSetting('notifications', 'browser', e.target.checked)}
                      className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                    />
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-gray-700">Content Ready</p>
                      <p className="text-xs text-gray-500">Notify when content is ready</p>
                    </div>
                    <input
                      type="checkbox"
                      checked={settings.notifications.contentReady}
                      onChange={(e) => updateSetting('notifications', 'contentReady', e.target.checked)}
                      className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                    />
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-gray-700">Error Alerts</p>
                      <p className="text-xs text-gray-500">Notify about errors and issues</p>
                    </div>
                    <input
                      type="checkbox"
                      checked={settings.notifications.errors}
                      onChange={(e) => updateSetting('notifications', 'errors', e.target.checked)}
                      className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                    />
                  </div>
                </div>
              </div>
            )}

            {/* API Keys Tab */}
            {activeTab === 'api' && (
              <div className="space-y-6">
                <h3 className="text-lg font-semibold text-gray-900">API Configuration</h3>
                
                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                  <h4 className="font-medium text-yellow-900 mb-2">API Access</h4>
                  <p className="text-yellow-700 text-sm mb-3">
                    Your API token is automatically managed. All requests are authenticated using JWT tokens.
                  </p>
                  <div className="bg-white rounded border p-3">
                    <code className="text-xs text-gray-600">
                      Authorization: Bearer [your-jwt-token]
                    </code>
                  </div>
                </div>

                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <h4 className="font-medium text-blue-900 mb-2">API Endpoints</h4>
                  <p className="text-blue-700 text-sm mb-3">
                    Your API base URL for external integrations:
                  </p>
                  <div className="bg-white rounded border p-3">
                    <code className="text-xs text-gray-600">
                      https://ai-agent-ikc8.onrender.com
                    </code>
                  </div>
                </div>

                <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                  <h4 className="font-medium text-green-900 mb-2">AI Services</h4>
                  <p className="text-green-700 text-sm">
                    Currently using free AI services (Hugging Face) with no API key required.
                  </p>
                </div>
              </div>
            )}

            {/* Save Button */}
            <div className="flex justify-end pt-6 border-t">
              <button onClick={handleSave} className="btn-primary flex items-center">
                <Save className="h-4 w-4 mr-2" />
                Save Settings
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Settings
