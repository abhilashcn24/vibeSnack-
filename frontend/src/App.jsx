import React, { useState } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { Moon, Sun, Sparkles } from 'lucide-react';
import SnackForm from './components/SnackForm';
import RecommendationCard from './components/RecommendationCard';
import { ThemeProvider, useTheme } from './context/ThemeContext';

// Configure axios base URL
const api = axios.create({
  baseURL: import.meta.env.PROD ? '/api' : 'http://127.0.0.1:8000',
});

function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();
  return (
    <button
      onClick={toggleTheme}
      className="p-2 rounded-full bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
      aria-label="Toggle Theme"
    >
      {theme === 'light' ? <Moon size={20} /> : <Sun size={20} />}
    </button>
  );
}

function MainContent() {
  const [recommendations, setRecommendations] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleRecommend = async (formData) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await api.post('/predict', formData);
      setRecommendations(response.data.recommendations);
      setCurrentIndex(0);
    } catch (err) {
      console.error(err);
      setError("Failed to get recommendations. Is the backend running?");
    } finally {
      setIsLoading(false);
    }
  };

  const handleAccept = async (snackId) => {
    try {
      await api.post('/feedback', { snack_id: snackId });
    } catch (err) {
      console.error("Failed to save feedback", err);
    }
  };

  const handleNext = () => {
    if (currentIndex < recommendations.length - 1) {
      setCurrentIndex(prev => prev + 1);
    }
  };

  const currentRecommendation = recommendations[currentIndex];
  const hasNext = currentIndex < recommendations.length - 1;

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-purple-100 dark:from-gray-900 dark:to-gray-800 transition-colors duration-300 font-sans py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto">
        <header className="flex justify-between items-center mb-12">
          <div className="flex items-center gap-2">
            <Sparkles className="text-indigo-600 dark:text-indigo-400" size={32} />
            <h1 className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600 dark:from-indigo-400 dark:to-purple-400">
              VibeSnack
            </h1>
          </div>
          <ThemeToggle />
        </header>

        <div className="text-center mb-12">
          <p className="mt-2 text-xl text-gray-600 dark:text-gray-300">
            Your tiny, delightful snack recommender.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
            className="lg:col-span-1"
          >
            <SnackForm onRecommend={handleRecommend} isLoading={isLoading} />
          </motion.div>

          <div className="lg:col-span-2 space-y-6">
            <AnimatePresence mode="wait">
              {error && (
                <motion.div
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0 }}
                  className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative"
                  role="alert"
                >
                  <strong className="font-bold">Error: </strong>
                  <span className="block sm:inline">{error}</span>
                </motion.div>
              )}
            </AnimatePresence>

            <AnimatePresence mode="wait">
              {recommendations.length > 0 ? (
                <motion.div
                  key={currentRecommendation.id}
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.95 }}
                  transition={{ duration: 0.3 }}
                >
                  <RecommendationCard
                    recommendation={currentRecommendation}
                    onAccept={handleAccept}
                    onNext={handleNext}
                    hasNext={hasNext}
                  />
                </motion.div>
              ) : (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm p-12 rounded-xl border-2 border-dashed border-gray-300 dark:border-gray-700 text-center text-gray-400 dark:text-gray-500"
                >
                  <p className="text-xl">Enter your vibe to get a snack!</p>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Alternatives List */}
            {recommendations.length > 0 && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
                className="mt-8"
              >
                <h3 className="text-lg font-medium text-gray-500 dark:text-gray-400 mb-4">Alternatives</h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  {recommendations.slice(currentIndex + 1, currentIndex + 4).map((rec, idx) => (
                    <motion.div
                      key={rec.id}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.1 * idx }}
                      className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 hover:shadow-md transition-shadow"
                    >
                      <h4 className="font-bold text-gray-800 dark:text-gray-200">{rec.name}</h4>
                      <p className="text-sm text-gray-500 dark:text-gray-400">{(rec.prob * 100).toFixed(0)}% Match</p>
                    </motion.div>
                  ))}
                </div>
              </motion.div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

function App() {
  return (
    <ThemeProvider>
      <MainContent />
    </ThemeProvider>
  );
}

export default App;
