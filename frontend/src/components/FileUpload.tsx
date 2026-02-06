import React, { useState } from 'react';

interface FileUploadProps {
    onUpload: (resume: File, jd: File) => void;
    loading: boolean;
}

export const FileUpload: React.FC<FileUploadProps> = ({ onUpload, loading }) => {
    const [resume, setResume] = useState<File | null>(null);
    const [jd, setJd] = useState<File | null>(null);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (resume && jd) {
            onUpload(resume, jd);
        }
    };

    return (
        <div className="bg-white p-6 rounded-lg shadow-md max-w-2xl mx-auto mt-8">
            <h2 className="text-2xl font-bold mb-6 text-gray-800">Upload Documents</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Resume (PDF)</label>
                    <input
                        type="file"
                        accept=".pdf,.txt"
                        onChange={(e) => setResume(e.target.files?.[0] || null)}
                        className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                    />
                </div>
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Job Description (TXT/PDF)</label>
                    <input
                        type="file"
                        accept=".txt,.pdf"
                        onChange={(e) => setJd(e.target.files?.[0] || null)}
                        className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                    />
                </div>
                <button
                    type="submit"
                    disabled={!resume || !jd || loading}
                    className={`w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
                >
                    {loading ? 'Analyzing...' : 'Analyze Match'}
                </button>
            </form>
        </div>
    );
};
