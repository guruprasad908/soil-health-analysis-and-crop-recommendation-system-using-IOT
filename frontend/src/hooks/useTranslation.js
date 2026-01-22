import { useContext } from 'react';
import { LanguageContext } from '../contexts/LanguageContext';
import { en, kn } from '../utils/translations';

const translations = {
  en,
  kn
};

export const useTranslation = () => {
  const { language } = useContext(LanguageContext);
  
  const t = (key) => {
    return translations[language]?.[key] || translations['en'][key] || key;
  };
  
  return { t, language };
};