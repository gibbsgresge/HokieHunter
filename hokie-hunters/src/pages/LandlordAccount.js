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
  Box,
  MenuItem
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
  const [safetyFeatures, setSafetyFeatures] = useState([]);
  const [newSafety, setNewSafety] = useState({ PropertyID: '', FeatureDescription: '' });
  const [editingSafety, setEditingSafety] = useState(null);
  const [commutes, setCommutes] = useState([]);
  const [newCommute, setNewCommute] = useState({ PropertyID: '', Time: '', Distance: '' });
  const [editingCommute, setEditingCommute] = useState(null);
  const [movingServices, setMovingServices] = useState([]);
  const [newService, setNewService] = useState({ PropertyID: '', CompanyName: '', ContactInfo: '' });
  const [editingService, setEditingService] = useState(null);
  const [amenities, setAmenities] = useState([]);
  const [newAmenity, setNewAmenity] = useState({ PropertyID: '', Type: '' });
  const [editingAmenity, setEditingAmenity] = useState(null);

  const landlordId = localStorage.getItem('user_id');

  const fetchProperties = async () => {
    const res = await fetch(`http://localhost:5000/landlord/${landlordId}/properties`);
    const data = await res.json();
    setProperties(data);
  };

  const fetchRelated = async () => {
    const [sf, cm, ms, am] = await Promise.all([
      fetch(`http://localhost:5000/landlord/${landlordId}/safetyfeatures`).then(r => r.json()),
      fetch(`http://localhost:5000/landlord/${landlordId}/commute`).then(r => r.json()),
      fetch(`http://localhost:5000/landlord/${landlordId}/movingservices`).then(r => r.json()),
      fetch(`http://localhost:5000/landlord/${landlordId}/amenities`).then(r => r.json())
    ]);
    setSafetyFeatures(sf);
    setCommutes(cm);
    setMovingServices(ms);
    setAmenities(am);
  };

  useEffect(() => {
    fetchProperties();
    fetchRelated();
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

  const crudSection = (title, items, setItems, newItem, setNewItem, editingItem, setEditingItem, fields, endpoint, idField) => (
    <Box mt={6}>
      <Typography variant="h6">{title}</Typography>
      <Table>
        <TableHead>
          <TableRow>
            {fields.map(f => <TableCell key={f.key}>{f.label}</TableCell>)}
            <TableCell>Actions</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {items
            .filter(i => properties.some(p => p.PropertyID === i.PropertyID))
            .map((item) => (
              <TableRow key={item[idField]}>
                {fields.map(f => (
                  <TableCell key={f.key}>
                    {editingItem === item[idField] ? (
                      <TextField
                        value={item[f.key]}
                        onChange={(e) => {
                          const updated = items.map(i => i[idField] === item[idField] ? { ...i, [f.key]: e.target.value } : i);
                          setItems(updated);
                        }}
                      />
                    ) : item[f.key]}
                  </TableCell>
                ))}
                <TableCell>
                  {editingItem === item[idField] ? (
                    <>
                      <Button onClick={async () => {
                        await fetch(`http://localhost:5000/${endpoint}/${item[idField]}`, {
                          method: 'PUT',
                          headers: { 'Content-Type': 'application/json' },
                          body: JSON.stringify(item)
                        });
                        setEditingItem(null);
                        fetchRelated();
                      }}>Save</Button>
                      <Button onClick={() => setEditingItem(null)}>Cancel</Button>
                    </>
                  ) : (
                    <>
                      <Button onClick={() => setEditingItem(item[idField])}>Edit</Button>
                      <Button color="error" onClick={async () => {
                        await fetch(`http://localhost:5000/${endpoint}/${item[idField]}`, { method: 'DELETE' });
                        fetchRelated();
                      }}>Delete</Button>
                    </>
                  )}
                </TableCell>
              </TableRow>
            ))}
          <TableRow>
            {fields.map(f => (
              <TableCell key={f.key}>
                {f.key === 'PropertyID' ? (
                  <TextField select value={newItem[f.key]} onChange={(e) => setNewItem({ ...newItem, [f.key]: e.target.value })}>
                    {properties.map(p => <MenuItem key={p.PropertyID} value={p.PropertyID}>{p.Name}</MenuItem>)}
                  </TextField>
                ) : (
                  <TextField value={newItem[f.key]} onChange={(e) => setNewItem({ ...newItem, [f.key]: e.target.value })} />
                )}
              </TableCell>
            ))}
            <TableCell>
              <Button onClick={async () => {
                await fetch(`http://localhost:5000/${endpoint}`, {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify(newItem)
                });
                setNewItem(fields.reduce((acc, cur) => ({ ...acc, [cur.key]: '' }), {}));
                fetchRelated();
              }}>Add</Button>
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </Box>
  );

  return (
    <Container sx={{ mt: 10 }}>
      <Typography variant="h4" gutterBottom>Your Properties</Typography>
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
              <TableCell>{editingId === prop.PropertyID ? <TextField value={editedProperty.Name} onChange={(e) => setEditedProperty({ ...editedProperty, Name: e.target.value })} /> : prop.Name}</TableCell>
              <TableCell>{editingId === prop.PropertyID ? <TextField value={editedProperty.Location} onChange={(e) => setEditedProperty({ ...editedProperty, Location: e.target.value })} /> : prop.Location}</TableCell>
              <TableCell>{editingId === prop.PropertyID ? <TextField value={editedProperty.Price} onChange={(e) => setEditedProperty({ ...editedProperty, Price: e.target.value })} /> : prop.Price}</TableCell>
              <TableCell>{editingId === prop.PropertyID ? <TextField value={editedProperty.RoomType} onChange={(e) => setEditedProperty({ ...editedProperty, RoomType: e.target.value })} /> : prop.RoomType}</TableCell>
              <TableCell>
                {editingId === prop.PropertyID ? (
                  <>
                    <Button onClick={handleSave}>Save</Button>
                    <Button onClick={handleCancel}>Cancel</Button>
                  </>
                ) : (
                  <>
                    <Button onClick={() => handleEdit(prop)}>Edit</Button>
                    <Button color="error" onClick={() => handleDelete(prop.PropertyID)}>Delete</Button>
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
          <TextField label="Name" value={newProperty.Name} onChange={(e) => setNewProperty({ ...newProperty, Name: e.target.value })} />
          <TextField label="Location" value={newProperty.Location} onChange={(e) => setNewProperty({ ...newProperty, Location: e.target.value })} />
          <TextField label="Price" value={newProperty.Price} onChange={(e) => setNewProperty({ ...newProperty, Price: e.target.value })} />
          <TextField label="Room Type" value={newProperty.RoomType} onChange={(e) => setNewProperty({ ...newProperty, RoomType: e.target.value })} />
          <Button variant="contained" onClick={handleAdd}>Add</Button>
        </Box>
      </Box>

      {crudSection("Safety Features", safetyFeatures, setSafetyFeatures, newSafety, setNewSafety, editingSafety, setEditingSafety,
        [{ key: 'PropertyID', label: 'Property' }, { key: 'FeatureDescription', label: 'Description' }],
        'safetyfeatures', 'FeatureID')}

      {crudSection("Commute Info", commutes, setCommutes, newCommute, setNewCommute, editingCommute, setEditingCommute,
        [{ key: 'PropertyID', label: 'Property' }, { key: 'Time', label: 'Time (min)' }, { key: 'Distance', label: 'Distance (mi)' }],
        'commute', 'CommuteID')}

      {crudSection("Moving Services", movingServices, setMovingServices, newService, setNewService, editingService, setEditingService,
        [{ key: 'PropertyID', label: 'Property' }, { key: 'CompanyName', label: 'Company' }, { key: 'ContactInfo', label: 'Contact Info' }],
        'movingservices', 'ServiceID')}

      {crudSection("Amenities", amenities, setAmenities, newAmenity, setNewAmenity, editingAmenity, setEditingAmenity,
        [{ key: 'PropertyID', label: 'Property' }, { key: 'Type', label: 'Amenity Type' }],
        'amenities', 'AmenityID')}
    </Container>
  );
}

export default LandlordAccount;
