import i18next from 'i18next';
import { initReactI18next } from 'react-i18next';

import esMX from './es-MX.json';
import en from './en.json';

const resources = {
    'es-MX': { translation: esMX },
    'en': { translation: en }
};

i18next
    .use(initReactI18next)
    .init({
        resources,
        lng: 'es-MX', // idioma por defecto
        fallbackLng: 'en',
        interpolation: {
            escapeValue: false
        }
    });

export default i18next;
