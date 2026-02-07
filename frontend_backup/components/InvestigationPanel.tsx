import React from 'react';
import ReactMarkdown from 'react-markdown';

interface InvestigationPanelProps {
    apiResponse: {
        summary: string;
    };
}

export default function InvestigationPanel({ apiResponse }: InvestigationPanelProps) {
    return (
        <div className="p-6 bg-slate-900 text-white rounded-xl shadow-2xl">
            <h2 className="text-2xl font-bold mb-4">Investigation Copilot</h2>
            {/* Renders the AI reasoning for 97.5% reduction */}
            <div className="prose prose-invert max-w-none">
                <ReactMarkdown>{apiResponse.summary}</ReactMarkdown>
            </div>
            <div className="mt-4 flex gap-4">
                <button className="bg-red-600 px-4 py-2 rounded hover:bg-red-700 transition-colors">Freeze Account</button>
                <button className="bg-slate-700 px-4 py-2 rounded hover:bg-slate-600 transition-colors">Dismiss Alert</button>
            </div>
        </div>
    );
}
