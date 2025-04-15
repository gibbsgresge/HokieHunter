import axios from 'axios';
const BASE_URL = 'http://localhost:5000';

export async function getProperties() {
  const res = await axios.get(`${BASE_URL}/properties`);
  return res.data;
}

export async function getProperty(id) {
  const res = await axios.get(`${BASE_URL}/properties/${id}`);
  return res.data;
}

export async function createProperty(data) {
  const res = await axios.post(`${BASE_URL}/properties`, data);
  return res.data;
}

export async function updateProperty(id, data) {
  const res = await axios.put(`${BASE_URL}/properties/${id}`, data);
  return res.data;
}

export async function deleteProperty(id) {
  const res = await axios.delete(`${BASE_URL}/properties/${id}`);
  return res.data;
}
