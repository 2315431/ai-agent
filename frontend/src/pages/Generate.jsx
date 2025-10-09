import { useState, useEffect } from 'react'
import { Zap, FileText, Copy, Download, RefreshCw } from 'lucide-react'
import { contentAPI, generationAPI } from '../services/api'
import toast from 'react-hot-toast'

const Generate = () => {
  const [contentSources, setContentSources] = useState([])
  const [selectedSource, setSelectedSource] = useState('')
  const [contentType, setContentType] = useState('linkedin_post')
  const [targetAudience, setTargetAudience] = useState('general')
  const [tone, setTone] = useState('professional')
  const [customText, setCustomText] = useState('')
  const [generating, setGenerating] = useState(false)
  const [generatedContent, setGeneratedContent] = useState(null)

  const contentTypes = [
    { value: 'linkedin_post', label: 'LinkedIn Post' },
    { value: 'twitter_thread', label: 'Twitter Thread' },
    { value: 'instagram_carousel', label: 'Instagram Carousel' },
    { value: 'newsletter_section', label: 'Newsletter Section' }
  ]

  const audiences = [
    { value: 'general', label: 'General Audience' },
    { value: 'professionals', label: 'Professionals' },
    { value: 'business_owners', label: 'Business Owners' },
    { value: 'entrepreneurs', label: 'Entrepreneurs' },
    { value: 'students', label: 'Students' }
  ]

  const tones = [
    { value: 'professional', label: 'Professional' },
    { value: 'casual', label: 'Casual' },
    { value: 'friendly', label: 'Friendly' },
    { value: 'authoritative', label: 'Authoritative' },
    { value: 'inspirational', label: 'Inspirational' }
  ]

  useEffect(() => {
    loadContentSources()
  }, [])

  const loadContentSources = async () => {
    try {
      const response = await contentAPI.list()
      setContentSources(response.data.sources || [])
    } catch (error) {
      console.error('Error loading content sources:', error)
    }
  }

  const handleGenerate = async () => {
    if (!selectedSource && !customText.trim()) {
      toast.error('Please select a content source or enter custom text')
      return
    }

    setGenerating(true)
    setGeneratedContent(null)

    try {
      let sourceText = customText

      if (selectedSource && !customText.trim()) {
        // Get content from selected source
        const source = contentSources.find(s => s.id === selectedSource)
        if (source && source.transcript) {
          sourceText = source.transcript
        } else {
          toast.error('Selected content source has no text content')
          return
        }
      }

      const requestData = {
        text: sourceText,
        type: contentType,
        audience: targetAudience,
        tone: tone
      }

      const response = await generationAPI.generate(requestData)
      setGeneratedContent(response.data)
      toast.success('Content generated successfully!')
    } catch (error) {
      console.error('Generation error:', error)
      toast.error('Failed to generate content')
    } finally {
      setGenerating(false)
    }
  }

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
    toast.success('Copied to clipboard!')
  }

  const downloadContent = () => {
    if (!generatedContent) return

    const content = generatedContent.generated_content
    let textContent = ''

    if (contentType === 'linkedin_post') {
      textContent = `${content.title}\n\n${content.content}\n\nHashtags: ${content.hashtags?.join(' ')}`
    } else if (contentType === 'twitter_thread') {
      textContent = content.thread?.join('\n\n') + `\n\nHashtags: ${content.hashtags?.join(' ')}`
    } else {
      textContent = content.content
    }

    const blob = new Blob([textContent], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${contentType}_${Date.now()}.txt`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Generate Content</h1>
        <p className="text-gray-600 mt-2">Create AI-powered social media posts from your content</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Generation Form */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Content Settings</h3>
          
          <div className="space-y-4">
            {/* Content Source Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Content Source
              </label>
              <select
                value={selectedSource}
                onChange={(e) => setSelectedSource(e.target.value)}
                className="input-field"
              >
                <option value="">Select uploaded content...</option>
                {contentSources.map((source) => (
                  <option key={source.id} value={source.id}>
                    {source.title} ({source.source_type})
                  </option>
                ))}
              </select>
            </div>

            {/* Custom Text Input */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Or Enter Custom Text
              </label>
              <textarea
                value={customText}
                onChange={(e) => setCustomText(e.target.value)}
                placeholder="Enter your content here..."
                rows={4}
                className="input-field"
              />
            </div>

            {/* Content Type */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Content Type
              </label>
              <select
                value={contentType}
                onChange={(e) => setContentType(e.target.value)}
                className="input-field"
              >
                {contentTypes.map((type) => (
                  <option key={type.value} value={type.value}>
                    {type.label}
                  </option>
                ))}
              </select>
            </div>

            {/* Target Audience */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Target Audience
              </label>
              <select
                value={targetAudience}
                onChange={(e) => setTargetAudience(e.target.value)}
                className="input-field"
              >
                {audiences.map((audience) => (
                  <option key={audience.value} value={audience.value}>
                    {audience.label}
                  </option>
                ))}
              </select>
            </div>

            {/* Tone */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Tone
              </label>
              <select
                value={tone}
                onChange={(e) => setTone(e.target.value)}
                className="input-field"
              >
                {tones.map((toneOption) => (
                  <option key={toneOption.value} value={toneOption.value}>
                    {toneOption.label}
                  </option>
                ))}
              </select>
            </div>

            {/* Generate Button */}
            <button
              onClick={handleGenerate}
              disabled={generating}
              className="w-full btn-primary flex items-center justify-center"
            >
              {generating ? (
                <>
                  <RefreshCw className="animate-spin h-5 w-5 mr-2" />
                  Generating...
                </>
              ) : (
                <>
                  <Zap className="h-5 w-5 mr-2" />
                  Generate Content
                </>
              )}
            </button>
          </div>
        </div>

        {/* Generated Content */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Generated Content</h3>
            {generatedContent && (
              <div className="flex space-x-2">
                <button
                  onClick={() => copyToClipboard(
                    contentType === 'linkedin_post' 
                      ? `${generatedContent.generated_content.title}\n\n${generatedContent.generated_content.content}`
                      : generatedContent.generated_content.thread?.join('\n') || generatedContent.generated_content.content
                  )}
                  className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg"
                  title="Copy to clipboard"
                >
                  <Copy className="h-4 w-4" />
                </button>
                <button
                  onClick={downloadContent}
                  className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg"
                  title="Download"
                >
                  <Download className="h-4 w-4" />
                </button>
              </div>
            )}
          </div>

          {generatedContent ? (
            <div className="space-y-4">
              {generatedContent.ai_powered && (
                <div className="flex items-center text-green-600 text-sm">
                  <Zap className="h-4 w-4 mr-2" />
                  AI-Powered Content ({generatedContent.ai_source})
                </div>
              )}

              {contentType === 'linkedin_post' && (
                <div>
                  <h4 className="font-semibold text-gray-900 mb-2">
                    {generatedContent.generated_content.title}
                  </h4>
                  <div className="whitespace-pre-wrap text-gray-700 mb-4">
                    {generatedContent.generated_content.content}
                  </div>
                  {generatedContent.generated_content.hashtags && (
                    <div className="flex flex-wrap gap-2">
                      {generatedContent.generated_content.hashtags.map((tag, index) => (
                        <span key={index} className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">
                          {tag}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {contentType === 'twitter_thread' && (
                <div>
                  {generatedContent.generated_content.thread?.map((tweet, index) => (
                    <div key={index} className="mb-3 p-3 bg-gray-50 rounded-lg">
                      <div className="text-sm text-gray-600 mb-1">Tweet {index + 1}</div>
                      <div className="whitespace-pre-wrap">{tweet}</div>
                    </div>
                  ))}
                  {generatedContent.generated_content.hashtags && (
                    <div className="flex flex-wrap gap-2 mt-4">
                      {generatedContent.generated_content.hashtags.map((tag, index) => (
                        <span key={index} className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">
                          {tag}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {(contentType === 'instagram_carousel' || contentType === 'newsletter_section') && (
                <div className="whitespace-pre-wrap text-gray-700">
                  {generatedContent.generated_content.content}
                </div>
              )}

              <div className="text-xs text-gray-500 pt-4 border-t">
                Source preview: {generatedContent.source_preview}
              </div>
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              <FileText className="h-12 w-12 mx-auto mb-4 text-gray-300" />
              <p>Generated content will appear here</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Generate
