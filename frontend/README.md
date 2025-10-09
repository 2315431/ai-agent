# Content Repurposing Agent - Frontend

A modern React web interface for the Content Repurposing Agent API.

## Features

- 🔐 **Secure Authentication** - JWT-based login system
- 📤 **Content Upload** - Drag & drop file uploads
- 🤖 **AI Generation** - Generate LinkedIn, Twitter, Instagram, and Newsletter content
- 📊 **Dashboard** - Overview of your content and stats
- 📚 **API Documentation** - Built-in API docs
- ⚙️ **Settings** - Customize your preferences

## Tech Stack

- **React 18** - Modern React with hooks
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **Axios** - HTTP client for API calls
- **Lucide React** - Beautiful icons
- **React Hot Toast** - Toast notifications

## Quick Start

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Set up environment:**
   ```bash
   cp env.example .env
   # Edit .env if needed
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

4. **Open in browser:**
   ```
   http://localhost:3000
   ```

## Login Credentials

- **Username:** `admin`
- **Password:** `darshan@2003`

## Build for Production

```bash
npm run build
```

The built files will be in the `dist` folder.

## Project Structure

```
frontend/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── Layout.jsx      # Main layout wrapper
│   │   ├── Sidebar.jsx     # Navigation sidebar
│   │   ├── Header.jsx      # Top header
│   │   └── ProtectedRoute.jsx # Route protection
│   ├── contexts/           # React contexts
│   │   └── AuthContext.jsx # Authentication state
│   ├── pages/              # Page components
│   │   ├── Login.jsx       # Login page
│   │   ├── Dashboard.jsx   # Main dashboard
│   │   ├── Upload.jsx      # File upload
│   │   ├── Generate.jsx    # AI content generation
│   │   ├── Results.jsx     # View results
│   │   ├── Content.jsx     # Content management
│   │   ├── Settings.jsx    # User settings
│   │   └── Docs.jsx        # API documentation
│   ├── services/           # API services
│   │   └── api.js          # Axios configuration
│   ├── App.jsx             # Main app component
│   ├── main.jsx            # App entry point
│   └── index.css           # Global styles
├── public/                 # Static assets
├── package.json            # Dependencies
├── vite.config.js          # Vite configuration
├── tailwind.config.js      # Tailwind configuration
└── README.md               # This file
```

## API Integration

The frontend connects to the Content Repurposing Agent API:

- **Base URL:** `https://ai-agent-ikc8.onrender.com`
- **Authentication:** JWT tokens
- **Content Types:** LinkedIn, Twitter, Instagram, Newsletter
- **File Upload:** TXT, MD, PDF, MP4, MP3, WAV

## Features Overview

### 🔐 Authentication
- Secure JWT-based login
- Protected routes
- Auto-logout on token expiry

### 📤 Content Upload
- Drag & drop interface
- Multiple file formats
- File size validation
- Upload progress

### 🤖 AI Generation
- Multiple content types
- Customizable audience and tone
- Real-time generation
- Copy and download options

### 📊 Dashboard
- Content statistics
- Recent uploads
- Quick actions
- AI status monitoring

### 📚 Documentation
- Interactive API docs
- Usage examples
- Endpoint reference
- Swagger UI integration

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

### Environment Variables

- `VITE_API_URL` - Backend API URL (default: https://ai-agent-ikc8.onrender.com)

## Deployment

The frontend can be deployed to any static hosting service:

- **Vercel** - Recommended for React apps
- **Netlify** - Great for static sites
- **GitHub Pages** - Free hosting
- **AWS S3** - Scalable static hosting

### Vercel Deployment

1. Connect your GitHub repository to Vercel
2. Set build command: `npm run build`
3. Set output directory: `dist`
4. Deploy!

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of the Content Repurposing Agent system.
