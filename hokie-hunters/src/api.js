import axios from 'axios'


const api = axios.create({
  baseURL: 'http://localhost:5000',
  withCredentials: true, 
})


export default api


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
