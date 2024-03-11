import React from 'react';
import './admin.css';
import { useNavigate } from 'react-router-dom';
const AdminDashboard = () => {

    const navigate = useNavigate();
  const handleAddAnime = () => {
    navigate('/addanime');
  };

  const handleRemoveAnime = () => {
    // Logic to remove anime
    console.log('Remove Anime');
    navigate('/removeAnime');
  };


  return (
    <div className="admin-dashboard">
      <div className="section anime-section">
        <h2>Anime Section</h2>
        <button onClick={handleAddAnime}>Add Anime</button>
        <button onClick={handleRemoveAnime}>Remove Anime</button>
      </div>
    </div>
  );
};

export default AdminDashboard;
