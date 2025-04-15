import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { Typography, Button, Grid } from '@mui/material'
import { fetchData, createItem, updateItem, deleteItem } from '../api'
import { entityConfig } from '../entityConfig'
import DataCard from '../components/DataCard'
import CrudDialog from '../components/CrudDialog'

function EntityPage() {
  const { entity } = useParams()
  const config = entityConfig[entity] || {}
  const { fields = [], idKey = 'id' } = config

  const [items, setItems] = useState([])
  const [dialogOpen, setDialogOpen] = useState(false)
  const [dialogMode, setDialogMode] = useState('create') // 'create' or 'update'
  const [selectedItem, setSelectedItem] = useState(null)

  // Fetch entity data on load or when entity changes
  useEffect(() => {
    if (entity) loadItems()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [entity])

  const loadItems = async () => {
    try {
      const data = await fetchData(entity)
      setItems(data)
    } catch (error) {
      console.error('Failed to fetch', error)
    }
  }

  const handleCreate = () => {
    setDialogMode('create')
    const emptyItem = fields.reduce((acc, field) => ({ ...acc, [field]: '' }), {})
    setSelectedItem(emptyItem)
    setDialogOpen(true)
  }

  const handleEdit = (item) => {
    setDialogMode('update')
    setSelectedItem(item)
    setDialogOpen(true)
  }

  const handleDelete = async (item) => {
    if (!window.confirm(`Delete this ${entity} entry?`)) return
    try {
      await deleteItem(entity, item[idKey])
      loadItems()
    } catch (error) {
      console.error('Delete failed:', error)
    }
  }

  const handleDialogSubmit = async (formData) => {
    try {
      if (dialogMode === 'create') {
        await createItem(entity, formData)
      } else {
        await updateItem(entity, formData[idKey], formData)
      }
      setDialogOpen(false)
      loadItems()
    } catch (error) {
      console.error('Save failed:', error)
    }
  }

  return (
    <div>
      <Typography variant="h5" gutterBottom sx={{ textTransform: 'capitalize' }}>
        {entity}
      </Typography>

      <Button
        variant="contained"
        color="primary"
        onClick={handleCreate}
        sx={{ mb: 3 }}
      >
        Insert {entity}
      </Button>

      <Grid container spacing={3}>
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
