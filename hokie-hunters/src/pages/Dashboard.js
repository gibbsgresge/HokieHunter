import React, { useEffect, useState } from 'react';
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  ResponsiveContainer
} from 'recharts';

const COLORS = ['#8884d8', '#82ca9d', '#ffc658', '#ff8042', '#8dd1e1', '#a4de6c', '#d0ed57'];

const Dashboard = () => {
  const [summary, setSummary] = useState(null);
  const [landlords, setLandlords] = useState([]);
  const [students, setStudents] = useState({ by_major: [], by_graduation_year: [] });

  useEffect(() => {
    fetch('/summary').then(res => res.json()).then(setSummary);
    fetch('/landlord-stats').then(res => res.json()).then(setLandlords);
    fetch('/student-stats').then(res => res.json()).then(setStudents);
  }, []);

  const roleData = summary
    ? [
        { name: 'Students', value: summary[" Students"] },
        { name: 'Landlords', value: summary[" Landlords"] },
        { name: 'Admins', value: summary[" Admins"] }
      ]
    : [];

  return (
    <div style={{ padding: '2rem' }}>
      <h1>= Stats Dashboard</h1>

      {/* Stat Cards */}
      {summary && (
        <div style={{ display: 'flex', justifyContent: 'space-between', gap: '1rem', marginBottom: '3rem' }}>
          <div style={cardStyle}>
            <h3>Total Listings</h3>
            <p>{summary["Total Listings"]}</p>
          </div>
          <div style={cardStyle}>
            <h3>Avg Listing Price</h3>
            <p>${parseFloat(summary["Avg Listing Price"]).toFixed(2)}</p>
          </div>
          <div style={cardStyle}>
            <h3>Avg Commute Time</h3>
            <p>{parseFloat(summary["Avg Commute Time"]).toFixed(2)} mins</p>
          </div>
        </div>
      )}

      {/* Student by Major Pie Chart */}
      <div style={{ marginBottom: '3rem' }}>
        <h2>Student Distribution by Major</h2>
        {students.by_major.length > 0 && (
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={students.by_major}
                dataKey="percent"
                nameKey="major"
                outerRadius={100}
                label
              >
                {students.by_major.map((_, index) => (
                  <Cell key={`major-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        )}
      </div>

      {/* Landlord Avg Price Bar Chart */}
      <div>
        <h2>Average Property Price by Landlord</h2>
        {landlords.length > 0 && (
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={landlords}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="avg_price" fill="#8884d8" name="Avg Price" />
            </BarChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
};

const cardStyle = {
  flex: 1,
  padding: '1rem',
  border: '1px solid #ddd',
  borderRadius: '10px',
  backgroundColor: '#f9f9f9',
  textAlign: 'center',
  boxShadow: '0 2px 5px rgba(0,0,0,0.1)'
};

export default Dashboard;