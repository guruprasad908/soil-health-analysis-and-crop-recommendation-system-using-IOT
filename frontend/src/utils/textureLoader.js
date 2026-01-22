// textureLoader.js
// Helper functions for loading and managing crop textures

/**
 * Sanitize crop name to create a valid filename
 * @param {string} cropName - The crop name to sanitize
 * @returns {string} - Sanitized filename without extension
 */
export const sanitizeCropName = (cropName) => {
  if (!cropName) return 'default_crop';
  return cropName
    .toLowerCase()
    .replace(/\s+/g, '_')
    .replace(/[^a-z0-9_]/g, '');
};

/**
 * Check if a texture file exists
 * @param {string} filename - The filename to check
 * @returns {Promise<boolean>} - True if file exists, false otherwise
 */
export const textureExists = async (filename) => {
  try {
    const response = await fetch(`./src/assets/textures/${filename}.png`);
    return response.ok;
  } catch (error) {
    return false;
  }
};

/**
 * Get the texture path for a crop
 * @param {string} cropName - The crop name
 * @returns {Promise<string>} - Path to the texture file
 */
export const getCropTexturePath = async (cropName) => {
  const sanitized = sanitizeCropName(cropName);
  const defaultPath = './src/assets/textures/default_crop.png';
  
  // Try the sanitized crop name first
  try {
    const cropPath = `./src/assets/textures/${sanitized}.png`;
    const response = await fetch(cropPath);
    if (response.ok) {
      return cropPath;
    }
  } catch (error) {
    // Continue to default
  }
  
  // Return default if crop-specific texture doesn't exist
  return defaultPath;
};

/**
 * Preload an image and return a Promise
 * @param {string} src - Image source URL
 * @returns {Promise<HTMLImageElement>} - Loaded image element
 */
export const preloadImage = (src) => {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = reject;
    img.src = src;
  });
};