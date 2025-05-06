import React, { useEffect, useState } from 'react';
import {
  Container,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Button,
  TextField,
  Box
} from '@mui/material';

function LandlordAccount() {
  const [properties, setProperties] = useState([]);
  const [newProperty, setNewProperty] = useState({
    Name: '',
    Location: '',
    Price: '',
    RoomType: ''
  });
  const [editingId, setEditingId] = useState(null);
  const [editedProperty, setEditedProperty] = useState({});
  const landlordId = localStorage.getItem('user_id');

  const fetchProperties = async () => {
    const res = await fetch(`http://localhost:5000/landlord/${landlordId}/properties`);
    const data = await res.json();
    setProperties(data);
  };

  useEffect(() => {
    fetchProperties();
  }, []);

  const handleDelete = async (id) => {
    await fetch(`http://localhost:5000/property/${id}`, { method: 'DELETE' });
    fetchProperties();
  };

  const handleAdd = async () => {
    const res = await fetch(`http://localhost:5000/property`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...newProperty, LandlordID: landlordId })
    });
    if (res.ok) {
      setNewProperty({ Name: '', Location: '', Price: '', RoomType: '' });
      fetchProperties();
    }
  };

  const handleEdit = (prop) => {
    setEditingId(prop.PropertyID);
    setEditedProperty({ ...prop });
  };

  const handleCancel = () => {
    setEditingId(null);
    setEditedProperty({});
  };

  const handleSave = async () => {
    const res = await fetch(`http://localhost:5000/property/${editingId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(editedProperty)
    });
    if (res.ok) {
      setEditingId(null);
      setEditedProperty({});
      fetchProperties();
    }
  };

  return (
    <Container sx={{ mt: 10 }}>
      <Typography variant="h4" gutterBottom>
        Your Properties
      </Typography>

      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Name</TableCell>
            <TableCell>Location</TableCell>
            <TableCell>Price</TableCell>
            <TableCell>Room Type</TableCell>
            <TableCell>Actions</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {properties.map((prop) => (
            <TableRow key={prop.PropertyID}>
              <TableCell>
                {editingId === prop.PropertyID ? (
                  <TextField
                    value={editedProperty.Name}
                    onChange={(e) =>
                      setEditedProperty({ ...editedProperty, Name: e.target.value })
                    }
                  />
                ) : (
                  prop.Name
                )}
              </TableCell>
              <TableCell>
                {editingId === prop.PropertyID ? (
                  <TextField
                    value={editedProperty.Location}
                    onChange={(e) =>
                      setEditedProperty({ ...editedProperty, Location: e.target.value })
                    }
                  />
                ) : (
                  prop.Location
                )}
              </TableCell>
              <TableCell>
                {editingId === prop.PropertyID ? (
                  <TextField
                    value={editedProperty.Price}
                    onChange={(e) =>
                      setEditedProperty({ ...editedProperty, Price: e.target.value })
                    }
                  />
                ) : (
                  prop.Price
                )}
              </TableCell>
              <TableCell>
                {editingId === prop.PropertyID ? (
                  <TextField
                    value={editedProperty.RoomType}
                    onChange={(e) =>
                      setEditedProperty({ ...editedProperty, RoomType: e.target.value })
                    }
                  />
                ) : (
                  prop.RoomType
                )}
              </TableCell>
              <TableCell>
                {editingId === prop.PropertyID ? (
                  <>
                    <Button color="primary" onClick={handleSave} sx={{ mr: 1 }}>
                      Save
                    </Button>
                    <Button onClick={handleCancel}>Cancel</Button>
                  </>
                ) : (
                  <>
                    <Button
                      sx={{ color: 'blue', mr: 1 }}
                      onClick={() => handleEdit(prop)}
                    >
                      Edit
                    </Button>
                    <Button color="error" onClick={() => handleDelete(prop.PropertyID)}>
                      Delete
                    </Button>
                  </>
                )}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>

      <Box mt={4}>
        <Typography variant="h6">Add New Property</Typography>
        <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', mt: 2 }}>
          <TextField
            label="Name"
            value={newProperty.Name}
            onChange={(e) => setNewProperty({ ...newProperty, Name: e.target.value })}
          />
          <TextField
            label="Location"
            value={newProperty.Location}
            onChange={(e) => setNewProperty({ ...newProperty, Location: e.target.value })}
          />
          <TextField
            label="Price"
            value={newProperty.Price}
            onChange={(e) => setNewProperty({ ...newProperty, Price: e.target.value })}
          />
          <TextField
            label="Room Type"
            value={newProperty.RoomType}
            onChange={(e) => setNewProperty({ ...newProperty, RoomType: e.target.value })}
          />
          <Button variant="contained" onClick={handleAdd}>
            Add
          </Button>
        </Box>
      </Box>
    </Container>
  );
}

export default LandlordAccount;
