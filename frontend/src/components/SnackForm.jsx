import React, { useState } from 'react';
import { Clock, Smile, Utensils, Leaf, Activity } from 'lucide-react';

const MOODS = ["happy", "sad", "bored", "stressed", "energetic", "lazy"];
const CONTEXTS = ["none", "studying", "gaming", "chilling", "gym"];

export default function SnackForm({ onRecommend, isLoading }) {
    const [formData, setFormData] = useState({
        hour: new Date().getHours(),
        mood: 'happy',
        hunger: 3,
        diet: 'veg',
        context: 'none'
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onRecommend(formData);
    };

    return (
        <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-xl border border-gray-100 dark:border-gray-700 transition-colors">
            <h2 className="text-2xl font-bold mb-6 text-gray-800 dark:text-white flex items-center gap-2">
                <span role="img" aria-label="wave">👋</span> Tell me about yourself
            </h2>
            <form onSubmit={handleSubmit} className="space-y-6">

                {/* Time */}
                <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1 flex items-center gap-2">
                        <Clock size={16} /> Time (Hour 0-23)
                    </label>
                    <input
                        type="number"
                        name="hour"
                        min="0"
                        max="23"
                        value={formData.hour}
                        onChange={handleChange}
                        className="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2.5 transition-colors"
                    />
                </div>

                {/* Mood */}
                <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1 flex items-center gap-2">
                        <Smile size={16} /> Mood
                    </label>
                    <select
                        name="mood"
                        value={formData.mood}
                        onChange={handleChange}
                        className="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2.5 transition-colors"
                    >
                        {MOODS.map(m => <option key={m} value={m}>{m}</option>)}
                    </select>
                </div>

                {/* Hunger */}
                <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 flex items-center gap-2">
                        <Utensils size={16} /> Hunger Level ({formData.hunger})
                    </label>
                    <input
                        type="range"
                        name="hunger"
                        min="1"
                        max="5"
                        value={formData.hunger}
                        onChange={handleChange}
                        className="w-full h-2 bg-gray-200 dark:bg-gray-600 rounded-lg appearance-none cursor-pointer accent-indigo-600"
                    />
                    <div className="flex justify-between text-xs text-gray-500 dark:text-gray-400 mt-1">
                        <span>Not hungry</span>
                        <span>Starving</span>
                    </div>
                </div>

                {/* Diet */}
                <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 flex items-center gap-2">
                        <Leaf size={16} /> Diet
                    </label>
                    <div className="flex space-x-4">
                        {['veg', 'non-veg'].map((type) => (
                            <label key={type} className={`
                                flex-1 cursor-pointer rounded-lg border p-3 flex items-center justify-center transition-all
                                ${formData.diet === type
                                    ? 'bg-indigo-50 dark:bg-indigo-900/30 border-indigo-500 text-indigo-700 dark:text-indigo-300 ring-1 ring-indigo-500'
                                    : 'border-gray-200 dark:border-gray-600 hover:bg-gray-50 dark:hover:bg-gray-700 text-gray-600 dark:text-gray-400'}
                            `}>
                                <input
                                    type="radio"
                                    name="diet"
                                    value={type}
                                    checked={formData.diet === type}
                                    onChange={handleChange}
                                    className="sr-only"
                                />
                                <span className="capitalize font-medium">{type}</span>
                            </label>
                        ))}
                    </div>
                </div>

                {/* Context */}
                <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1 flex items-center gap-2">
                        <Activity size={16} /> Context
                    </label>
                    <select
                        name="context"
                        value={formData.context}
                        onChange={handleChange}
                        className="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2.5 transition-colors"
                    >
                        {CONTEXTS.map(c => <option key={c} value={c}>{c}</option>)}
                    </select>
                </div>

                <button
                    type="submit"
                    disabled={isLoading}
                    className="w-full flex justify-center py-3 px-4 border border-transparent rounded-xl shadow-sm text-sm font-bold text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-70 disabled:cursor-not-allowed transform transition-all active:scale-[0.98]"
                >
                    {isLoading ? (
                        <span className="flex items-center gap-2">
                            <span className="animate-spin">⏳</span> Thinking...
                        </span>
                    ) : 'Recommend Snack 🚀'}
                </button>
            </form>
        </div>
    );
}
