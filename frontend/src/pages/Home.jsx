import React from 'react';
import { Link } from 'react-router-dom';
import { CloudSun, Sprout, Droplets, TrendingUp, History, FileText } from 'lucide-react';
import { useTranslation } from '../hooks/useTranslation';
import './Home.css';

const coreFeatures = [
  {
    titleKey: 'home.climateIntelligence',
    descriptionKey: 'home.climateIntelligenceDesc',
    ctaKey: 'home.viewClimateDashboards',
    to: '/weather',
    icon: CloudSun
  },
  {
    titleKey: 'home.cropSenseEngine',
    descriptionKey: 'home.cropSenseEngineDesc',
    ctaKey: 'home.predictCrops',
    to: '/prediction',
    icon: Sprout
  },
  {
    titleKey: 'home.nutrientGuidance',
    descriptionKey: 'home.nutrientGuidanceDesc',
    ctaKey: 'home.exploreFertilizerGuide',
    to: '/fertilizer-guide',
    icon: Droplets
  }
];

const advancedFeatures = [
  {
    titleKey: 'home.modelExplorer',
    descriptionKey: 'home.modelExplorerDesc',
    to: '/model-comparison',
    icon: TrendingUp
  },
  {
    titleKey: 'home.fieldHistory',
    descriptionKey: 'home.fieldHistoryDesc',
    to: '/history',
    icon: History
  }
];

const highlights = [
  {
    titleKey: 'home.soilFirstDecisions',
    copyKey: 'home.soilFirstDecisionsDesc'
  },
  {
    titleKey: 'home.weatherReadyFarming',
    copyKey: 'home.weatherReadyFarmingDesc'
  },
  {
    titleKey: 'home.alwaysLearning',
    copyKey: 'home.alwaysLearningDesc'
  }
];

const Home = () => {
  const { t } = useTranslation();

  return (
    <div className="home-page">
      <section className="hero fade-in-up">
        <div className="container hero-grid">
          <div className="hero-copy">
            <span className="eyebrow">SOIL-SMART. WEATHER-AWARE. FARMER-FOCUSED.</span>
            <h1>{t('home.title')}</h1>
            <p>
              {t('home.description')}
            </p>
            <div className="hero-actions">
              <Link to="/prediction" className="btn-primary">{t('prediction.title')}</Link>
              <Link to="/weather" className="btn-ghost">{t('weather.title')}</Link>
            </div>
            <div className="hero-metrics">
              <div>
                <strong>99.5%</strong>
                <span>{t('home.stackedEnsembleAccuracy')}</span>
              </div>
              <div>
                <strong>22</strong>
                <span>{t('home.cropsSupported')}</span>
              </div>
              <div>
                <strong>6</strong>
                <span>{t('home.mlAlgorithms')}</span>
              </div>
            </div>
          </div>

          <div className="hero-card">
            <div className="card-head">
              <span>{t('home.todaysSnapshot')}</span>
            </div>
            <ul>
              {highlights.map((item) => (
                <li key={item.titleKey}>
                  <h3>{t(item.titleKey)}</h3>
                  <p>{t(item.copyKey)}</p>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </section>

      <section className="feature-section fade-in-up">
        <div className="container">
          <div className="section-heading">
            <h2>{t('home.coreIntelligenceModules')}</h2>
            <p className="section-subtitle">{t('home.navigateSoilSampling')}</p>
          </div>
          <div className="feature-grid">
            {coreFeatures.map((feature) => (
              <Link to={feature.to} className="feature-card-link" key={feature.titleKey}>
                <article className="feature-card">
                  <h3>
                    <feature.icon size={20} />
                    {t(feature.titleKey)}
                  </h3>
                  <p>{t(feature.descriptionKey)}</p>
                  <div className="feature-link">
                    {t(feature.ctaKey)}
                    <span aria-hidden>→</span>
                  </div>
                </article>
              </Link>
            ))}
          </div>
        </div>
      </section>

      <section className="feature-section fade-in-up">
        <div className="container">
          <div className="section-heading">
            <h2>{t('home.advancedWorkflows')}</h2>
            <p className="section-subtitle">{t('home.scaleInsights')}</p>
          </div>
          <div className="feature-grid compact">
            {advancedFeatures.map((feature) => (
              <Link to={feature.to} className="feature-card-link" key={feature.titleKey}>
                <article className="feature-card compact">
                  <div>
                    <h3>
                      <feature.icon size={20} />
                      {t(feature.titleKey)}
                    </h3>
                    <p>{t(feature.descriptionKey)}</p>
                  </div>
                  <div className="feature-link minimal">
                    {t('home.explore')}
                    <span aria-hidden>→</span>
                  </div>
                </article>
              </Link>
            ))}
          </div>
        </div>
      </section>

      <section className="feature-section fade-in-up">
        <div className="container">
          <div className="section-heading">
            <h2>{t('sample.report')}</h2>
            <p className="section-subtitle">{t('home.sampleReportDesc')}</p>
          </div>
          <div className="sample-report-card">
            <h3>
              <FileText size={20} />
              {t('home.viewSampleReport')}
            </h3>
            <p>{t('home.sampleReportDetails')}</p>
            <Link to="/sample-report" className="sample-report-link">
              {t('home.viewSampleReport')}
              <span aria-hidden>→</span>
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;