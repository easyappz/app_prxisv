/**
 * Utility functions for managing authentication tokens in localStorage
 */

const TOKEN_KEY = 'authToken';

/**
 * Save authentication token to localStorage
 * @param {string} token - The authentication token to save
 */
export const saveToken = (token) => {
  if (token) {
    localStorage.setItem(TOKEN_KEY, token);
  }
};

/**
 * Get authentication token from localStorage
 * @returns {string|null} - The stored token or null if not found
 */
export const getToken = () => {
  return localStorage.getItem(TOKEN_KEY);
};

/**
 * Remove authentication token from localStorage
 */
export const removeToken = () => {
  localStorage.removeItem(TOKEN_KEY);
};
