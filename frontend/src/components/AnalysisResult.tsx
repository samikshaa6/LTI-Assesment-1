import React from 'react';

interface AnalysisResultProps {
    data: {
        match_score: number;
        strengths: string[];
        gaps: string[];
        summary: string;
    } | null;
}

export const AnalysisResult: React.FC<AnalysisResultProps> = ({ data }) => {
    if (!data) return null;

    return (
        <div className="bg-white p-6 rounded-lg shadow-md max-w-2xl mx-auto mt-6">
            <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-gray-800">Match Analysis</h2>
                <div className="flex items-center">
                    <div className={`text-4xl font-bold ${data.match_score > 70 ? 'text-green-600' : data.match_score > 40 ? 'text-yellow-500' : 'text-red-500'}`}>
                        {data.match_score}%
                    </div>
                    <span className="ml-2 text-sm text-gray-500">Match</span>
                </div>
            </div>

            <div className="mb-6">
                <h3 className="font-semibold text-lg mb-2">Summary</h3>
                <p className="text-gray-600">{data.summary}</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-4 bg-green-50 rounded-lg">
                    <h3 className="font-semibold text-green-800 mb-2">✅ Strengths</h3>
                    <ul className="list-disc list-inside text-sm text-gray-700">
                        {data.strengths.map((s, i) => <li key={i}>{s}</li>)}
                    </ul>
                </div>
                <div className="p-4 bg-red-50 rounded-lg">
                    <h3 className="font-semibold text-red-800 mb-2">❌ Gaps</h3>
                    <ul className="list-disc list-inside text-sm text-gray-700">
                        {data.gaps.map((s, i) => <li key={i}>{s}</li>)}
                    </ul>
                </div>
            </div>
        </div>
    );
};
