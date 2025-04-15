import axios from 'axios';
const BASE_URL = 'http://localhost:5000';

export async function createCommute(data) {
  const res = await axios.post(`${BASE_URL}/commute`, data);
  return res.data;
}