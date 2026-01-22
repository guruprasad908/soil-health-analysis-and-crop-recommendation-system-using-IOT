import React from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from '../hooks/useTranslation';
import './Footer.css';

const Footer = () => {
  const { t } = useTranslation();
  const currentYear = new Date().getFullYear();

  return (
    <footer className="agri-footer">
      <div className="container footer-inner">
        <div className="footer-top">
          <div className="footer-brand">
            <div className="footer-mark">🌱</div>
            <div>
              <h3>{t('footer.soilSenseCollective')}</h3>
              <p>{t('footer.guidingFarmers')}</p>
            </div>
          </div>

          <div className="footer-grid">
            <div className="footer-section">
              <h4>{t('footer.platform')}</h4>
              <ul>
                <li><Link to="/">{t('nav.home')}</Link></li>
                <li><Link to="/prediction">{t('nav.cropRecommendation')}</Link></li>
                <li><Link to="/weather">{t('nav.weatherInsights')}</Link></li>
              </ul>
            </div>
            <div className="footer-section">
              <h4>{t('footer.advisories')}</h4>
              <ul>
                <li><Link to="/fertilizer-guide">{t('nav.fertilizerGuide')}</Link></li>
                <li><Link to="/fertilizer-recommendation">{t('fertilizer.recommendation')}</Link></li>
                <li><Link to="/model-comparison">{t('nav.ensembleLab')}</Link></li>
                <li><Link to="/history">{t('nav.history')}</Link></li>
                <li><Link to="/rl-feedback">{t('nav.rlFeedback')}</Link></li>
              </ul>
            </div>
            <div className="footer-section">
              <h4>{t('footer.tools')}</h4>
              <ul>
                <li><Link to="/sample-report">{t('sample.report')}</Link></li>
                <li><a href="https://open-meteo.com/" target="_blank" rel="noreferrer">{t('footer.openMeteoApi')}</a></li>
              </ul>
            </div>
          </div>
        </div>

        <div className="footer-bottom">
          <p>© {currentYear} {t('footer.soilSenseCollective')}. {t('footer.allRightsReserved')}</p>
          <p className="footer-note">{t('footer.craftedFor')}</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;