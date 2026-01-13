import { useState } from 'react';

interface ShareHelpersProps {
    title: string;
    text: string;
    url?: string;
    imageUrl?: string;
}

/**
 * Hook para compartir contenido usando Web Share API nativa
 * con fallback a URLs específicas por plataforma
 */
export function useShare() {
    const [isSharing, setIsSharing] = useState(false);

    /**
     * Web Share API (Nativa del navegador)
     * Funciona en móvil y desktop moderno
     */
    const shareNative = async ({ title, text, url }: ShareHelpersProps) => {
        if (!navigator.share) {
            return false; // Browser no soporta, usar fallback
        }

        try {
            setIsSharing(true);
            await navigator.share({
                title,
                text,
                url: url || window.location.href
            });
            return true;
        } catch (error) {
            if ((error as Error).name === 'AbortError') {
                // Usuario canceló, no es error
                return false;
            }
            console.error('Error sharing:', error);
            return false;
        } finally {
            setIsSharing(false);
        }
    };

    /**
     * Genera URLs de compartir por plataforma
     */
    const getShareUrls = ({ title, text, url, imageUrl }: ShareHelpersProps) => {
        const shareUrl = url || window.location.href;
        const encodedText = encodeURIComponent(text);
        const encodedTitle = encodeURIComponent(title);
        const encodedUrl = encodeURIComponent(shareUrl);
        const encodedImage = imageUrl ? encodeURIComponent(imageUrl) : '';

        return {
            facebook: `https://www.facebook.com/sharer/sharer.php?u=${encodedUrl}`,

            twitter: `https://twitter.com/intent/tweet?text=${encodedText}&url=${encodedUrl}`,

            linkedin: `https://www.linkedin.com/sharing/share-offsite/?url=${encodedUrl}`,

            whatsapp: `https://api.whatsapp.com/send?text=${encodedText}%20${encodedUrl}`,

            telegram: `https://t.me/share/url?url=${encodedUrl}&text=${encodedText}`,

            pinterest: imageUrl
                ? `https://pinterest.com/pin/create/button/?url=${encodedUrl}&media=${encodedImage}&description=${encodedText}`
                : null,

            reddit: `https://reddit.com/submit?url=${encodedUrl}&title=${encodedTitle}`,

            // Email
            email: `mailto:?subject=${encodedTitle}&body=${encodedText}%0A%0A${encodedUrl}`,

            // SMS (móvil)
            sms: `sms:?body=${encodedText}%20${encodedUrl}`
        };
    };

    /**
     * Abre popup de compartir por plataforma
     */
    const shareViaPopup = (url: string, platform: string) => {
        const width = 600;
        const height = 600;
        const left = (window.innerWidth - width) / 2;
        const top = (window.innerHeight - height) / 2;

        const popup = window.open(
            url,
            `share-${platform}`,
            `width=${width},height=${height},left=${left},top=${top},toolbar=no,location=no,status=no,menubar=no,scrollbars=yes,resizable=yes`
        );

        if (popup) {
            popup.focus();
            return true;
        }
        return false;
    };

    /**
     * Copiar al portapapeles
     */
    const copyToClipboard = async (text: string) => {
        try {
            await navigator.clipboard.writeText(text);
            return true;
        } catch (error) {
            // Fallback para navegadores antiguos
            const textArea = document.createElement('textarea');
            textArea.value = text;
            textArea.style.position = 'fixed';
            textArea.style.opacity = '0';
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();

            try {
                document.execCommand('copy');
                document.body.removeChild(textArea);
                return true;
            } catch (err) {
                document.body.removeChild(textArea);
                return false;
            }
        }
    };

    return {
        shareNative,
        getShareUrls,
        shareViaPopup,
        copyToClipboard,
        isSharing,
        supportsNativeShare: !!navigator.share
    };
}

/**
 * URLs de descarga directa para apps móviles
 */
export const getAppDownloadUrls = () => ({
    facebook: {
        ios: 'https://apps.apple.com/app/facebook/id284882215',
        android: 'https://play.google.com/store/apps/details?id=com.facebook.katana'
    },
    instagram: {
        ios: 'https://apps.apple.com/app/instagram/id389801252',
        android: 'https://play.google.com/store/apps/details?id=com.instagram.android'
    },
    tiktok: {
        ios: 'https://apps.apple.com/app/tiktok/id835599320',
        android: 'https://play.google.com/store/apps/details?id=com.zhiliaoapp.musically'
    },
    whatsapp: {
        ios: 'https://apps.apple.com/app/whatsapp-messenger/id310633997',
        android: 'https://play.google.com/store/apps/details?id=com.whatsapp'
    },
    linkedin: {
        ios: 'https://apps.apple.com/app/linkedin/id288429040',
        android: 'https://play.google.com/store/apps/details?id=com.linkedin.android'
    }
});
