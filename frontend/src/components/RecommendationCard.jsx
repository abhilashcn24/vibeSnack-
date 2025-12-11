import React, { useState } from 'react';
import { Check, RefreshCw, Info, Tag } from 'lucide-react';

export default function RecommendationCard({ recommendation, onAccept, onNext, hasNext }) {
    const [isAccepted, setIsAccepted] = useState(false);

    const handleAccept = () => {
        onAccept(recommendation.id);
        setIsAccepted(true);
    };

    const handleNext = () => {
        setIsAccepted(false);
        onNext();
    };

    if (!recommendation) return null;

    return (
        <div className="bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-xl border border-indigo-100 dark:border-gray-700 transition-colors">
            <h3 className="text-lg font-medium text-indigo-500 dark:text-indigo-400 mb-2 uppercase tracking-wide">I recommend...</h3>
            <h1 className="text-4xl sm:text-5xl font-extrabold text-gray-900 dark:text-white mb-6 tracking-tight leading-tight">
                {recommendation.name}
            </h1>

            <div className="flex flex-wrap gap-2 mb-6">
                {recommendation.tags.map(tag => (
                    <span key={tag} className="flex items-center gap-1 px-3 py-1 bg-indigo-50 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-300 text-sm font-semibold rounded-full border border-indigo-100 dark:border-indigo-800">
                        <Tag size={12} /> {tag}
                    </span>
                ))}
            </div>

            <div className="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 border-l-4 border-blue-500 p-5 mb-8 rounded-r-lg">
                <p className="text-blue-800 dark:text-blue-200 text-lg leading-relaxed">{recommendation.message}</p>
            </div>

            <div className="flex flex-col sm:flex-row gap-4 mb-8">
                <button
                    onClick={handleAccept}
                    disabled={isAccepted}
                    className={`
                        flex-1 flex items-center justify-center gap-2 font-bold py-3 px-6 rounded-xl transition-all transform active:scale-[0.98]
                        ${isAccepted
                            ? 'bg-green-100 text-green-700 border border-green-200 cursor-default'
                            : 'bg-green-500 hover:bg-green-600 text-white shadow-lg hover:shadow-green-500/30'}
                    `}
                >
                    {isAccepted ? <><Check size={20} /> Accepted</> : <><Check size={20} /> Accept</>}
                </button>

                <button
                    onClick={handleNext}
                    disabled={!hasNext}
                    className="flex-1 flex items-center justify-center gap-2 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-bold py-3 px-6 rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    <RefreshCw size={20} /> Try another
                </button>
            </div>

            <div className="border-t border-gray-100 dark:border-gray-700 pt-6">
                <details className="cursor-pointer group">
                    <summary className="flex items-center gap-2 text-sm font-medium text-gray-500 dark:text-gray-400 group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors list-none">
                        <Info size={16} /> Why this snack?
                    </summary>
                    <div className="mt-3 text-sm text-gray-600 dark:text-gray-300 bg-gray-50 dark:bg-gray-700/50 p-4 rounded-lg">
                        <p className="mb-2"><strong>Model Confidence:</strong> <span className="text-indigo-600 dark:text-indigo-400 font-bold">{(recommendation.prob * 100).toFixed(1)}%</span></p>
                        <p className="leading-relaxed">{recommendation.explanation}</p>
                    </div>
                </details>
            </div>
        </div>
    );
}
