import axios from 'axios';
const BASE_URL = 'http://localhost:5000';

export async function createMessage(data) {
  const res = await axios.post(`${BASE_URL}/messages`, data);
  return res.data;
}