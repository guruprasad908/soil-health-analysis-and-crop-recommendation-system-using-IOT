import React from 'react';
import { useTranslation } from '../hooks/useTranslation';
import './About.css';

const About = () => {
  const { t } = useTranslation();
  
  return (
    <div className="about-page">
      <div className="container">
        <div className="section-heading">
          <h1>{t('about.title')}</h1>
          <p className="section-subtitle">{t('about.projectOverview')}</p>
        </div>

        <section className="card project-overview">
          <h2>{t('about.projectOverview')}</h2>
          <p>
            {t('about.projectDescription')}
          </p>
          
          <div className="project-details">
            <div className="detail-card">
              <h3>{t('about.mission')}</h3>
              <p>{t('about.missionDescription')}</p>
            </div>
            
            <div className="detail-card">
              <h3>{t('about.vision')}</h3>
              <p>{t('about.visionDescription')}</p>
            </div>
          </div>
        </section>

        <section className="card team-section">
          <h2>{t('about.developmentTeam')}</h2>
          <div className="team-grid">
            <div className="team-member">
              <div className="member-info">
                <h3>Guruprasad Pujari</h3>
                <p className="member-id">2BL23CI402</p>
              </div>
            </div>
            
            <div className="team-member">
              <div className="member-info">
                <h3>Sankirana S Managuli</h3>
                <p className="member-id">2BL22CI042</p>
              </div>
            </div>
            
            <div className="team-member">
              <div className="member-info">
                <h3>Apoorva Tuppad</h3>
                <p className="member-id">2BL22CI009</p>
              </div>
            </div>
            
            <div className="team-member">
              <div className="member-info">
                <h3>Priyanka Masabinal</h3>
                <p className="member-id">2BL22CI033</p>
              </div>
            </div>
          </div>
        </section>

        <section className="card guidance-section">
          <h2>{t('about.guidance')}</h2>
          <div className="guide-info">
            <h3>Prof. Poornima MAMDAPUR</h3>
            <p>{t('about.department')}</p>
            <p>{t('about.college')}</p>
            <p>Vijayapur – 586 103</p>
          </div>
        </section>

        <section className="card academic-section">
          <h2>{t('about.academicInfo')}</h2>
          <div className="academic-details">
            <p><strong>{t('about.department')}:</strong> {t('about.cseDepartment')}</p>
            <p><strong>{t('about.specialization')}:</strong> {t('about.aiMlSpecialization')}</p>
            <p><strong>{t('about.semester')}:</strong> {t('about.seventhSemester')}</p>
            <p><strong>{t('about.college')}:</strong> {t('about.fullCollegeName')}</p>
          </div>
        </section>

        <section className="card core-modules">
          <h2>{t('about.coreModules')}</h2>
          <div className="modules-grid">
            <div className="module-card">
              <div className="module-icon">
                <img 
                  src="https://cdn-icons-png.flaticon.com/512/747/747310.png" 
                  alt={t('about.soilAnalysis')} 
                  className="module-logo"
                />
              </div>
              <h3>{t('about.soilAnalysis')}</h3>
              <p>{t('about.soilAnalysisDescription')}</p>
            </div>
            
            <div className="module-card">
              <div className="module-icon">
                <img 
                  src="https://cdn-icons-png.flaticon.com/512/2920/2920485.png" 
                  alt={t('about.cropRecommendation')} 
                  className="module-logo"
                />
              </div>
              <h3>{t('about.intelligentCropRecommendation')}</h3>
              <p>{t('about.cropRecommendationDescription')}</p>
            </div>
            
            <div className="module-card">
              <div className="module-icon">
                <img 
                  src="https://cdn-icons-png.flaticon.com/512/3069/3069047.png" 
                  alt={t('about.weatherIntegration')} 
                  className="module-logo"
                />
              </div>
              <h3>{t('about.weatherIntelligence')}</h3>
              <p>{t('about.weatherDescription')}</p>
            </div>
            
            <div className="module-card">
              <div className="module-icon">
                <img 
                  src="https://cdn-icons-png.flaticon.com/512/2965/2965567.png" 
                  alt={t('about.fertilizerAdvisor')} 
                  className="module-logo"
                />
              </div>
              <h3>{t('about.fertilizerAdvisor')}</h3>
              <p>{t('about.fertilizerDescription')}</p>
            </div>
            
            <div className="module-card">
              <div className="module-icon">
                <img 
                  src="https://cdn-icons-png.flaticon.com/512/2920/2920366.png" 
                  alt={t('about.yieldPrediction')} 
                  className="module-logo"
                />
              </div>
              <h3>{t('about.yieldPrediction')}</h3>
              <p>{t('about.yieldPredictionDescription')}</p>
            </div>
            
            <div className="module-card">
              <div className="module-icon">
                <img 
                  src="https://cdn-icons-png.flaticon.com/512/2966/2966327.png" 
                  alt={t('about.marketAnalysis')} 
                  className="module-logo"
                />
              </div>
              <h3>{t('about.marketPriceAnalysis')}</h3>
              <p>{t('about.marketAnalysisDescription')}</p>
            </div>
          </div>
        </section>

        <section className="card model-accuracy">
          <h2>{t('about.modelAccuracy')}</h2>
          <div className="accuracy-grid">
            <div className="accuracy-card">
              <h3>{t('about.stackingClassifier')}</h3>
              <div className="accuracy-value">99.55%</div>
              <p>{t('about.stackingClassifierDescription')}</p>
            </div>
            
            <div className="accuracy-card">
              <h3>{t('about.randomForest')}</h3>
              <div className="accuracy-value">99.55%</div>
              <p>{t('about.randomForestDescription')}</p>
            </div>
            
            <div className="accuracy-card">
              <h3>{t('about.gradientBoosting')}</h3>
              <div className="accuracy-value">98.64%</div>
              <p>{t('about.gradientBoostingDescription')}</p>
            </div>
            
            <div className="accuracy-card">
              <h3>{t('about.decisionTree')}</h3>
              <div className="accuracy-value">98.86%</div>
              <p>{t('about.decisionTreeDescription')}</p>
            </div>
          </div>
        </section>

        <section className="card tech-stack">
          <h2>{t('about.technologyStack')}</h2>
          <div className="tech-grid">
            <div className="tech-category">
              <h3>{t('about.frontend')}</h3>
              <div className="tech-images">
                <div className="tech-item">
                  <img 
                    src="https://upload.wikimedia.org/wikipedia/commons/a/a7/React-icon.svg" 
                    alt="React" 
                    className="tech-logo"
                  />
                  <span>React.js</span>
                </div>
                <div className="tech-item">
                  <img 
                    src="https://www.chartjs.org/media/logo-title.svg" 
                    alt="Chart.js" 
                    className="tech-logo"
                  />
                  <span>Chart.js</span>
                </div>
                <div className="tech-item">
                  <div className="tech-logo css-logo">CSS3</div>
                  <span>CSS3</span>
                </div>
              </div>
            </div>
            
            <div className="tech-category">
              <h3>Backend</h3>
              <div className="tech-images">
                <div className="tech-item">
                  <img 
                    src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" 
                    alt="FastAPI" 
                    className="tech-logo fastapi-logo"
                  />
                  <span>FastAPI</span>
                </div>
                <div className="tech-item">
                  <img 
                    src="https://wiki.postgresql.org/images/a/a4/PostgreSQL_logo.3colors.svg" 
                    alt="PostgreSQL" 
                    className="tech-logo"
                  />
                  <span>PostgreSQL</span>
                </div>
                <div className="tech-item">
                  <img 
                    src="https://avatars.githubusercontent.com/u/20247959?s=200&v=4" 
                    alt="SQLAlchemy" 
                    className="tech-logo"
                  />
                  <span>SQLAlchemy</span>
                </div>
              </div>
            </div>
            
            <div className="tech-category">
              <h3>Machine Learning</h3>
              <div className="tech-images">
                <div className="tech-item">
                  <img 
                    src="https://upload.wikimedia.org/wikipedia/commons/0/05/Scikit_learn_logo_small.svg" 
                    alt="scikit-learn" 
                    className="tech-logo"
                  />
                  <span>scikit-learn</span>
                </div>
                <div className="tech-item">
                  <img 
                    src="https://pandas.pydata.org/static/img/pandas_mark.svg" 
                    alt="pandas" 
                    className="tech-logo"
                  />
                  <span>pandas</span>
                </div>
                <div className="tech-item">
                  <img 
                    src="https://numpy.org/images/logo.svg" 
                    alt="numpy" 
                    className="tech-logo"
                  />
                  <span>numpy</span>
                </div>
              </div>
            </div>
            
            <div className="tech-category">
              <h3>External APIs</h3>
              <div className="tech-images">
                <div className="tech-item">
                  <div className="tech-logo api-logo">OW</div>
                  <span>OpenWeather API</span>
                </div>
                <div className="tech-item">
                  <div className="tech-logo api-logo">OM</div>
                  <span>Open-Meteo API</span>
                </div>
                <div className="tech-item">
                  <div className="tech-logo api-logo">GOV</div>
                  <span>Indian Agricultural APIs</span>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};

export default About;