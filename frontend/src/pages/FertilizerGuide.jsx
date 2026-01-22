import React, { useState } from "react";
import { useTranslation } from '../hooks/useTranslation';
import "./FertilizerGuide.css";

// Import local images
import nitrogenFertilizer from "../assets/images/nitrogen_fertilizer.jpg";
import phosphorusFertilizer from "../assets/images/phosphorus_fertilizer.jpg";
import potassiumFertilizer from "../assets/images/potassium_fertilizer.jpg";
import organicFertilizer from "../assets/images/organic_fertilizer.jpg";
import compostFertilizer from "../assets/images/compost_fertilizer.jpg";
import farmyardManure from "../assets/images/farmyard_manure.jpg";
import vermicompost from "../assets/images/vermicompost.jpg";
import biofertilizerBacteria from "../assets/images/biofertilizer_bacteria.jpg";
import rhizobiumCulture from "../assets/images/rhizobium_culture.jpg";
import mycorrhizaFungi from "../assets/images/mycorrhiza_fungi.jpg";
import fertilizerApplication from "../assets/images/fertilizer_application.jpg";
import fertigationMethod from "../assets/images/fertigation_method.jpg";
import soilHealth from "../assets/images/soil_health.jpg";
import nutrientManagement from "../assets/images/nutrient_management.jpg";

// New specific method images
import bandPlacement from "../assets/images/Band Placement.jfif";
import broadcasting from "../assets/images/Broadcasting Uniformly.jpg";
import foliarSpray from "../assets/images/Foliar Spray.jfif";
import safeHandling from "../assets/images/Safe Handling of Fertilizers.jpg";

const FertilizerGuide = () => {
  const { t } = useTranslation();
  const [activeTab, setActiveTab] = useState("overview");

  // Image mapping
  const imageMap = {
    "nitrogen-fertilizer": nitrogenFertilizer,
    "phosphorus-fertilizer": phosphorusFertilizer,
    "potassium-fertilizer": potassiumFertilizer,
    "organic-fertilizer": organicFertilizer,
    "compost-fertilizer": compostFertilizer,
    "farmyard-manure": farmyardManure,
    "vermicompost": vermicompost,
    "biofertilizer-bacteria": biofertilizerBacteria,
    "rhizobium-culture": rhizobiumCulture,
    "mycorrhiza-fungi": mycorrhizaFungi,
    "fertilizer-application": fertilizerApplication,
    "fertigation-method": fertigationMethod,
    "soil-health": soilHealth,
    "nutrient-management": nutrientManagement,
    "band-placement": bandPlacement,
    "broadcasting": broadcasting,
    "foliar-spray": foliarSpray,
    "safe-handling": safeHandling,
  };

  const getImageUrl = (key) => imageMap[key] || nitrogenFertilizer;

  // Simple image component for local images with consistent sizing
  const LocalImage = ({ src, alt, className }) => {
    return (
      <img
        src={src}
        alt={alt}
        className={className}
        loading="lazy"
      />
    );
  };

  const TabButton = ({ id, label }) => (
    <button
      className={`tab ${activeTab === id ? "active" : ""}`}
      onClick={() => setActiveTab(id)}
    >
      {label}
    </button>
  );

  /* ---------- Overview ---------- */
  const renderOverview = () => (
    <div className="tab-content">
      <section className="card info-card">
        <header>
          <span className="badge">{t('fertilizer.overview')}</span>
          <h2>{t('fertilizer.comprehensiveGuide')}</h2>
          <p className="section-description">
            {t('fertilizer.guideDescription')}
          </p>
        </header>

        <div className="info-content">
          <p>
            {t('fertilizer.overviewContent')}
          </p>
          <div className="image-container">
            <LocalImage
              src={getImageUrl("nutrient-management")}
              alt="Nutrient Management"
              className="content-image"
            />
          </div>
        </div>
      </section>
    </div>
  );

  /* ---------- Macronutrients (NPK) ---------- */
  const renderMacronutrients = () => (
    <div className="tab-content">
      <section className="card nutrient-card">
        <header>
          <span className="badge">{t('fertilizer.macronutrients')}</span>
          <h2>{t('fertilizer.understandingNPK')}</h2>
          <p className="section-description">
            {t('fertilizer.npkDescription')}
          </p>
        </header>

        <div className="nutrient-grid">
          {/* N, P, K items are preserved exactly as provided */}
          <article className="nutrient-item">
            <div className="nutrient-head">
              <span className="nutrient-icon">🟢</span>
              <h3>Nitrogen (N)</h3>
            </div>
            <div className="nutrient-details">
              <p className="nutrient-role"><strong>{t('fertilizer.role')}:</strong> {t('fertilizer.nitrogenRole')}</p>
              <p className="nutrient-deficiency"><strong>{t('fertilizer.deficiency')}:</strong> {t('fertilizer.nitrogenDeficiency')}</p>
              <p className="nutrient-excess"><strong>{t('fertilizer.excess')}:</strong> {t('fertilizer.nitrogenExcess')}</p>
              <div className="nutrient-sources">
                <strong>{t('fertilizer.sources')}:</strong>
                <ul className="source-list">
                  <li>Urea (46% N)</li>
                  <li>Ammonium nitrate (33% N)</li>
                  <li>Ammonium sulphate (21% N)</li>
                  <li>Compost or FYM (0.5-2% N)</li>
                  <li>Green manure (1-3% N)</li>
                  <li>Rhizobium inoculant</li>
                </ul>
              </div>
              <p className="nutrient-application"><strong>{t('fertilizer.application')}:</strong> {t('fertilizer.nitrogenApplication')}</p>
              <p className="nutrient-timing"><strong>{t('fertilizer.timing')}:</strong> {t('fertilizer.nitrogenTiming')}</p>
              <p className="nutrient-crops"><strong>{t('fertilizer.criticalFor')}:</strong> {t('fertilizer.nitrogenCrops')}</p>
            </div>
            <div className="image-container">
              <LocalImage
                src={getImageUrl("nitrogen-fertilizer")}
                alt="Nitrogen Fertilizer"
                className="content-image"
              />
            </div>
          </article>

          <article className="nutrient-item">
            <div className="nutrient-head">
              <span className="nutrient-icon">🔵</span>
              <h3>Phosphorus (P)</h3>
            </div>
            <div className="nutrient-details">
              <p className="nutrient-role"><strong>{t('fertilizer.role')}:</strong> {t('fertilizer.phosphorusRole')}</p>
              <p className="nutrient-deficiency"><strong>{t('fertilizer.deficiency')}:</strong> {t('fertilizer.phosphorusDeficiency')}</p>
              <p className="nutrient-excess"><strong>{t('fertilizer.excess')}:</strong> {t('fertilizer.phosphorusExcess')}</p>
              <div className="nutrient-sources">
                <strong>{t('fertilizer.sources')}:</strong>
                <ul className="source-list">
                  <li>Single super phosphate (16% P₂O₅)</li>
                  <li>Triple super phosphate (46% P₂O₅)</li>
                  <li>Bone meal (15-20% P)</li>
                  <li>Rock phosphate (25-30% P)</li>
                  <li>PSB biofertilizer</li>
                  <li>Compost enriched with bone meal</li>
                </ul>
              </div>
              <p className="nutrient-application"><strong>{t('fertilizer.application')}:</strong> {t('fertilizer.phosphorusApplication')}</p>
              <p className="nutrient-timing"><strong>{t('fertilizer.timing')}:</strong> {t('fertilizer.phosphorusTiming')}</p>
              <p className="nutrient-crops"><strong>{t('fertilizer.criticalFor')}:</strong> {t('fertilizer.phosphorusCrops')}</p>
            </div>
            <div className="image-container">
              <LocalImage
                src={getImageUrl("phosphorus-fertilizer")}
                alt="Phosphorus Fertilizer"
                className="content-image"
              />
            </div>
          </article>

          <article className="nutrient-item">
            <div className="nutrient-head">
              <span className="nutrient-icon">🟠</span>
              <h3>Potassium (K)</h3>
            </div>
            <div className="nutrient-details">
              <p className="nutrient-role"><strong>{t('fertilizer.role')}:</strong> {t('fertilizer.potassiumRole')}</p>
              <p className="nutrient-deficiency"><strong>{t('fertilizer.deficiency')}:</strong> {t('fertilizer.potassiumDeficiency')}</p>
              <p className="nutrient-excess"><strong>{t('fertilizer.excess')}:</strong> {t('fertilizer.potassiumExcess')}</p>
              <div className="nutrient-sources">
                <strong>{t('fertilizer.sources')}:</strong>
                <ul className="source-list">
                  <li>Muriate of potash (60% K₂O)</li>
                  <li>Sulphate of potash (50% K₂O)</li>
                  <li>Wood ash (5-10% K)</li>
                  <li>Banana peel compost</li>
                  <li>Potash mobilizing bacteria (KMB)</li>
                  <li>Coconut coir pith</li>
                </ul>
              </div>
              <p className="nutrient-application"><strong>{t('fertilizer.application')}:</strong> {t('fertilizer.potassiumApplication')}</p>
              <p className="nutrient-timing"><strong>{t('fertilizer.timing')}:</strong> {t('fertilizer.potassiumTiming')}</p>
              <p className="nutrient-crops"><strong>{t('fertilizer.criticalFor')}:</strong> {t('fertilizer.potassiumCrops')}</p>
            </div>
            <div className="image-container">
              <LocalImage
                src={getImageUrl("potassium-fertilizer")}
                alt="Potassium Fertilizer"
                className="content-image"
              />
            </div>
          </article>
        </div>
      </section>
    </div>
  );

  /* ---------- Secondary & Micronutrients ---------- */
  const renderSecondaryMicro = () => (
    <div className="tab-content">
      <section className="card secondary-card">
        <header>
          <span className="badge">{t('fertilizer.secondaryNutrients')}</span>
          <h2>{t('fertilizer.calciumMagnesiumSulphur')}</h2>
          <p className="section-description">
            {t('fertilizer.secondaryDescription')}
          </p>
        </header>
        <div className="secondary-grid">
          <article className="secondary-item">
            <h3>{t('fertilizer.calcium')}</h3>
            <p><strong>{t('fertilizer.role')}:</strong> {t('fertilizer.calciumRole')}</p>
            <p><strong>{t('fertilizer.deficiency')}:</strong> {t('fertilizer.calciumDeficiency')}</p>
            <div className="nutrient-sources">
              <strong>{t('fertilizer.sources')}:</strong>
              <ul className="source-list">
                <li>Gypsum (CaSO₄)</li>
                <li>Lime (CaCO₃)</li>
                <li>Bone meal</li>
                <li>Eggshell powder</li>
              </ul>
            </div>
          </article>

          <article className="secondary-item">
            <h3>{t('fertilizer.magnesium')}</h3>
            <p><strong>{t('fertilizer.role')}:</strong> {t('fertilizer.magnesiumRole')}</p>
            <p><strong>{t('fertilizer.deficiency')}:</strong> {t('fertilizer.magnesiumDeficiency')}</p>
            <div className="nutrient-sources">
              <strong>{t('fertilizer.sources')}:</strong>
              <ul className="source-list">
                <li>Epsom salt (MgSO₄)</li>
                <li>Dolomite lime</li>
                <li>Magnesium oxide</li>
              </ul>
            </div>
          </article>

          <article className="secondary-item">
            <h3>{t('fertilizer.sulphur')}</h3>
            <p><strong>{t('fertilizer.role')}:</strong> {t('fertilizer.sulphurRole')}</p>
            <p><strong>{t('fertilizer.deficiency')}:</strong> {t('fertilizer.sulphurDeficiency')}</p>
            <div className="nutrient-sources">
              <strong>{t('fertilizer.sources')}:</strong>
              <ul className="source-list">
                <li>Gypsum</li>
                <li>Ammonium sulphate</li>
                <li>Elemental sulphur</li>
                <li>Compost</li>
              </ul>
            </div>
          </article>
        </div>
      </section>

      <section className="card micro-card">
        <header>
          <span className="badge">{t('fertilizer.micronutrients')}</span>
          <h2>{t('fertilizer.traceElements')}</h2>
          <p className="section-description">
            {t('fertilizer.traceDescription')}
          </p>
        </header>
        <div className="micro-grid">
          <article className="micro-item">
            <h4>{t('fertilizer.zinc')}</h4>
            <p><strong>{t('fertilizer.role')}:</strong> {t('fertilizer.zincRole')}</p>
            <p><strong>{t('fertilizer.deficiency')}:</strong> {t('fertilizer.zincDeficiency')}</p>
            <p><strong>{t('fertilizer.sources')}:</strong> Zinc sulphate, zinc oxide, zinc chelates</p>
          </article>

          <article className="micro-item">
            <h4>{t('fertilizer.iron')}</h4>
            <p><strong>{t('fertilizer.role')}:</strong> {t('fertilizer.ironRole')}</p>
            <p><strong>{t('fertilizer.deficiency')}:</strong> {t('fertilizer.ironDeficiency')}</p>
            <p><strong>{t('fertilizer.sources')}:</strong> Ferrous sulphate, iron chelates, compost</p>
          </article>

          <article className="micro-item">
            <h4>{t('fertilizer.manganese')}</h4>
            <p><strong>{t('fertilizer.role')}:</strong> {t('fertilizer.manganeseRole')}</p>
            <p><strong>{t('fertilizer.deficiency')}:</strong> {t('fertilizer.manganeseDeficiency')}</p>
            <p><strong>{t('fertilizer.sources')}:</strong> Manganese sulphate, manganese oxide</p>
          </article>

          <article className="micro-item">
            <h4>{t('fertilizer.boron')}</h4>
            <p><strong>{t('fertilizer.role')}:</strong> {t('fertilizer.boronRole')}</p>
            <p><strong>{t('fertilizer.deficiency')}:</strong> {t('fertilizer.boronDeficiency')}</p>
            <p><strong>{t('fertilizer.sources')}:</strong> Borax, boric acid, compost</p>
          </article>

          <article className="micro-item">
            <h4>{t('fertilizer.copper')}</h4>
            <p><strong>{t('fertilizer.role')}:</strong> {t('fertilizer.copperRole')}</p>
            <p><strong>{t('fertilizer.deficiency')}:</strong> {t('fertilizer.copperDeficiency')}</p>
            <p><strong>{t('fertilizer.sources')}:</strong> Copper sulphate, copper chelates</p>
          </article>

          <article className="micro-item">
            <h4>{t('fertilizer.molybdenum')}</h4>
            <p><strong>{t('fertilizer.role')}:</strong> {t('fertilizer.molybdenumRole')}</p>
            <p><strong>{t('fertilizer.deficiency')}:</strong> {t('fertilizer.molybdenumDeficiency')}</p>
            <p><strong>{t('fertilizer.sources')}:</strong> Sodium molybdate, molybdenum trioxide</p>
          </article>
        </div>
      </section>
    </div>
  );

  /* ---------- Organic Fertilizers ---------- */
  const renderOrganic = () => (
    <div className="tab-content">
      <section className="card organic-card">
        <header>
          <span className="badge">{t('fertilizer.organicAmendments')}</span>
          <h2>{t('fertilizer.naturalEnhancers')}</h2>
          <p className="section-description">
            {t('fertilizer.organicDescription')}
          </p>
        </header>
        <div className="organic-grid">
          <article className="organic-item">
            <h3>{t('fertilizer.compost')}</h3>
            <p><strong>{t('fertilizer.advantages')}:</strong> {t('fertilizer.compostBenefits')}</p>
            <p><strong>{t('fertilizer.application')}:</strong> {t('fertilizer.compostApp')}</p>
            <div className="image-container">
              <LocalImage
                src={getImageUrl("compost-fertilizer")}
                alt="Compost Fertilizer"
                className="content-image"
              />
            </div>
          </article>

          <article className="organic-item">
            <h3>{t('fertilizer.fym')}</h3>
            <p><strong>{t('fertilizer.advantages')}:</strong> {t('fertilizer.fymBenefits')}</p>
            <p><strong>{t('fertilizer.application')}:</strong> {t('fertilizer.fymApp')}</p>
            <div className="image-container">
              <LocalImage
                src={getImageUrl("farmyard-manure")}
                alt="Farmyard Manure"
                className="content-image"
              />
            </div>
          </article>

          <article className="organic-item">
            <h3>{t('fertilizer.vermicompost')}</h3>
            <p><strong>{t('fertilizer.advantages')}:</strong> {t('fertilizer.vermicompostBenefits')}</p>
            <p><strong>{t('fertilizer.application')}:</strong> {t('fertilizer.vermicompostApp')}</p>
            <div className="image-container">
              <LocalImage
                src={getImageUrl("vermicompost")}
                alt="Vermicompost"
                className="content-image"
              />
            </div>
          </article>

          <article className="organic-item">
            <h3>{t('fertilizer.greenManure')}</h3>
            <p><strong>{t('fertilizer.advantages')}:</strong> {t('fertilizer.greenManureBenefits')}</p>
            <p><strong>{t('fertilizer.application')}:</strong> {t('fertilizer.greenManureApp')}</p>
            <div className="image-container">
              <LocalImage
                src={getImageUrl("organic-fertilizer")}
                alt="Organic Fertilizer"
                className="content-image"
              />
            </div>
          </article>
        </div>
      </section>
    </div>
  );

  /* ---------- Biofertilizers ---------- */
  const renderBiofertilizers = () => (
    <div className="tab-content">
      <section className="card bio-card">
        <header>
          <span className="badge">{t('fertilizer.biofertilizers')}</span>
          <h2>{t('fertilizer.livingEnhancers')}</h2>
          <p className="section-description">
            {t('fertilizer.bioDescription')}
          </p>
        </header>
        <div className="bio-grid">
          <article className="bio-item">
            <h3>{t('fertilizer.rhizobium')}</h3>
            <p><strong>{t('fertilizer.role')}:</strong> {t('fertilizer.rhizobiumFunc')}</p>
            <p><strong>{t('fertilizer.criticalFor')}:</strong> {t('fertilizer.rhizobiumCrops')}</p>
            <p><strong>{t('fertilizer.application')}:</strong> {t('fertilizer.rhizobiumApp')}</p>
            <div className="image-container">
              <LocalImage
                src={getImageUrl("rhizobium-culture")}
                alt="Rhizobium Culture"
                className="content-image"
              />
            </div>
          </article>

          <article className="bio-item">
            <h3>{t('fertilizer.psb')}</h3>
            <p><strong>{t('fertilizer.role')}:</strong> {t('fertilizer.psbFunc')}</p>
            <p><strong>{t('fertilizer.criticalFor')}:</strong> {t('fertilizer.psbCrops')}</p>
            <p><strong>{t('fertilizer.application')}:</strong> {t('fertilizer.psbApp')}</p>
            <div className="image-container">
              <LocalImage
                src={getImageUrl("biofertilizer-bacteria")}
                alt="Biofertilizer Bacteria"
                className="content-image"
              />
            </div>
          </article>

          <article className="bio-item">
            <h3>{t('fertilizer.mycorrhizae')}</h3>
            <p><strong>{t('fertilizer.role')}:</strong> {t('fertilizer.mycorrhizaeFunc')}</p>
            <p><strong>{t('fertilizer.criticalFor')}:</strong> {t('fertilizer.mycorrhizaeCrops')}</p>
            <p><strong>{t('fertilizer.application')}:</strong> {t('fertilizer.mycorrhizaeApp')}</p>
            <div className="image-container">
              <LocalImage
                src={getImageUrl("mycorrhiza-fungi")}
                alt="Mycorrhiza Fungi"
                className="content-image"
              />
            </div>
          </article>
        </div>
      </section>
    </div>
  );

  /* ---------- Application Methods & Timing ---------- */
  const renderApplicationTiming = () => (
    <div className="tab-content">
      <section className="card method-card">
        <header>
          <span className="badge">{t('fertilizer.application')}</span>
          <h2>{t('fertilizer.effectiveDelivery')}</h2>
          <p className="section-description">
            {t('fertilizer.deliveryDescription')}
          </p>
        </header>
        <div className="method-grid">
          <article className="method-item">
            <h3>{t('fertilizer.broadcasting')}</h3>
            <p className="method-description">{t('fertilizer.broadcastingDesc')}</p>
            <div className="method-pros"><strong>{t('fertilizer.advantages')}:</strong> {t('fertilizer.broadcastingPros')}</div>
            <div className="method-cons"><strong>{t('fertilizer.limitations')}:</strong> {t('fertilizer.broadcastingCons')}</div>
            <p className="method-best"><strong>{t('fertilizer.bestFor')}:</strong> {t('fertilizer.broadcastingBest')}</p>
            <div className="image-container">
              <LocalImage
                src={getImageUrl("broadcasting")}
                alt="Broadcasting Fertilizer"
                className="content-image"
              />
            </div>
          </article>

          <article className="method-item">
            <h3>{t('fertilizer.bandPlacement')}</h3>
            <p className="method-description">{t('fertilizer.bandPlacementDesc')}</p>
            <div className="method-pros"><strong>{t('fertilizer.advantages')}:</strong> {t('fertilizer.bandPlacementPros')}</div>
            <div className="method-cons"><strong>{t('fertilizer.limitations')}:</strong> {t('fertilizer.bandPlacementCons')}</div>
            <p className="method-best"><strong>{t('fertilizer.bestFor')}:</strong> {t('fertilizer.bandPlacementBest')}</p>
            <div className="image-container">
              <LocalImage
                src={getImageUrl("band-placement")}
                alt="Band Placement"
                className="content-image"
              />
            </div>
          </article>

          <article className="method-item">
            <h3>{t('fertilizer.fertigation')}</h3>
            <p className="method-description">{t('fertilizer.fertigationDesc')}</p>
            <div className="method-pros"><strong>{t('fertilizer.advantages')}:</strong> {t('fertilizer.fertigationPros')}</div>
            <div className="method-cons"><strong>{t('fertilizer.limitations')}:</strong> {t('fertilizer.fertigationCons')}</div>
            <p className="method-best"><strong>{t('fertilizer.bestFor')}:</strong> {t('fertilizer.fertigationBest')}</p>
            <div className="image-container">
              <LocalImage
                src={getImageUrl("fertigation-method")}
                alt="Fertigation Method"
                className="content-image"
              />
            </div>
          </article>

          <article className="method-item">
            <h3>{t('fertilizer.foliarSpray')}</h3>
            <p className="method-description">{t('fertilizer.foliarSprayDesc')}</p>
            <div className="method-pros"><strong>{t('fertilizer.advantages')}:</strong> {t('fertilizer.foliarSprayPros')}</div>
            <div className="method-cons"><strong>{t('fertilizer.limitations')}:</strong> {t('fertilizer.foliarSprayCons')}</div>
            <p className="method-best"><strong>{t('fertilizer.bestFor')}:</strong> {t('fertilizer.foliarSprayBest')}</p>
            <div className="image-container">
              <LocalImage
                src={getImageUrl("foliar-spray")}
                alt="Foliar Spray"
                className="content-image"
              />
            </div>
          </article>

          <article className="method-item">
            <h3>{t('fertilizer.deepPlacement')}</h3>
            <p className="method-description">{t('fertilizer.deepPlacementDesc')}</p>
            <div className="method-pros"><strong>{t('fertilizer.advantages')}:</strong> {t('fertilizer.deepPlacementPros')}</div>
            <div className="method-cons"><strong>{t('fertilizer.limitations')}:</strong> {t('fertilizer.deepPlacementCons')}</div>
            <p className="method-best"><strong>{t('fertilizer.bestFor')}:</strong> {t('fertilizer.deepPlacementBest')}</p>
            <div className="image-container">
              <LocalImage
                src={getImageUrl("fertilizer-application")}
                alt="Deep Placement"
                className="content-image"
              />
            </div>
          </article>
        </div>

        {/* Timing guidelines below */}
        <section className="card timing-card" style={{ marginTop: "1.5rem" }}>
          <header>
            <span className="badge">{t('fertilizer.timing')}</span>
            <h2>{t('fertilizer.whenToApply')}</h2>
            <p className="section-description">
              {t('fertilizer.timingDesc')}
            </p>
          </header>
          <div className="timing-grid">
            <article className="timing-item">
              <h3>{t('fertilizer.presowing')}</h3>
              <p><strong>{t('fertilizer.nutrients')}:</strong> {t('fertilizer.presowingNutrients')}</p>
              <p><strong>{t('fertilizer.timing')}:</strong> {t('fertilizer.presowingTiming')}</p>
              <p><strong>{t('fertilizer.reason')}:</strong> {t('fertilizer.presowingReason')}</p>
              <div className="image-container">
                <LocalImage
                  src={getImageUrl("soil-health")}
                  alt="Soil Health"
                  className="content-image"
                />
              </div>
            </article>

            <article className="timing-item">
              <h3>{t('fertilizer.atSowing')}</h3>
              <p><strong>{t('fertilizer.nutrients')}:</strong> {t('fertilizer.atSowingNutrients')}</p>
              <p><strong>{t('fertilizer.timing')}:</strong> {t('fertilizer.atSowingTiming')}</p>
              <p><strong>{t('fertilizer.reason')}:</strong> {t('fertilizer.atSowingReason')}</p>
              <div className="image-container">
                <LocalImage
                  src={getImageUrl("soil-health")}
                  alt="Sowing Application"
                  className="content-image"
                />
              </div>
            </article>

            <article className="timing-item">
              <h3>{t('fertilizer.vegetative')}</h3>
              <p><strong>{t('fertilizer.nutrients')}:</strong> {t('fertilizer.vegetativeNutrients')}</p>
              <p><strong>{t('fertilizer.timing')}:</strong> {t('fertilizer.vegetativeTiming')}</p>
              <p><strong>{t('fertilizer.reason')}:</strong> {t('fertilizer.vegetativeReason')}</p>
              <div className="image-container">
                <LocalImage
                  src={getImageUrl("nutrient-management")}
                  alt="Vegetative Stage"
                  className="content-image"
                />
              </div>
            </article>

            <article className="timing-item">
              <h3>{t('fertilizer.flowering')}</h3>
              <p><strong>{t('fertilizer.nutrients')}:</strong> {t('fertilizer.floweringNutrients')}</p>
              <p><strong>{t('fertilizer.timing')}:</strong> {t('fertilizer.floweringTiming')}</p>
              <p><strong>{t('fertilizer.reason')}:</strong> {t('fertilizer.floweringReason')}</p>
              <div className="image-container">
                <LocalImage
                  src={getImageUrl("nutrient-management")}
                  alt="Flowering Stage"
                  className="content-image"
                />
              </div>
            </article>

            <article className="timing-item">
              <h3>{t('fertilizer.fruiting')}</h3>
              <p><strong>{t('fertilizer.nutrients')}:</strong> {t('fertilizer.fruitingNutrients')}</p>
              <p><strong>{t('fertilizer.timing')}:</strong> {t('fertilizer.fruitingTiming')}</p>
              <p><strong>{t('fertilizer.reason')}:</strong> {t('fertilizer.fruitingReason')}</p>
              <div className="image-container">
                <LocalImage
                  src={getImageUrl("nutrient-management")}
                  alt="Fruit/Grain Filling"
                  className="content-image"
                />
              </div>
            </article>
          </div>
        </section>
      </section>
    </div>
  );

  /* ---------- Best Practices & Safety ---------- */
  const renderPracticesSafety = () => (
    <div className="tab-content">
      <section className="card practice-card">
        <header>
          <span className="badge">{t('fertilizer.bestPractices')}</span>
          <h2>{t('fertilizer.playbook')}</h2>
          <p className="section-description">
            {t('fertilizer.playbookDesc')}
          </p>
        </header>
        <ul className="practice-list">
          <li>{t('fertilizer.bp1')}</li>
          <li>{t('fertilizer.bp2')}</li>
          <li>{t('fertilizer.bp3')}</li>
          <li>{t('fertilizer.bp4')}</li>
          <li>{t('fertilizer.bp5')}</li>
          <li>{t('fertilizer.bp6')}</li>
          <li>{t('fertilizer.bp7')}</li>
          <li>{t('fertilizer.bp8')}</li>
          <li>{t('fertilizer.bp9')}</li>
          <li>{t('fertilizer.bp10')}</li>
        </ul>
      </section>

      <section className="card safety-card">
        <header>
          <span className="badge">{t('fertilizer.safetyStorage')}</span>
          <h2>{t('fertilizer.safeHandling')}</h2>
          <p className="section-description">
            {t('fertilizer.safetyDesc')}
          </p>
        </header>

        <ul className="safety-list">
          <li>{t('fertilizer.safe1')}</li>
          <li>{t('fertilizer.safe2')}</li>
          <li>{t('fertilizer.safe3')}</li>
          <li>{t('fertilizer.safe4')}</li>
          <li>{t('fertilizer.safe5')}</li>
          <li>{t('fertilizer.safe6')}</li>
          <li>{t('fertilizer.safe7')}</li>
          <li>{t('fertilizer.safe8')}</li>
          <li>{t('fertilizer.safe9')}</li>
          <li>{t('fertilizer.safe10')}</li>
        </ul>

        <div className="image-container">
          <LocalImage
            src={getImageUrl("safe-handling")}
            alt="Safe Handling of Fertilizers"
            className="content-image"
          />
        </div>
      </section>
    </div>
  );

  /* ---------- Dosage Calculator (static guidance) ---------- */
  const renderDosage = () => (
    <div className="tab-content">
      <section className="card dosage-card">
        <header>
          <span className="badge">{t('fertilizer.dosageCalc')}</span>
          <h2>{t('fertilizer.howToCalc')}</h2>
          <p className="section-description">
            {t('fertilizer.calcDesc')}
          </p>
        </header>

        <div className="dosage-content">
          <div className="dosage-formula">
            <h3>{t('fertilizer.formula')}</h3>
            <p><strong>{t('fertilizer.formulaText')}</strong></p>
          </div>
          <div className="dosage-example">
            <h3>{t('fertilizer.example')}</h3>
            <p>{t('fertilizer.exampleText1')}</p>
            <p><strong>{t('fertilizer.exampleText2')}</strong></p>
          </div>
          <div className="dosage-tips">
            <h3>{t('fertilizer.importantTips')}</h3>
            <ul>
              <li>{t('fertilizer.tip1')}</li>
              <li>{t('fertilizer.tip2')}</li>
              <li>{t('fertilizer.tip3')}</li>
              <li>{t('fertilizer.tip4')}</li>
              <li>{t('fertilizer.tip5')}</li>
              <li>{t('fertilizer.tip6')}</li>
            </ul>
          </div>
        </div>
      </section>
    </div>
  );

  return (
    <div className="fertilizer-guide">
      <div className="container">
        <div className="section-heading">
          <h1>{t('fertilizer.mainPageTitle')}</h1>
          <p className="section-subtitle">
            {t('fertilizer.mainPageSubtitle')}
          </p>
        </div>

        <div className="tabs-container">
          <div className="tabs">
            <TabButton id="overview" label={t('fertilizer.overview')} />
            <TabButton id="macros" label={t('fertilizer.macronutrients')} />
            <TabButton id="sec_micro" label={t('fertilizer.secondaryMicronutrients')} />
            <TabButton id="bio" label={t('fertilizer.biofertilizers')} />
            <TabButton id="organic" label={t('fertilizer.organicFertilizers')} />
            <TabButton id="application" label={t('fertilizer.applicationTiming')} />
            <TabButton id="practices" label={t('fertilizer.practicesSafety')} />
            <TabButton id="dosage" label={t('fertilizer.dosageCalculator')} />
          </div>

          <div className="tab-content-container">
            {activeTab === "overview" && renderOverview()}
            {activeTab === "macros" && renderMacronutrients()}
            {activeTab === "sec_micro" && renderSecondaryMicro()}
            {activeTab === "bio" && renderBiofertilizers()}
            {activeTab === "organic" && renderOrganic()}
            {activeTab === "application" && renderApplicationTiming()}
            {activeTab === "practices" && renderPracticesSafety()}
            {activeTab === "dosage" && renderDosage()}
          </div>
        </div>

        <div className="success-message">
          <p>{t('fertilizer.successMsg')}</p>
        </div>
      </div>
    </div>
  );
};

export default FertilizerGuide;
