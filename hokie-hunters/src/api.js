import axios from 'axios'

// Create Axios instance for general use (login/signup)
const api = axios.create({
  baseURL: 'http://localhost:5000',
  withCredentials: true, // enable cookies/sessions
})

// Export this for `import api from '../api'`
export default api

// Existing CRUD exports
export const fetchData = async (entity) => {
  const res = await api.get(`/${entity}`)
  return res.data
}

export const createItem = async (entity, data) => {
  const res = await api.post(`/${entity}`, data)
  return res.data
}

export const updateItem = async (entity, id, data) => {
  const res = await api.put(`/${entity}/${id}`, data)
  return res.data
}

export const deleteItem = async (entity, id) => {
  const res = await api.delete(`/${entity}/${id}`)
  return res.data
}
