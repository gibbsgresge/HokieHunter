import React from 'react';
import LandlordAccount from './LandlordAccount';
import StudentAccount from './StudentAccount';
import AdminAccount from './AdminAccount';
function Account() {
  const role = localStorage.getItem('role');

  if (role === 'landlord') {
    return <LandlordAccount />;
  }

  if (role === 'student') {
    return <StudentAccount />
  }

  if (role === 'admin') {
    return <AdminAccount />;
  }

  return <div style={{ marginTop: 80, padding: 20 }}>You must be logged in to view this page.</div>;
}

export default Account;
