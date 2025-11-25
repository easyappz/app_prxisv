import instance from './axios';
import { getToken } from '../utils/auth';

/**
 * Register a new user
 * @param {string} username - Username for the new account
 * @param {string} password - Password for the new account
 * @returns {Promise} - Returns token and user data
 */
export const register = async (username, password) => {
  const response = await instance.post('/api/auth/register/', {
    username,
    password,
  });
  return response.data;
};

/**
 * Login user with credentials
 * @param {string} username - Username
 * @param {string} password - Password
 * @returns {Promise} - Returns token and user data
 */
export const login = async (username, password) => {
  const response = await instance.post('/api/auth/login/', {
    username,
    password,
  });
  return response.data;
};

/**
 * Get current authenticated user information
 * @returns {Promise} - Returns current user data
 */
export const getCurrentUser = async () => {
  const token = getToken();
  const response = await instance.get('/api/auth/me/', {
    headers: {
      Authorization: `Token ${token}`,
    },
  });
  return response.data;
};
