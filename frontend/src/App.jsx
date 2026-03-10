import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { LayoutDashboard, FileText, CheckSquare, Activity, Loader2, UploadCloud, UserPen } from 'lucide-react';
import FileUpload from './components/processing/FileUpload';
import ProcessingFlow from './components/processing/ProcessingFlow';
import HITLPortal from './components/hitl/HITLPortal';
import Dashboard from './components/dashboard/Dashboard';
import CAMSummary from './components/cam/CAMSummary';
import RecommendationPanel from './components/recommendation/RecommendationPanel';

function App() {
  const [activeTab, setActiveTab] = useState('upload');
  const [apiData, setApiData] = useState(null);
  const [uploadFiles, setUploadFiles] = useState(null);
  const [isProcessingComplete, setIsProcessingComplete] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isAnimationComplete, setIsAnimationComplete] = useState(false);
  const [isApiComplete, setIsApiComplete] = useState(false);
  const [hitlData, setHitlData] = useState(null);

  const handleUploadComplete = (files) => {
    setUploadFiles(files);
    setActiveTab('hitl');
  };

  const handleHITLComplete = (hitlResult) => {
    setHitlData(hitlResult);
    setActiveTab('processing');
    // Fire the API call immediately in parallel with the animation
    fireAnalysis(uploadFiles, hitlResult);
  };

  // Fire the backend analysis immediately (runs in parallel with animation)
  const fireAnalysis = async (files, hitl) => {
    setIsLoading(true);
    setIsApiComplete(false);
    setIsAnimationComplete(false);
    setError(null);
    try {
      const formData = new FormData();
      if (files) {
        Object.keys(files).forEach(key => {
          if (files[key]) {
            formData.append(key, files[key]);
          }
        });
      }

      // Append HITL data as JSON string if available
      if (hitl) {
        formData.append('hitl_data', JSON.stringify(hitl));
      }

      const response = await axios.post('http://localhost:8000/api/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      setApiData(response.data);
      setIsApiComplete(true);
      setIsProcessingComplete(true);
    } catch (err) {
      setError('Failed to connect to backend engine. Is the backend running?');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAnimationComplete = () => {
    setIsAnimationComplete(true);
  };

  // Navigate to dashboard only when BOTH animation and API are done
  useEffect(() => {
    if (isAnimationComplete && isApiComplete && activeTab === 'processing') {
      setActiveTab('dashboard');
    }
  }, [isAnimationComplete, isApiComplete, activeTab]);

  const navItems = [
    { id: 'upload', label: 'Upload', icon: UploadCloud },
    { id: 'hitl', label: 'HITL Portal', icon: UserPen, disabled: !uploadFiles },
    { id: 'processing', label: 'Processing', icon: Activity, disabled: activeTab === 'upload' || activeTab === 'hitl' },
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard, disabled: !isProcessingComplete },
    { id: 'cam', label: 'CAM Summary', icon: FileText, disabled: !isProcessingComplete },
    { id: 'decision', label: 'Decision', icon: CheckSquare, disabled: !isProcessingComplete },
  ];

  return (
    <div className="min-h-screen bg-background-light text-gray-900 font-display flex flex-col">
      {/* Top Navigation */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex">
              <div className="flex-shrink-0 flex items-center shrink-0 space-x-2">
                <div className="h-8 w-8 bg-primary-600 rounded flex items-center justify-center text-white font-bold text-xl">C</div>
                <span className="font-bold text-xl tracking-tight">CAM<span className="text-primary-600">AI</span></span>
              </div>
              <nav className="hidden md:ml-8 md:flex md:space-x-8">
                {navItems.map(item => {
                  const Icon = item.icon;
                  return (
                    <button
                      key={item.id}
                      onClick={() => !item.disabled && setActiveTab(item.id)}
                      disabled={item.disabled}
                      className={`
                        inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors
                        ${activeTab === item.id
                          ? 'border-primary-500 text-primary-600'
                          : item.disabled
                            ? 'border-transparent text-gray-300 cursor-not-allowed'
                            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                        }
                      `}
                    >
                      <Icon className="w-4 h-4 mr-2" />
                      {item.label}
                    </button>
                  );
                })}
              </nav>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 w-full max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {error && (
          <div className="bg-red-50 border-l-4 border-red-400 p-4 mb-6">
            <div className="flex">
              <div className="ml-3">
                <p className="text-sm text-red-700">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Tab Content Rendering */}
        <div className="transition-all duration-300">
          {activeTab === 'upload' && <FileUpload onUploadComplete={handleUploadComplete} />}

          {activeTab === 'hitl' && (
            <HITLPortal uploadedFiles={uploadFiles} onComplete={handleHITLComplete} />
          )}

          {activeTab === 'processing' && (
            <div className="flex flex-col items-center">
              <ProcessingFlow onComplete={handleAnimationComplete} />
              {isAnimationComplete && isLoading && (
                <div className="mt-8 flex flex-col items-center text-primary-600">
                  <Loader2 className="w-8 h-8 animate-spin mb-2" />
                  <span className="font-medium">Finalizing analysis, please wait...</span>
                </div>
              )}
            </div>
          )}

          {activeTab === 'dashboard' && <Dashboard data={apiData} />}
          {activeTab === 'cam' && <CAMSummary data={apiData} />}
          {activeTab === 'decision' && <RecommendationPanel data={apiData} />}
        </div>
      </main>
    </div>
  );
}

export default App;
