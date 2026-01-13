import i18next from 'i18next';
import { initReactI18next } from 'react-i18next';

import esM from './es-MX.json';
import en from './en.json';

const resources = {
    'es-MX': { translation: esMX },
    'en': { translation: en }
};

i18next
    .use(initReactI18next)
    .init({
        resources,
        lng: 'es-MX', // Idioma por defecto
        fallbackLng: 'es-MX',
        interpolation: {
            escapeValue: false
        }
    });

export default i18next;
