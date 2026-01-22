import React, { useState } from 'react';
import { useTranslation } from '../hooks/useTranslation';
import './BioFertilizerGuide.css';

// Import local images
import bioFertilizer1 from '../assets/images/bio-fertilizer-1.jpg';
import soilImprovement from '../assets/images/soil-improvement.jpg';
import reducedChemicals from '../assets/images/reduced-chemicals.jpg';
import rootDevelopment from '../assets/images/root-development.jpg';
import costEffective from '../assets/images/cost-effective.jpg';
import environmentSafe from '../assets/images/environment-safe.jpg';
import organicFarming from '../assets/images/organic-farming.jpg';
import nitrogenFixing from '../assets/images/nitrogen-fixing.jpg';
import phosphateSolubilizing from '../assets/images/phosphate-solubilizing.jpg';
import potassiumMobilizing from '../assets/images/potassium-mobilizing.jpg';
import mycorrhizalFungi from '../assets/images/mycorrhizal-fungi.jpg';
import otherTypes from '../assets/images/other-types.jpg';
import applicationMethods from '../assets/images/application-methods.jpg';
import handlingGuidelines from '../assets/images/handling-guidelines.jpg';
import advantages from '../assets/images/advantages.jpg';
import limitations from '../assets/images/limitations.jpg';
import compatibility from '../assets/images/compatibility.jpg';
import commercialProducts from '../assets/images/commercial-products.jpg';
import qualityParameters from '../assets/images/quality-parameters.jpg';
import futureBioFertilizers from '../assets/images/future-bio-fertilizers.jpg';
import precisionAgriculture from '../assets/images/precision-agriculture.jpg';
import nanoBiofertilizers from '../assets/images/nano-biofertilizers.jpg';
import microbialConsortia from '../assets/images/microbial-consortia.jpg';
import governmentIncentives from '../assets/images/government-incentives.jpg';
import funFacts from '../assets/images/fun-facts.jpg';

const BioFertilizerGuide = () => {
  const { t } = useTranslation();
  const [activeTab, setActiveTab] = useState('overview');

  // Image mapping using local images
  const imageMap = {
    "bio-fertilizer-1": bioFertilizer1,
    "soil-improvement": soilImprovement,
    "reduced-chemicals": reducedChemicals,
    "root-development": rootDevelopment,
    "cost-effective": costEffective,
    "environment-safe": environmentSafe,
    "organic-farming": organicFarming,
    "nitrogen-fixing": nitrogenFixing,
    "phosphate-solubilizing": phosphateSolubilizing,
    "potassium-mobilizing": potassiumMobilizing,
    "mycorrhizal-fungi": mycorrhizalFungi,
    "other-types": otherTypes,
    "application-methods": applicationMethods,
    "handling-guidelines": handlingGuidelines,
    "advantages": advantages,
    "limitations": limitations,
    "compatibility": compatibility,
    "commercial-products": commercialProducts,
    "quality-parameters": qualityParameters,
    "future-bio-fertilizers": futureBioFertilizers,
    "precision-agriculture": precisionAgriculture,
    "nano-biofertilizers": nanoBiofertilizers,
    "microbial-consortia": microbialConsortia,
    "government-incentives": governmentIncentives,
    "fun-facts": funFacts,
  };

  const getImageUrl = (key) => imageMap[key] || bioFertilizer1;

  // Simplified image component for local images
  const LocalImage = ({ src, alt, className }) => {
    return (
      <img
        src={src}
        alt={alt}
        className={className}
        loading="lazy"
        onError={(e) => {
          e.target.style.display = 'none';
        }}
      />
    );
  };

  const renderOverview = () => (
    <div className="tab-content">
      <div className="section-card">
        <h3>{t('bioFertilizer.introduction')}</h3>
        <p>
          {t('bioFertilizer.introContent')}
        </p>
        <div className="intro-image-container">
          <LocalImage
            src={getImageUrl("bio-fertilizer-1")}
            alt={t('bioFertilizer.introduction')}
            className="intro-image"
          />
        </div>
      </div>

      <div className="section-card">
        <h3>{t('bioFertilizer.benefits')}</h3>
        <div className="benefits-grid">
          <div className="benefit-item">
            <LocalImage
              src={getImageUrl("soil-improvement")}
              alt="Soil Improvement"
              className="benefit-icon"
            />
            <p>{t('bioFertilizer.ben1')}</p>
          </div>
          <div className="benefit-item">
            <LocalImage
              src={getImageUrl("reduced-chemicals")}
              alt="Reduced Chemicals"
              className="benefit-icon"
            />
            <p>{t('bioFertilizer.ben2')}</p>
          </div>
          <div className="benefit-item">
            <LocalImage
              src={getImageUrl("root-development")}
              alt="Root Development"
              className="benefit-icon"
            />
            <p>{t('bioFertilizer.ben3')}</p>
          </div>
          <div className="benefit-item">
            <LocalImage
              src={getImageUrl("cost-effective")}
              alt="Cost Effective"
              className="benefit-icon"
            />
            <p>{t('bioFertilizer.ben4')}</p>
          </div>
          <div className="benefit-item">
            <LocalImage
              src={getImageUrl("environment-safe")}
              alt="Environment Safe"
              className="benefit-icon"
            />
            <p>{t('bioFertilizer.ben5')}</p>
          </div>
          <div className="benefit-item">
            <LocalImage
              src={getImageUrl("organic-farming")}
              alt="Organic Farming"
              className="benefit-icon"
            />
            <p>{t('bioFertilizer.ben6')}</p>
          </div>
        </div>
      </div>
    </div>
  );

  const renderTypes = () => (
    <div className="tab-content">
      <div className="section-card">
        <h3>{t('bioFertilizer.majorTypes')}</h3>

        <div className="fertilizer-category">
          <div className="category-header">
            <LocalImage
              src={getImageUrl("nitrogen-fixing")}
              alt="Nitrogen Fixing"
              className="category-icon"
            />
            <h4>{t('bioFertilizer.nFixing')}</h4>
          </div>
          <p><strong>{t('fertilizer.function')}:</strong> {t('bioFertilizer.nFixingFunc')}</p>
          <div className="image-container">
            <LocalImage
              src={getImageUrl("nitrogen-fixing")}
              alt="Nitrogen Fixation"
              className="content-image"
            />
          </div>
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>{t('bioFertilizer.microorganism')}</th>
                  <th>{t('bioFertilizer.worksBestFor')}</th>
                  <th>{t('bioFertilizer.description')}</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>Rhizobium</strong></td>
                  <td>{t('bioFertilizer.legumes')}</td>
                  <td>{t('bioFertilizer.rhizobiumDesc')}</td>
                </tr>
                <tr>
                  <td><strong>Azotobacter</strong></td>
                  <td>{t('bioFertilizer.nonLegumes')}</td>
                  <td>{t('bioFertilizer.azotobacterDesc')}</td>
                </tr>
                <tr>
                  <td><strong>Azospirillum</strong></td>
                  <td>{t('bioFertilizer.cereals')}</td>
                  <td>{t('bioFertilizer.azospirillumDesc')}</td>
                </tr>
                <tr>
                  <td><strong>BGA (Blue Green Algae)</strong></td>
                  <td>{t('bioFertilizer.paddy')}</td>
                  <td>{t('bioFertilizer.bgaDesc')}</td>
                </tr>
                <tr>
                  <td><strong>Azolla-Anabaena</strong></td>
                  <td>{t('bioFertilizer.rice')}</td>
                  <td>{t('bioFertilizer.azollaDesc')}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div className="fertilizer-category">
          <div className="category-header">
            <LocalImage
              src={getImageUrl("phosphate-solubilizing")}
              alt="Phosphate Solubilizing"
              className="category-icon"
            />
            <h4>{t('bioFertilizer.psbTitle')}</h4>
          </div>
          <div className="image-container">
            <LocalImage
              src={getImageUrl("phosphate-solubilizing")}
              alt={t('bioFertilizer.psbTitle')}
              className="content-image"
            />
          </div>
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>{t('bioFertilizer.microorganism')}</th>
                  <th>{t('fertilizer.function')}</th>
                  <th>{t('bioFertilizer.crops')}</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>Bacillus megaterium</strong></td>
                  <td>{t('bioFertilizer.bacillusDesc')}</td>
                  <td>{t('bioFertilizer.cerealsLegumes')}</td>
                </tr>
                <tr>
                  <td><strong>Pseudomonas striata</strong></td>
                  <td>{t('bioFertilizer.pseudomonasDesc')}</td>
                  <td>{t('bioFertilizer.vegFruits')}</td>
                </tr>
                <tr>
                  <td><strong>Aspergillus spp.</strong></td>
                  <td>{t('bioFertilizer.aspergillusDesc')}</td>
                  <td>{t('bioFertilizer.multiCrop')}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div className="fertilizer-category">
          <div className="category-header">
            <LocalImage
              src={getImageUrl("potassium-mobilizing")}
              alt="Potassium Mobilizing"
              className="category-icon"
            />
            <h4>{t('bioFertilizer.kMobilizing')}</h4>
          </div>
          <div className="image-container">
            <LocalImage
              src={getImageUrl("potassium-mobilizing")}
              alt={t('bioFertilizer.kMobilizing')}
              className="content-image"
            />
          </div>
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>{t('bioFertilizer.microorganism')}</th>
                  <th>{t('fertilizer.function')}</th>
                  <th>{t('bioFertilizer.crops')}</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>Frateuria aurantia</strong></td>
                  <td>{t('bioFertilizer.kMobilizingDesc')}</td>
                  <td>{t('bioFertilizer.maizeSugarcane')}</td>
                </tr>
                <tr>
                  <td><strong>Bacillus mucilaginosus</strong></td>
                  <td>{t('bioFertilizer.bacillusMucDesc')}</td>
                  <td>{t('bioFertilizer.horticulture')}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div className="fertilizer-category">
          <div className="category-header">
            <LocalImage
              src={getImageUrl("mycorrhizal-fungi")}
              alt="Mycorrhizal Fungi"
              className="category-icon"
            />
            <h4>{t('bioFertilizer.vam')}</h4>
          </div>
          <p><strong>{t('bioFertilizer.vamDesc')}</strong></p>
          <div className="image-container">
            <LocalImage
              src={getImageUrl("mycorrhizal-fungi")}
              alt={t('bioFertilizer.vam')}
              className="content-image"
            />
          </div>
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>{t('bioFertilizer.type')}</th>
                  <th>{t('fertilizer.function')}</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>Glomus spp.</strong></td>
                  <td>{t('bioFertilizer.glomusDesc')}</td>
                </tr>
                <tr>
                  <td><strong>Gigaspora spp.</strong></td>
                  <td>{t('bioFertilizer.gigasporaDesc')}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div className="fertilizer-category">
          <div className="category-header">
            <LocalImage
              src={getImageUrl("other-types")}
              alt="Other Types"
              className="category-icon"
            />
            <h4>{t('bioFertilizer.otherTypes')}</h4>
          </div>
          <div className="image-container">
            <LocalImage
              src={getImageUrl("other-types")}
              alt={t('bioFertilizer.otherTypes')}
              className="content-image"
            />
          </div>
          <ul className="other-types-list">
            <li><strong>{t('bioFertilizer.sulphurOxidizers')}</strong> {t('bioFertilizer.sulphurOxidizersDesc')}</li>
            <li><strong>{t('bioFertilizer.zincSolubilizers')}</strong> <em>Bacillus subtilis</em> {t('and')} <em>Pseudomonas fluorescens</em> {t('bioFertilizer.zincSolubilizersDesc')}</li>
            <li><strong>{t('bioFertilizer.pgpr')}</strong> {t('bioFertilizer.pgprDesc')}</li>
          </ul>
        </div>
      </div>
    </div>
  );

  const renderApplication = () => (
    <div className="tab-content">
      <div className="section-card">
        <h3>{t('bioFertilizer.appMethods')}</h3>
        <div className="image-container">
          <LocalImage
            src={getImageUrl("application-methods")}
            alt={t('bioFertilizer.appMethods')}
            className="content-image"
          />
        </div>
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>{t('bioFertilizer.method')}</th>
                <th>{t('bioFertilizer.description')}</th>
                <th>{t('bioFertilizer.exampleUse')}</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>{t('bioFertilizer.seedTreatment')}</strong></td>
                <td>{t('bioFertilizer.seedTreatmentDesc')}</td>
                <td>Rhizobium, Azotobacter</td>
              </tr>
              <tr>
                <td><strong>{t('bioFertilizer.rootDip')}</strong></td>
                <td>{t('bioFertilizer.rootDipDesc')}</td>
                <td>Rice, tomato</td>
              </tr>
              <tr>
                <td><strong>{t('bioFertilizer.soilApp')}</strong></td>
                <td>{t('bioFertilizer.soilAppDesc')}</td>
                <td>PSB, KMB, Mycorrhiza</td>
              </tr>
              <tr>
                <td><strong>{t('bioFertilizer.foliar')}</strong></td>
                <td>{t('bioFertilizer.foliarDesc')}</td>
                <td>PGPR, Azospirillum</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div className="section-card">
        <h3>{t('bioFertilizer.handling')}</h3>
        <div className="image-container">
          <LocalImage
            src={getImageUrl("handling-guidelines")}
            alt={t('bioFertilizer.handling')}
            className="content-image"
          />
        </div>
        <div className="guidelines-grid">
          <div className="guideline-item">
            <LocalImage
              src={getImageUrl("reduced-chemicals")}
              alt="Chemical Mixing"
              className="guideline-icon"
            />
            <p>{t('bioFertilizer.avoidMixing')}</p>
          </div>
          <div className="guideline-item">
            <LocalImage
              src={getImageUrl("environment-safe")}
              alt="Storage"
              className="guideline-icon"
            />
            <p>{t('bioFertilizer.storeCool')}</p>
          </div>
          <div className="guideline-item">
            <LocalImage
              src={getImageUrl("soil-improvement")}
              alt="Sunlight"
              className="guideline-icon"
            />
            <p>{t('bioFertilizer.avoidSun')}</p>
          </div>
          <div className="guideline-item">
            <LocalImage
              src={getImageUrl("quality-parameters")}
              alt="Expiry"
              className="guideline-icon"
            />
            <p>{t('bioFertilizer.expiry')}</p>
          </div>
        </div>
      </div>
    </div>
  );

  const renderAdvantages = () => (
    <div className="tab-content">
      <div className="section-card">
        <h3>{t('bioFertilizer.advantages')}</h3>
        <div className="image-container">
          <LocalImage
            src={getImageUrl("advantages")}
            alt={t('bioFertilizer.advantages')}
            className="content-image"
          />
        </div>
        <ul className="advantages-list">
          <li>{t('bioFertilizer.adv1')}</li>
          <li>{t('bioFertilizer.adv2')}</li>
          <li>{t('bioFertilizer.adv3')}</li>
          <li>{t('bioFertilizer.adv4')}</li>
          <li>{t('bioFertilizer.adv5')}</li>
        </ul>
      </div>

      <div className="section-card">
        <h3>{t('bioFertilizer.limitations')}</h3>
        <div className="image-container">
          <LocalImage
            src={getImageUrl("limitations")}
            alt={t('bioFertilizer.limitations')}
            className="content-image"
          />
        </div>
        <ul className="limitations-list">
          <li>{t('bioFertilizer.lim1')}</li>
          <li>{t('bioFertilizer.lim2')}</li>
          <li>{t('bioFertilizer.lim3')}</li>
          <li>{t('bioFertilizer.lim4')}</li>
        </ul>
      </div>

      <div className="section-card">
        <h3>{t('bioFertilizer.compatibility')}</h3>
        <div className="image-container">
          <LocalImage
            src={getImageUrl("compatibility")}
            alt={t('bioFertilizer.compatibility')}
            className="content-image"
          />
        </div>
        <div className="combinations-grid">
          <div className="combination-item">
            <strong>Rhizobium + PSB</strong>
            <span>→ {t('bioFertilizer.legumes')}</span>
          </div>
          <div className="combination-item">
            <strong>Azotobacter + PSB + KMB</strong>
            <span>→ {t('bioFertilizer.cerealsLegumes')}</span>
          </div>
          <div className="combination-item">
            <strong>VAM + PGPR</strong>
            <span>→ {t('bioFertilizer.vegFruits')}</span>
          </div>
        </div>
      </div>
    </div>
  );

  const renderProducts = () => (
    <div className="tab-content">
      <div className="section-card">
        <h3>{t('bioFertilizer.popularProducts')}</h3>
        <div className="image-container">
          <LocalImage
            src={getImageUrl("commercial-products")}
            alt={t('bioFertilizer.popularProducts')}
            className="content-image"
          />
        </div>
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>{t('bioFertilizer.brand')}</th>
                <th>{t('bioFertilizer.composition')}</th>
                <th>{t('bioFertilizer.recommended')}</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Bio-N</strong></td>
                <td>Azospirillum + Azotobacter</td>
                <td>{t('bioFertilizer.cereals')}</td>
              </tr>
              <tr>
                <td><strong>RhizoMix</strong></td>
                <td>Rhizobium</td>
                <td>{t('bioFertilizer.legumes')}</td>
              </tr>
              <tr>
                <td><strong>Phospho-Rich</strong></td>
                <td>PSB</td>
                <td>{t('bioFertilizer.vegFruits')}</td>
              </tr>
              <tr>
                <td><strong>Potash-King</strong></td>
                <td>KMB</td>
                <td>{t('bioFertilizer.maizeSugarcane')}</td>
              </tr>
              <tr>
                <td><strong>MycoGrow</strong></td>
                <td>VAM fungi</td>
                <td>{t('bioFertilizer.vegFruits')}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div className="section-card">
        <h3>{t('bioFertilizer.qualityParams')}</h3>
        <div className="image-container">
          <LocalImage
            src={getImageUrl("quality-parameters")}
            alt={t('bioFertilizer.qualityParams')}
            className="content-image"
          />
        </div>
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>{t('bioFertilizer.parameter')}</th>
                <th>{t('bioFertilizer.standard')}</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>{t('bioFertilizer.viableCount')}</td>
                <td>≥10⁷ CFU/g {t('or')} ml</td>
              </tr>
              <tr>
                <td>{t('bioFertilizer.moisture')}</td>
                <td>&lt;30%</td>
              </tr>
              <tr>
                <td>{t('bioFertilizer.phRange')}</td>
                <td>6.5 – 7.5</td>
              </tr>
              <tr>
                <td>{t('bioFertilizer.shelfLife')}</td>
                <td>6–12 {t('months')}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );

  const renderFuture = () => (
    <div className="tab-content">
      <div className="section-card">
        <h3>{t('bioFertilizer.future')}</h3>
        <p>
          {t('bioFertilizer.futureContent')}
        </p>
        <div className="image-container">
          <LocalImage
            src={getImageUrl("future-bio-fertilizers")}
            alt={t('bioFertilizer.future')}
            className="content-image"
          />
        </div>

        <div className="future-grid">
          <div className="future-item">
            <LocalImage
              src={getImageUrl("precision-agriculture")}
              alt={t('bioFertilizer.precisionAg')}
              className="future-icon"
            />
            <h4>{t('bioFertilizer.precisionAg')}</h4>
            <p>{t('bioFertilizer.precisionAgDesc')}</p>
          </div>
          <div className="future-item">
            <LocalImage
              src={getImageUrl("nano-biofertilizers")}
              alt={t('bioFertilizer.nanoBio')}
              className="future-icon"
            />
            <h4>{t('bioFertilizer.nanoBio')}</h4>
            <p>{t('bioFertilizer.nanoBioDesc')}</p>
          </div>
          <div className="future-item">
            <LocalImage
              src={getImageUrl("microbial-consortia")}
              alt={t('bioFertilizer.microbial')}
              className="future-icon"
            />
            <h4>{t('bioFertilizer.microbial')}</h4>
            <p>{t('bioFertilizer.microbialDesc')}</p>
          </div>
          <div className="future-item">
            <LocalImage
              src={getImageUrl("government-incentives")}
              alt={t('bioFertilizer.govtSupport')}
              className="future-icon"
            />
            <h4>{t('bioFertilizer.govtSupport')}</h4>
            <p>{t('bioFertilizer.govtSupportDesc')}</p>
          </div>
        </div>
      </div>

      <div className="section-card">
        <h3>{t('bioFertilizer.funFacts')}</h3>
        <div className="image-container">
          <LocalImage
            src={getImageUrl("fun-facts")}
            alt={t('bioFertilizer.funFacts')}
            className="content-image"
          />
        </div>
        <div className="facts-grid">
          <div className="fact-card">
            <h3>1 kg</h3>
            <p>{t('bioFertilizer.fact1')}</p>
          </div>
          <div className="fact-card">
            <h3>1.5 million tons</h3>
            <p>{t('bioFertilizer.fact2')}</p>
          </div>
          <div className="fact-card">
            <h3>30%</h3>
            <p>{t('bioFertilizer.fact3')}</p>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="bio-fertilizer-guide">
      <div className="container">
        <header className="page-header">
          <h1>{t('bioFertilizer.pageTitle')}</h1>
          <p className="page-subtitle">
            {t('bioFertilizer.pageSubtitle')}
          </p>
        </header>

        <div className="tabs-container">
          <div className="tabs">
            <button
              className={`tab ${activeTab === 'overview' ? 'active' : ''}`}
              onClick={() => setActiveTab('overview')}
            >
              {t('fertilizer.overview')}
            </button>
            <button
              className={`tab ${activeTab === 'types' ? 'active' : ''}`}
              onClick={() => setActiveTab('types')}
            >
              {t('bioFertilizer.typesTab')}
            </button>
            <button
              className={`tab ${activeTab === 'application' ? 'active' : ''}`}
              onClick={() => setActiveTab('application')}
            >
              {t('bioFertilizer.appTab')}
            </button>
            <button
              className={`tab ${activeTab === 'advantages' ? 'active' : ''}`}
              onClick={() => setActiveTab('advantages')}
            >
              {t('bioFertilizer.advTab')}
            </button>
            <button
              className={`tab ${activeTab === 'products' ? 'active' : ''}`}
              onClick={() => setActiveTab('products')}
            >
              {t('bioFertilizer.productsTab')}
            </button>
            <button
              className={`tab ${activeTab === 'future' ? 'active' : ''}`}
              onClick={() => setActiveTab('future')}
            >
              {t('bioFertilizer.futureTab')}
            </button>
          </div>

          <div className="tab-content-container">
            {activeTab === 'overview' && renderOverview()}
            {activeTab === 'types' && renderTypes()}
            {activeTab === 'application' && renderApplication()}
            {activeTab === 'advantages' && renderAdvantages()}
            {activeTab === 'products' && renderProducts()}
            {activeTab === 'future' && renderFuture()}
          </div>
        </div>

        <div className="success-message">
          <p>{t('bioFertilizer.successMsg')}</p>
        </div>
      </div>
    </div>
  );
};

export default BioFertilizerGuide;