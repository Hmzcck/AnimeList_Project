import React, { useState } from 'react';
import axios from 'axios';
import './removeAnime.css'; 

const RemoveAnimePage = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [animeList, setAnimeList] = useState([]);

  const handleSearch = () => {
  
    axios.post(`/api/admin/search_anime`, { searchTerm })
      .then(response => {
        setAnimeList(response.data); 
      })
      .catch(error => console.error('Error fetching data:', error));
  };

  const handleRemove = (animeId) => {
    axios.delete(`/api/remove_anime/${animeId}`)
      .then(() => {
        const updatedList = animeList.filter(anime => anime[0] !== animeId);
        setAnimeList(updatedList);
      })
      .catch(error => console.error('Error removing anime:', error));
  };

  return (
    <div className="remove-anime-page">
      <h2>Remove Anime Page</h2>
      <div className="search-container">
        <input
          type="text"
          placeholder="Enter anime name"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <button onClick={handleSearch}>Search</button>
      </div>
      <div className="anime-list">
        {animeList.map((anime) => (
          <div key={anime[0]} className="anime-item">
            <strong>{anime[1]}</strong>
            <button onClick={() => handleRemove(anime[0])}>Remove</button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RemoveAnimePage;
