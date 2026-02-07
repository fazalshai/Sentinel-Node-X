import React from 'react';

// Render the 30-second investigation summary for Deriv judges
const RenderInvestigation = ({ data }) => {
    return (
        <div className="p-4 border-l-4 border-red-500 bg-gray-900 text-white">
            <h2 className="text-xl font-bold">🚨 {data.is_suspicious ? "SUSPICIOUS" : "CLEAR"}</h2>
            <p className="mt-2 text-sm text-gray-400">Score: {data.temporal_result.score}</p>
            <div className="mt-4 p-2 bg-black rounded">
                {/* This displays the AI reasoning and recommendations */}
                <pre className="whitespace-pre-wrap">{data.summary}</pre>
            </div>
        </div>
    );
};

export default RenderInvestigation;
