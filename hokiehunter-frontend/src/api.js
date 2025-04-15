// src/api.js
import axios from 'axios'

const API = axios.create({
  baseURL: 'http://localhost:5000' // or your server
})

// GET all
export const fetchData = async (entity) => {
  // e.g. entity = "users" => GET /users
  const res = await API.get(`/${entity}`)
  return res.data
}

// CREATE
export const createItem = async (entity, payload) => {
  const res = await API.post(`/${entity}`, payload)
  return res.data
}

// UPDATE
export const updateItem = async (entity, id, payload) => {
  const res = await API.put(`/${entity}/${id}`, payload)
  return res.data
}

// DELETE
export const deleteItem = async (entity, id) => {
  const res = await API.delete(`/${entity}/${id}`)
  return res.data
}
