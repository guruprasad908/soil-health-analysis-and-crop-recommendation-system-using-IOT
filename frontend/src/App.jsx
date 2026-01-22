import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import { ThemeProvider } from './contexts/ThemeContext';
import { LanguageProvider } from './contexts/LanguageContext';
import Header from './components/Header';
import Footer from './components/Footer';
import Home from './pages/Home';
import Weather from './pages/Weather';
import Prediction from './pages/Prediction';
import FertilizerGuide from './pages/FertilizerGuide';
import FertilizerRecommendation from './pages/FertilizerRecommendation';
import ModelComparison from './pages/ModelComparison';
import History from './pages/History';

import About from './pages/About';
import SampleReport from './pages/SampleReport';
import BioFertilizerGuide from './pages/BioFertilizerGuide';
import SensorDashboard from './pages/SensorDashboard';
import RLFeedback from './pages/RLFeedback';
import FarmVisualizer from './pages/FarmVisualizer';

function App() {
  return (
    <ThemeProvider>
      <LanguageProvider>
        <Router>
          <div className="App">
            <Header />
            <main className="main-content">
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/weather" element={<Weather />} />
                <Route path="/prediction" element={<Prediction />} />
                <Route path="/fertilizer-guide" element={<FertilizerGuide />} />
                <Route path="/fertilizer-recommendation" element={<FertilizerRecommendation />} />
                <Route path="/bio-fertilizer-guide" element={<BioFertilizerGuide />} />
                <Route path="/model-comparison" element={<ModelComparison />} />
                <Route path="/history" element={<History />} />
                <Route path="/history" element={<History />} />
                <Route path="/sensor-dashboard" element={<SensorDashboard />} />
                <Route path="/rl-feedback" element={<RLFeedback />} />
                <Route path="/farm-visualizer" element={<FarmVisualizer />} />
                <Route path="/about" element={<About />} />
                <Route path="/sample-report" element={<SampleReport />} />
              </Routes>
            </main>
            <Footer />
          </div>
        </Router>
      </LanguageProvider>
    </ThemeProvider>
  );
}

export default App;