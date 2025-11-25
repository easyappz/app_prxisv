import instance from './axios';
import { getToken } from '../utils/auth';

/**
 * Get all chat messages
 * @returns {Promise} - Returns array of messages
 */
export const getMessages = async () => {
  const token = getToken();
  const response = await instance.get('/api/messages/', {
    headers: {
      Authorization: `Token ${token}`,
    },
  });
  return response.data;
};

/**
 * Send a new chat message
 * @param {string} text - Message text content
 * @returns {Promise} - Returns created message data
 */
export const sendMessage = async (text) => {
  const token = getToken();
  const response = await instance.post(
    '/api/messages/',
    { text },
    {
      headers: {
        Authorization: `Token ${token}`,
      },
    }
  );
  return response.data;
};
