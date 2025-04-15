// src/pages/EntityPage.js
import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { Typography, Button, Grid } from '@mui/material'
import { fetchData, createItem, updateItem, deleteItem } from '../api'
import { entityConfig } from '../entityConfig'
import DataCard from '../components/DataCard'
import CrudDialog from '../components/CrudDialog'

function EntityPage() {
  const { entity } = useParams()             // e.g. "users" or "properties"
  const config = entityConfig[entity] || {}  // fields, idKey
  const { fields = [], idKey = 'id' } = config

  const [items, setItems] = useState([])
  const [dialogOpen, setDialogOpen] = useState(false)
  const [dialogMode, setDialogMode] = useState('create') // or 'update'
  const [selectedItem, setSelectedItem] = useState(null)

  useEffect(() => {
    if (config) loadItems()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [entity]) // refetch if entity changes

  const loadItems = async () => {
    const data = await fetchData(entity)
    setItems(data)
  }

  const handleCreate = () => {
    setDialogMode('create')
    // create an object with empty strings for each field
    const emptyObj = fields.reduce((acc, f) => ({ ...acc, [f]: '' }), {})
    setSelectedItem(emptyObj)
    setDialogOpen(true)
  }

  const handleEdit = (item) => {
    setDialogMode('update')
    setSelectedItem({ ...item }) // shallow copy
    setDialogOpen(true)
  }

  const handleDelete = async (item) => {
    if (!window.confirm(`Are you sure you want to delete this ${entity}?`)) return
    await deleteItem(entity, item[idKey])
    loadItems()
  }

  const handleDialogSubmit = async (formData) => {
    if (dialogMode === 'create') {
      await createItem(entity, formData)
    } else {
      await updateItem(entity, formData[idKey], formData)
    }
    loadItems()
    setDialogOpen(false)
  }

  return (
    <div>
      <Typography variant="h5" gutterBottom textTransform="capitalize">
        {entity}
      </Typography>
      <Button variant="contained" onClick={handleCreate} sx={{ mb: 2 }}>
        Insert {entity}
      </Button>

      <Grid container spacing={2}>
        {items.map((item) => (
          <Grid item xs={12} sm={6} md={4} key={item[idKey]}>
            <DataCard
              itemData={item}
              onEdit={() => handleEdit(item)}
              onDelete={() => handleDelete(item)}
            />
          </Grid>
        ))}
      </Grid>

      <CrudDialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        mode={dialogMode}
        data={selectedItem}
        onSubmit={handleDialogSubmit}
        fields={fields}
      />
    </div>
  )
}

export default EntityPage
