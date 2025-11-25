import instance from './axios.js';
import { getToken } from '../utils/auth.js';

/**
 * Get all chat messages
 * @returns {Promise} - Promise with messages array
 */
export const getMessages = async () => {
  const token = getToken();
  
  const response = await instance.get('/api/messages/', {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  
  return response.data;
};

/**
 * Send a new message to chat
 * @param {string} text - Message text content
 * @returns {Promise} - Promise with created message object
 */
export const sendMessage = async (text) => {
  const token = getToken();
  
  const response = await instance.post(
    '/api/messages/',
    { text },
    {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    }
  );
  
  return response.data;
};
