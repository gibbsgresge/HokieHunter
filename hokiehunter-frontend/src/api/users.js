import axios from 'axios';
const BASE_URL = 'http://localhost:5000';

export async function getUsers() {
  const res = await axios.get(`${BASE_URL}/users`);
  return res.data;
}

export async function getUser(id) {
  const res = await axios.get(`${BASE_URL}/users/${id}`);
  return res.data;
}

export async function createUser(data) {
  const res = await axios.post(`${BASE_URL}/users`, data);
  return res.data;
}

export async function updateUser(id, data) {
  const res = await axios.put(`${BASE_URL}/users/${id}`, data);
  return res.data;
}

export async function deleteUser(id) {
  const res = await axios.delete(`${BASE_URL}/users/${id}`);
  return res.data;
}
