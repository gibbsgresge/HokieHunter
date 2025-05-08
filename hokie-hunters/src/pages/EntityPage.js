import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import {
  Container,
  Typography,
  CircularProgress,
  Paper,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Box,
  IconButton,
  TextField,
  Button,
  Grid
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';
import SaveIcon from '@mui/icons-material/Save';
import CancelIcon from '@mui/icons-material/Cancel';

function EntityPage() {
  const { entityName } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [editingRow, setEditingRow] = useState(null);
  const [editData, setEditData] = useState({});
  const [newEntry, setNewEntry] = useState({});
  const role = localStorage.getItem('role');

  const endpointMap = {
    property: 'property',
    leasetransfer: 'leasetransfer',
    review: 'review',
    favorite: 'favorite',
    roommatesearch: 'roommatesearch',
    commute: 'commute',
    movingservices: 'movingservices',
    safetyfeatures: 'safetyfeatures',
    amenities: 'amenities'
  };

  const idFieldMap = {
    property: 'PropertyID',
    leasetransfer: 'TransferID',
    review: 'ReviewID',
    favorite: 'FavoriteID',
    roommatesearch: 'StudentID',
    commute: 'CommuteID',
    movingservices: 'ServiceID',
    safetyfeatures: 'FeatureID',
    amenities: 'AmenityID'
  };

  const idField = idFieldMap[entityName];

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch(`http://localhost:5000/${endpointMap[entityName]}`);
      const json = await res.json();
      setData(json);
    } catch (err) {
      console.error('Error fetching data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    return () => {
      setEditingRow(null);
      setEditData({});
      setNewEntry({});
    };
  }, [entityName]);

  const handleDelete = async (id) => {
    try {
      await fetch(`http://localhost:5000/${endpointMap[entityName]}/${id}`, {
        method: 'DELETE'
      });
      fetchData();
    } catch (err) {
      console.error('Failed to delete entry:', err);
    }
  };

  const startEditing = (entry) => {
    setEditingRow(entry[idField]);
    setEditData({ ...entry });
  };

  const cancelEditing = () => {
    setEditingRow(null);
    setEditData({});
  };

  const handleSave = async () => {
    try {
      await fetch(`http://localhost:5000/${endpointMap[entityName]}/${editingRow}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(editData)
      });
      cancelEditing();
      fetchData();
    } catch (err) {
      console.error('Failed to update entry:', err);
    }
  };

  const handleCreate = async () => {
    try {
      await fetch(`http://localhost:5000/${endpointMap[entityName]}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newEntry)
      });
      setNewEntry({});
      fetchData();
    } catch (err) {
      console.error('Failed to create entry:', err);
    }
  };

  if (loading) return <CircularProgress sx={{ mt: 10 }} />;
  if (!data || data.length === 0) return <Typography>No data found.</Typography>;

  const headers = Object.keys(data[0]).filter((key) => {
    const lower = key.toLowerCase();
    return !(lower.includes('id') && !lower.includes('name') && !lower.includes('email'));
  });

  const isAmenity = entityName === 'amenities';

  return (
    <Container maxWidth="lg" sx={{ mt: 8 }}>
      <Typography variant="h4" sx={{ mb: 3, fontWeight: 600 }}>
        {entityName.charAt(0).toUpperCase() + entityName.slice(1)} Entries
      </Typography>
      <Paper elevation={3}>
        <Box sx={{ overflowX: 'auto' }}>
          <Table>
            <TableHead>
              <TableRow>
                {role === 'admin' && <TableCell />}
                {headers.map((header) => (
                  <TableCell key={header}>
                    {header.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}
                  </TableCell>
                ))}
                {role === 'admin' && <TableCell>Actions</TableCell>}
              </TableRow>
            </TableHead>
            <TableBody>
              {data.map((entry, idx) => (
                <TableRow key={idx}>
                  {role === 'admin' && (
                    <TableCell>
                      <IconButton onClick={() => handleDelete(entry[idField])} color="error">
                        <DeleteIcon />
                      </IconButton>
                    </TableCell>
                  )}
                  {headers.map((field) => (
                    <TableCell key={field}>
                      {editingRow === entry[idField] ? (
                        <TextField
                          value={editData[field] ?? ''}
                          onChange={(e) =>
                            setEditData({ ...editData, [field]: e.target.value })
                          }
                          variant="standard"
                          fullWidth
                        />
                      ) : (
                        entry[field]
                      )}
                    </TableCell>
                  ))}
                  {role === 'admin' && (
                    <TableCell>
                      {editingRow === entry[idField] ? (
                        <>
                          <IconButton onClick={handleSave} color="primary">
                            <SaveIcon />
                          </IconButton>
                          <IconButton onClick={cancelEditing} color="inherit">
                            <CancelIcon />
                          </IconButton>
                        </>
                      ) : (
                        <IconButton onClick={() => startEditing(entry)} color="primary">
                          <EditIcon />
                        </IconButton>
                      )}
                    </TableCell>
                  )}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Box>
      </Paper>
    </Container>
  );
}

export default EntityPage;
