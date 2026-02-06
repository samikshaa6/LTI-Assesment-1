import { useState } from 'react';
import { FileUpload } from './components/FileUpload';
import { AnalysisResult } from './components/AnalysisResult';
import { ChatInterface } from './components/ChatInterface';
import { uploadFiles } from './api';

function App() {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async (resume: File, jd: File) => {
    setLoading(true);
    try {
      const result = await uploadFiles(resume, jd);
      if (result.status === 'success') {
        setAnalysis(result.analysis);
      } else {
        alert('Upload failed');
      }
    } catch (error) {
      console.error(error);
      alert('Error uploading files');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto text-center mb-8">
        <h1 className="text-4xl font-extrabold text-blue-900">AI Resume Screener</h1>
        <p className="mt-2 text-lg text-gray-600">Smart Resume Screening with RAG</p>
      </div>

      <FileUpload onUpload={handleUpload} loading={loading} />

      {analysis && (
        <>
          <AnalysisResult data={analysis} />
          <ChatInterface />
        </>
      )}
    </div>
  );
}

export default App;
