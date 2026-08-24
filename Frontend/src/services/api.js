import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api',
  timeout: 20000,
  headers: {
    'Content-Type': 'application/json'
  }
});

export const classifyTicket = async (ticketText) => {
  try {
    const response = await api.post('/classify/', { ticket_text: ticketText });
    return response.data;
  } catch (error) {
    if (error.response?.data) {
      throw error;
    }
    throw error;
  }
};

export const getTicketHistory = async (search = '') => {
  const response = await api.get('/history/', {
    params: { search }
  });
  return response.data;
};
