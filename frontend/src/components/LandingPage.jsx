import React from 'react';
import { Link } from 'react-router-dom';

const LandingPage = () => (
  <div className="landing">
    <h1>Welcome to HokieHunter</h1>
    <p>Helping VT students find off-campus housing!</p>

    <section>
      <h2>Profiles</h2>
      <ul>
        <li><strong>Student</strong>: View and book available properties.</li>
        <li><strong>Landlord</strong>: List your property, update info, manage tenants.</li>
        <li><strong>Admin</strong>: Moderate listings and manage users.</li>
      </ul>
    </section>

    <section>
      <h2>Get Started</h2>
      <Link to="/users">View Users</Link> | 
      <Link to="/properties">View Properties</Link> | 
      <Link to="/bookings">View Bookings</Link>
    </section>
  </div>
);

export default LandingPage;
