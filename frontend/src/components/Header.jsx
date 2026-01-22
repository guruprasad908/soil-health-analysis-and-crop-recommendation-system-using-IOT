import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useTheme } from '../contexts/ThemeContext';
import { useLanguage } from '../contexts/LanguageContext';
import { useTranslation } from '../hooks/useTranslation';
import './Header.css';

// Navigation items are now translated dynamically in the component

const Header = () => {
  const location = useLocation();
  const { theme, toggleTheme } = useTheme();
  const { language, toggleLanguage } = useLanguage();
  const { t } = useTranslation();
  const [menuOpen, setMenuOpen] = useState(false);

  const isActive = (path) => (location.pathname === path ? 'active' : '');

  // Update navigation items with translations
  const translatedNavItems = [
    { path: '/', label: t('nav.home') },
    { path: '/prediction', label: t('nav.cropRecommendation') },
    { path: '/weather', label: t('nav.weatherInsights'), newTab: true },
    { path: '/sensor-dashboard', label: t('nav.sensorDashboard'), newTab: true },
    { path: '/model-comparison', label: t('nav.ensembleLab') },

    { path: '/fertilizer-guide', label: t('nav.fertilizerGuide') },
    { path: '/bio-fertilizer-guide', label: t('nav.bioFertilizerGuide') },
    { path: '/history', label: t('nav.history') },
    { path: '/rl-feedback', label: t('nav.rlFeedback') },
    { path: '/about', label: t('nav.aboutUs') }
  ];

  return (
    <header className="agri-header">
      <div className="header-gradient" />
      <div className="header-content">
        <Link to="/" className="brand" onClick={() => setMenuOpen(false)}>
          <div className="brand-copy">
            <span className="brand-title">{t('common.soilSense')}</span>
            <span className="brand-subtitle">{t('common.intelligentAgriculture')}</span>
          </div>
        </Link>

        <button
          className={`nav-toggle ${menuOpen ? 'open' : ''}`}
          aria-label="Toggle navigation"
          onClick={() => setMenuOpen((prev) => !prev)}
        >
          <span />
          <span />
          <span />
        </button>

        <nav className={`main-nav ${menuOpen ? 'open' : ''}`}>
          <ul>
            {translatedNavItems.map((item) => (
              <li key={item.path}>
                {item.newTab ? (
                  <a
                    href={item.path}
                    target="_blank"
                    rel="noopener noreferrer"
                    className={isActive(item.path)}
                    onClick={() => setMenuOpen(false)}
                  >
                    <span>{item.label}</span>
                  </a>
                ) : (
                  <Link
                    to={item.path}
                    className={isActive(item.path)}
                    onClick={() => setMenuOpen(false)}
                  >
                    <span>{item.label}</span>
                  </Link>
                )}
              </li>
            ))}
            <li>
              <button className="theme-toggle" onClick={toggleTheme} aria-label={t('common.toggleTheme')}>
                <span className="toggle-track" />
                <span className="toggle-icon">{theme === 'dark' ? '🌞' : '🌙'}</span>
              </button>
            </li>
            <li>
              <button className="theme-toggle" onClick={toggleLanguage} aria-label={t('common.toggleLanguage')}>
                <span className="toggle-track" />
                <span className="toggle-icon">{language === 'en' ? 'ಕನ್ನಡ' : 'English'}</span>
              </button>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;